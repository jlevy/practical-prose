"""
Model-scoring runner for the qualitative rubric (Anthropic SDK + prompt caching).

Reads an in-progress eval report YAML (typically produced by
`pprose report from-metrics`), invokes the Anthropic SDK with the rubric +
guidelines + artifact + structured-output prompt, parses the JSON block out
of the response, and fills the YAML's qual + violations + metadata.

The rubric / guidelines / instructions block is sent with `cache_control` so
subsequent calls in the same batch (within the cache TTL) reuse the cached
input — ~10× cheaper and faster per call after the first.

Reads `ANTHROPIC_API_KEY` from the environment; `.env` and `.env.local` in
the current directory hierarchy or `$HOME` are auto-loaded.

Run `pprose score --help` for the CLI surface.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import BaseModel

from pprose import resources
from pprose import rubric_schema as rs
from pprose.eval_render import render_single_doc_rollup
from pprose.eval_report import (
    EvalReport,
    ExpressionReasons,
    ExpressionScores,
    GroundingReasons,
    GroundingScores,
    JudgmentReasons,
    JudgmentScores,
    PurposeReasons,
    PurposeScores,
    QualReasons,
    QualScores,
    ReasoningReasons,
    ReasoningScores,
    Violation,
)

PACKAGE_ROOT = Path(__file__).resolve().parent


def _find_repo_root(start: Path) -> Path:
    # Walk up from `start` looking for a .git marker, used to resolve relative
    # artifact paths and to prefer the repo's own docs when dogfooding inside the
    # source tree. Fall back to `start` so the tool keeps functioning outside a
    # git tree (e.g. an installed wheel).
    for p in [start, *start.parents]:
        if (p / ".git").exists():
            return p
    return start


def _resolve_doc(name: str) -> Path:
    """Resolve a guideline doc, preferring a repo copy (dogfooding) over the bundle.

    Order: $PPROSE_DOCS_DIR/<name>.md, then REPO_ROOT/docs/<name>.md when the
    package sits inside the source repo, then the copy bundled in the wheel — so
    `pprose score` works standalone in any environment.
    """
    override = os.environ.get("PPROSE_DOCS_DIR")
    if override:
        p = Path(override) / f"{name}.md"
        if p.is_file():
            return p
    repo_doc = REPO_ROOT / "docs" / f"{name}.md"
    if repo_doc.is_file():
        return repo_doc
    return resources.doc_path("guidelines", name)


REPO_ROOT = _find_repo_root(PACKAGE_ROOT)
PROMPT_TEMPLATE_PATH = PACKAGE_ROOT / "prompts" / "eval-rubric-score.md"
RUBRIC_PATH = _resolve_doc("practical-prose-rubric")
GUIDELINES_PATH = _resolve_doc("practical-prose-guidelines")

JSON_FENCE_RE = re.compile(r"```json\s*\n(.+?)\n```", re.DOTALL)

# Defaults baked from plan-2026-05-12-eval-scoring-rearchitecture.md decisions.
DEFAULT_MODEL = "claude-sonnet-4-5"
DEFAULT_MAX_TOKENS = 8192
DEFAULT_TIMEOUT_S = 600.0  # 10 minutes — Q10 decision

# Anthropic publishes model aliases like "claude-sonnet-4-5", "claude-opus-4-1",
# "claude-haiku-4-5". Accept short names too for convenience.
_MODEL_ALIASES = {
    "sonnet": "claude-sonnet-4-5",
    "opus": "claude-opus-4-1",
    "haiku": "claude-haiku-4-5",
}


def _resolve_model(name: str | None) -> str:
    if not name:
        return DEFAULT_MODEL
    return _MODEL_ALIASES.get(name, name)


def _load_env_files() -> None:
    """Load .env then .env.local from the cwd hierarchy and $HOME.

    Later files override earlier ones, so a more-specific .env.local trumps a
    less-specific .env.
    """
    from dotenv import find_dotenv, load_dotenv

    for filename in (".env", ".env.local"):
        found = find_dotenv(filename=filename, usecwd=True)
        if found:
            load_dotenv(found, override=True)
        home_path = Path.home() / filename
        if home_path.exists():
            load_dotenv(home_path, override=True)


_SCORES_CLS = {
    "purpose": PurposeScores,
    "expression": ExpressionScores,
    "grounding": GroundingScores,
    "reasoning": ReasoningScores,
    "judgment": JudgmentScores,
}
_REASONS_CLS = {
    "purpose": PurposeReasons,
    "expression": ExpressionReasons,
    "grounding": GroundingReasons,
    "reasoning": ReasoningReasons,
    "judgment": JudgmentReasons,
}
VALID_DIMENSION_KEYS = set(rs.dimension_keys())


@dataclass
class ScoredResult:
    qual: QualScores
    violations: list[Violation]
    qual_reasons: QualReasons = field(default_factory=QualReasons)


def _rule_bounds_appendix() -> str:
    # Inject per-dimension rule_number ranges so the model can't cite an
    # out-of-range rule (which the validator rejects, killing the whole eval).
    lines = [
        "## Rule-number bounds per dimension",
        "",
        "When citing `rule_number` under `violations`, use only an integer in the",
        "range listed for that dimension. Numbers outside these ranges will fail",
        "validation and the eval will be discarded.",
        "",
    ]
    for group in rs.GROUPS:
        for dim in group.dimensions:
            count = rs.RULE_COUNTS[dim.key]
            lines.append(f"- **{dim.label}**: rules 1-{count}")
    return "\n".join(lines)


def _canonical_names() -> str:
    """Comma-separated canonical dimension labels, in schema order."""
    return ", ".join(d.label for d in rs.DIMENSIONS)


def _scores_json_skeleton() -> str:
    """The JSON output example, with one entry per dimension key, schema-derived."""
    key_fields = [f'"{d.key}":' for d in rs.DIMENSIONS]
    width = max(len(k) for k in key_fields)
    entries = [f'    {k:<{width}} {{"score": 0, "reason": "..."}}' for k in key_fields]
    body = ",\n".join(entries)
    return (
        "```json\n"
        "{\n"
        '  "scores": {\n'
        f"{body}\n"
        "  },\n"
        '  "violations": [\n'
        '    {"dimension": "Clarity", "rule_number": 4, "description": "...", '
        '"location": "L412-418"}\n'
        "  ]\n"
        "}\n"
        "```"
    )


def _cached_block_text() -> str:
    """The invariant block: instructions + rule-bounds appendix + rubric + guidelines.

    Identical across every call in a batch, so the SDK can serve it from the
    prompt cache after the first request. Kept as one logical block (one
    cache_control marker) for simplicity.
    """
    if not PROMPT_TEMPLATE_PATH.is_file():
        raise FileNotFoundError(f"prompt template missing: {PROMPT_TEMPLATE_PATH}")
    if not RUBRIC_PATH.is_file():
        raise FileNotFoundError(f"rubric missing: {RUBRIC_PATH}")
    if not GUIDELINES_PATH.is_file():
        raise FileNotFoundError(f"guidelines missing: {GUIDELINES_PATH}")
    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    template = (
        template.replace("{{CANONICAL_NAMES}}", _canonical_names())
        .replace("{{SCORES_JSON}}", _scores_json_skeleton())
        .replace("{{DIMENSION_COUNT}}", str(rs.dimension_count()))
    )
    parts = [
        "# Inputs",
        "",
        "## Instructions and output format",
        "",
        template,
        "",
        _rule_bounds_appendix(),
        "",
        "## Rubric (practical-prose-rubric.md)",
        "",
        RUBRIC_PATH.read_text(encoding="utf-8"),
        "",
        "## Prescriptive guidelines (practical-prose-guidelines.md)",
        "",
        GUIDELINES_PATH.read_text(encoding="utf-8"),
    ]
    return "\n".join(parts)


def _artifact_block_text(artifact_path: Path) -> str:
    if not artifact_path.is_file():
        raise FileNotFoundError(f"artifact missing: {artifact_path}")
    return "\n".join(
        [
            f"## Artifact under review ({artifact_path})",
            "",
            artifact_path.read_text(encoding="utf-8"),
        ]
    )


def build_prompt(artifact_path: Path) -> str:
    """Render the full prompt as a single string (used for --dry-run and prompt_sha256).

    The text matches what the SDK sees (cached block followed by artifact block),
    so the prompt_sha256 stays comparable across CLI-era and SDK-era YAMLs.
    """
    return _cached_block_text() + "\n\n" + _artifact_block_text(artifact_path)


def _build_messages(cached_block: str, artifact_block: str) -> list[dict]:
    """Assemble the SDK message list from pre-rendered block texts.

    One user message with two content blocks: the invariant block (rubric +
    guidelines + instructions) marked `cache_control: ephemeral`, then the
    uncached artifact body. The cache TTL is ~5 minutes; subsequent calls within
    that window read the cached prefix at ~0.1× the input cost.
    """
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": cached_block, "cache_control": {"type": "ephemeral"}},
                {"type": "text", "text": artifact_block},
            ],
        }
    ]


def extract_json_block(text: str) -> dict:
    """Pull the first ```json fence out of the model response and parse it."""
    m = JSON_FENCE_RE.search(text)
    if not m:
        raise ValueError(
            f"no ```json``` block in response; got {len(text)} chars starting: {text[:200]!r}"
        )
    payload = m.group(1).strip()
    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"json block did not parse: {exc}\npayload:\n{payload[:500]}") from exc


def parse_response(payload: dict) -> ScoredResult:
    """Translate a parsed JSON payload into QualScores + violations."""
    if "scores" not in payload or not isinstance(payload["scores"], dict):
        raise ValueError("response missing 'scores' object")
    scores_raw = payload["scores"]
    missing = VALID_DIMENSION_KEYS - set(scores_raw.keys())
    if missing:
        raise ValueError(f"response missing dimensions: {sorted(missing)}")
    extra = set(scores_raw.keys()) - VALID_DIMENSION_KEYS
    if extra:
        raise ValueError(f"response has unknown dimension keys: {sorted(extra)}")

    def _score(key: str) -> int | str:
        entry = scores_raw[key]
        if not isinstance(entry, dict) or "score" not in entry:
            raise ValueError(f"dimension {key!r} has no 'score' field")
        s = entry["score"]
        if s == "NA":
            return "NA"
        if not isinstance(s, int) or not 0 <= s <= 5:
            raise ValueError(f"dimension {key!r} score must be int 0-5 or the literal 'NA': {s!r}")
        return s

    def _reason(key: str) -> str | None:
        entry = scores_raw[key]
        if not isinstance(entry, dict):
            return None
        reason = entry.get("reason")
        if reason is None:
            return None
        if not isinstance(reason, str):
            raise ValueError(f"dimension {key!r} reason not str: {reason!r}")
        return reason.strip() or None

    score_groups: dict[str, BaseModel] = {}
    reason_groups: dict[str, BaseModel] = {}
    for group in rs.GROUPS:
        score_kwargs = {d.key: _score(d.key) for d in group.dimensions}
        reason_kwargs = {d.key: _reason(d.key) for d in group.dimensions}
        score_groups[group.key] = _SCORES_CLS[group.key](**score_kwargs)
        reason_groups[group.key] = _REASONS_CLS[group.key](**reason_kwargs)
    qual = QualScores(**score_groups)
    qual_reasons = QualReasons(**reason_groups)

    violations_raw = payload.get("violations", [])
    if not isinstance(violations_raw, list):
        raise ValueError("response 'violations' is not a list")
    violations: list[Violation] = []
    for v in violations_raw:
        if not isinstance(v, dict):
            raise ValueError(f"violation is not an object: {v!r}")
        rn = v.get("rule_number")
        if not isinstance(rn, int):
            raise ValueError(
                f"violation rule_number must be an integer, got {type(rn).__name__}: "
                f"{rn!r} (dimension {v.get('dimension')!r})"
            )
        # Drop out-of-range rule_numbers with a stderr warning rather than
        # crashing the whole eval — the model occasionally invents a number
        # past the dimension's bound even with the bounds appendix in the
        # prompt. The score and other citations are still useful; the raw
        # response is preserved for audit.
        try:
            max_rule = rs.rule_count(v["dimension"])
        except KeyError:
            max_rule = None
        if max_rule is not None and not (1 <= rn <= max_rule):
            sys.stderr.write(
                f"warning: dropping out-of-range violation rule_number={rn} "
                f"for dimension {v['dimension']!r} (valid 1-{max_rule}); "
                f"description: {(v.get('description') or '')[:120]!r}\n"
            )
            continue
        violations.append(
            Violation(
                dimension=v["dimension"],
                rule_number=rn,
                description=v["description"],
                location=v.get("location"),
            )
        )
    return ScoredResult(qual=qual, qual_reasons=qual_reasons, violations=violations)


@dataclass
class AnthropicCallResult:
    """Wrapper around an Anthropic response capturing what we need for audit + scoring."""

    text: str
    model_id: str
    cache_creation_input_tokens: int
    cache_read_input_tokens: int
    input_tokens: int
    output_tokens: int


def _extract_call_result(response) -> AnthropicCallResult:
    """Convert an SDK Message response into AnthropicCallResult."""
    text_parts: list[str] = []
    for block in response.content:
        if getattr(block, "type", None) == "text":
            text_parts.append(block.text)
    text = "".join(text_parts)
    usage = response.usage
    return AnthropicCallResult(
        text=text,
        model_id=response.model,
        cache_creation_input_tokens=getattr(usage, "cache_creation_input_tokens", 0) or 0,
        cache_read_input_tokens=getattr(usage, "cache_read_input_tokens", 0) or 0,
        input_tokens=getattr(usage, "input_tokens", 0) or 0,
        output_tokens=getattr(usage, "output_tokens", 0) or 0,
    )


def call_anthropic(
    messages: list[dict],
    *,
    model: str | None = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    timeout: float = DEFAULT_TIMEOUT_S,
) -> AnthropicCallResult:
    """Invoke the Anthropic Messages API (sync) with the prepared message list.

    Reads `ANTHROPIC_API_KEY` from the environment via the SDK default.
    Returns the response text plus the usage stats needed to populate
    `ReproContext.cache_stats`.
    """
    import anthropic

    client = anthropic.Anthropic(timeout=timeout)
    response = client.messages.create(
        model=_resolve_model(model),
        max_tokens=max_tokens,
        messages=messages,
    )
    return _extract_call_result(response)


async def call_anthropic_async(
    messages: list[dict],
    *,
    model: str | None = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    timeout: float = DEFAULT_TIMEOUT_S,
) -> AnthropicCallResult:
    """Async variant of call_anthropic, used by score_batch under gather_limited."""
    import anthropic

    client = anthropic.AsyncAnthropic(timeout=timeout)
    response = await client.messages.create(
        model=_resolve_model(model),
        max_tokens=max_tokens,
        messages=messages,
    )
    return _extract_call_result(response)


def _anthropic_sdk_version() -> str:
    import anthropic

    return getattr(anthropic, "__version__", "unknown")


@dataclass
class ReproContext:
    """Reproducibility metadata captured at model-invocation time."""

    model: str | None = None
    model_id: str | None = None
    command: str | None = None
    prompt_sha256: str | None = None
    rubric_sha256: str | None = None
    guidelines_sha256: str | None = None
    artifact_sha256: str | None = None
    sdk_version: str | None = None
    cache_stats: dict | None = None


def _sha256_of_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_of_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def merge_into_report(
    report: EvalReport,
    scored: ScoredResult,
    evaluator: str,
    repro: ReproContext | None = None,
) -> EvalReport:
    """Return a new EvalReport with scored qual + violations + evaluator merged in.

    If `repro` is provided (model-scoring path), its fields are recorded under
    metadata for reproducibility.
    """
    data = report.model_dump(mode="json", exclude_none=True)
    data.pop("derived", None)  # let validator recompute
    data["qual"] = scored.qual.model_dump(mode="json")
    data["qual_reasons"] = scored.qual_reasons.model_dump(mode="json")
    data["violations"] = [v.model_dump(mode="json") for v in scored.violations]
    data["metadata"]["evaluator"] = evaluator
    data["metadata"]["method"] = data["metadata"].get("method") or "model (anthropic SDK)"
    data["metadata"]["status"] = "complete"
    if repro is not None:
        for key, value in (
            ("model", repro.model),
            ("model_id", repro.model_id),
            ("command", repro.command),
            ("prompt_sha256", repro.prompt_sha256),
            ("rubric_sha256", repro.rubric_sha256),
            ("guidelines_sha256", repro.guidelines_sha256),
            ("artifact_sha256", repro.artifact_sha256),
            ("sdk_version", repro.sdk_version),
            ("cache_stats", repro.cache_stats),
        ):
            if value is not None:
                data["metadata"][key] = value
    notes = data["metadata"].get("notes")
    stub_marker = "Stub — qual scores are 0"
    if notes and stub_marker in notes:
        data["metadata"].pop("notes", None)
    return EvalReport.model_validate(data)


@dataclass
class _ScorePrep:
    """Everything needed before the SDK call, computed once per artifact."""

    report: EvalReport
    artifact_path: Path
    messages: list[dict]
    out_path: Path
    prompt_text: str


def _prepare_score(yaml_path: Path, *, out: Path | None) -> _ScorePrep:
    """Load the eval file, resolve the artifact path, build messages + I/O paths."""
    report = EvalReport.from_eval_md(yaml_path)
    artifact_path = Path(report.artifact.path)
    if not artifact_path.is_absolute():
        artifact_path = REPO_ROOT / artifact_path

    cached_block = _cached_block_text()
    artifact_block = _artifact_block_text(artifact_path)
    messages = _build_messages(cached_block, artifact_block)

    out_path = out if out else yaml_path
    return _ScorePrep(
        report=report,
        artifact_path=artifact_path,
        messages=messages,
        out_path=out_path,
        prompt_text=cached_block + "\n\n" + artifact_block,
    )


def _apply_score(
    prep: _ScorePrep,
    result: AnthropicCallResult,
    *,
    model: str | None,
    evaluator: str,
    allow_misaligned: bool,
    argv: list[str] | None,
    quiet: bool = False,
) -> int:
    """Parse the model response, merge into the eval report, write `.eval.md`.

    Returns 0 on success, 1 on alignment failure. Shared between the sync and
    async _score_one paths.
    """
    payload = extract_json_block(result.text)
    scored = parse_response(payload)

    cmd_str = " ".join(["pprose", "score"] + (argv or sys.argv[1:]))
    repro = ReproContext(
        model=model,
        model_id=result.model_id,
        command=cmd_str,
        prompt_sha256=_sha256_of_text(prep.prompt_text),
        rubric_sha256=_sha256_of_file(RUBRIC_PATH),
        guidelines_sha256=_sha256_of_file(GUIDELINES_PATH),
        artifact_sha256=_sha256_of_file(prep.artifact_path),
        sdk_version=_anthropic_sdk_version(),
        cache_stats={
            "creation_input_tokens": result.cache_creation_input_tokens,
            "read_input_tokens": result.cache_read_input_tokens,
            "input_tokens": result.input_tokens,
            "output_tokens": result.output_tokens,
        },
    )
    filled = merge_into_report(prep.report, scored, evaluator=evaluator, repro=repro)

    align_errors = filled.alignment_errors()
    if align_errors and not allow_misaligned:
        print(
            f"error [{prep.out_path.name}]: model response violates alignment principle:",
            file=sys.stderr,
        )
        for e in align_errors:
            print(f"  {e}", file=sys.stderr)
        print(
            "  hint: pass --allow-misaligned to write the YAML anyway for inspection",
            file=sys.stderr,
        )
        return 1
    if align_errors:
        print(
            f"warning [{prep.out_path.name}]: writing misaligned YAML "
            f"(--allow-misaligned): {len(align_errors)} alignment issue(s)",
            file=sys.stderr,
        )

    body = render_single_doc_rollup(filled, heading_level=1)
    output = filled.to_eval_md(body)
    prep.out_path.write_text(output, encoding="utf-8")
    if not quiet:
        print(f"OK: wrote {prep.out_path}", file=sys.stderr)
    return 0


def _score_one(
    yaml_path: Path,
    *,
    out: Path | None,
    model: str | None,
    evaluator: str,
    allow_misaligned: bool,
    argv: list[str] | None,
) -> int:
    """Score a single YAML via the sync SDK path. Returns 0 on success."""
    if not yaml_path.is_file():
        print(f"error: not a file: {yaml_path}", file=sys.stderr)
        return 1
    prep = _prepare_score(yaml_path, out=out)
    result = call_anthropic(prep.messages, model=model)
    return _apply_score(
        prep,
        result,
        model=model,
        evaluator=evaluator,
        allow_misaligned=allow_misaligned,
        argv=argv,
    )


async def _score_one_async(
    yaml_path: Path,
    *,
    out: Path | None,
    model: str | None,
    evaluator: str,
    allow_misaligned: bool,
    argv: list[str] | None,
    quiet: bool = False,
) -> int:
    """Score a single YAML via the async SDK path. Used by score_batch."""
    if not yaml_path.is_file():
        print(f"error: not a file: {yaml_path}", file=sys.stderr)
        return 1
    prep = _prepare_score(yaml_path, out=out)
    result = await call_anthropic_async(prep.messages, model=model)
    return _apply_score(
        prep,
        result,
        model=model,
        evaluator=evaluator,
        allow_misaligned=allow_misaligned,
        argv=argv,
        quiet=quiet,
    )


async def score_batch(
    yaml_paths: list[Path],
    *,
    model: str | None,
    evaluator: str,
    allow_misaligned: bool,
    argv: list[str] | None,
    max_concurrent: int = 8,
    max_rps: float = 4.0,
) -> int:
    """Score N YAMLs in parallel via gather_limited.

    Prompt caching is shared across the calls (the rubric + guidelines block
    is byte-identical), so the first call writes the cache and subsequent
    calls within ~5 min read it at ~0.1× the input cost. Order of completion
    is unrelated to order of input; results are reported as docs finish.
    """
    from pprose._concurrency import gather_limited

    if not yaml_paths:
        return 0

    print(
        f"batch: scoring {len(yaml_paths)} YAMLs "
        f"(max_concurrent={max_concurrent}, max_rps={max_rps})",
        file=sys.stderr,
    )

    coros = [
        _score_one_async(
            p,
            out=None,
            model=model,
            evaluator=evaluator,
            allow_misaligned=allow_misaligned,
            argv=argv,
            quiet=True,
        )
        for p in yaml_paths
    ]
    results = await gather_limited(
        *coros,
        max_concurrent=max_concurrent,
        max_rps=max_rps,
        return_exceptions=True,
    )

    failures = 0
    for path, rc in zip(yaml_paths, results, strict=True):
        if isinstance(rc, BaseException):
            failures += 1
            print(f"FAIL [{path.name}]: {type(rc).__name__}: {rc}", file=sys.stderr)
        elif rc != 0:
            failures += 1
            print(
                f"FAIL [{path.name}]: alignment / parse failure (see stderr above)", file=sys.stderr
            )
        else:
            print(f"OK   [{path.name}]", file=sys.stderr)

    print(
        f"batch: {len(yaml_paths) - failures}/{len(yaml_paths)} OK, {failures} failed",
        file=sys.stderr,
    )
    return 0 if failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Score the qual + violations blocks of one or more eval reports "
            "via the Anthropic SDK. The rubric + guidelines block is cached "
            "across calls within ~5 minutes."
        ),
    )
    parser.add_argument(
        "yaml_paths",
        metavar="report_paths",
        nargs="+",
        help=(
            "One or more eval reports (typically from `pprose report from-metrics`). "
            "Multiple paths score them sequentially; pair with --batch for parallel."
        ),
    )
    parser.add_argument(
        "--out",
        default=None,
        help=(
            "Output path for a single eval report (default: rewrite in place). "
            "Not allowed when scoring multiple reports in one run."
        ),
    )
    parser.add_argument(
        "--model",
        default=None,
        help=(
            f"Claude model alias or ID (e.g. sonnet, opus, haiku, or a full ID). "
            f"Default: {DEFAULT_MODEL}."
        ),
    )
    parser.add_argument(
        "--evaluator",
        default="model (anthropic SDK)",
        help="Identity to record in metadata.evaluator.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Render the prompt and write it to stdout; do not call the API.",
    )
    parser.add_argument(
        "--allow-misaligned",
        action="store_true",
        help=(
            "Write the eval report even if the model's response violates the "
            "alignment property (score < 5 without a matching violation, or "
            "score 5 with one). Use only for inspection / debugging."
        ),
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help=(
            "Score the listed eval reports in parallel via bounded async concurrency. "
            "The rubric + guidelines block is shared across calls, so the first "
            "call writes the prompt cache and the rest read it (~10× cheaper)."
        ),
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=8,
        help="In --batch mode: maximum simultaneous in-flight SDK calls (default 8).",
    )
    parser.add_argument(
        "--max-rps",
        type=float,
        default=4.0,
        help="In --batch mode: maximum SDK request starts per second (default 4).",
    )
    args = parser.parse_args(argv)

    _load_env_files()

    yaml_paths = [Path(p) for p in args.yaml_paths]
    if args.out and len(yaml_paths) > 1:
        print("error: --out is only valid with a single eval report", file=sys.stderr)
        return 2
    for p in yaml_paths:
        if not p.is_file():
            print(f"error: not a file: {p}", file=sys.stderr)
            return 1

    if args.dry_run:
        # Dry-run only meaningful for a single doc.
        if len(yaml_paths) > 1:
            print("error: --dry-run is only valid with a single eval report", file=sys.stderr)
            return 2
        report = EvalReport.from_eval_md(yaml_paths[0])
        artifact_path = Path(report.artifact.path)
        if not artifact_path.is_absolute():
            artifact_path = REPO_ROOT / artifact_path
        sys.stdout.write(build_prompt(artifact_path))
        return 0

    if "ANTHROPIC_API_KEY" not in os.environ:
        print(
            "error: ANTHROPIC_API_KEY not set; "
            "add it to .env or .env.local (auto-loaded), or export it",
            file=sys.stderr,
        )
        return 2

    if args.batch:
        import asyncio

        return asyncio.run(
            score_batch(
                yaml_paths,
                model=args.model,
                evaluator=args.evaluator,
                allow_misaligned=args.allow_misaligned,
                argv=argv,
                max_concurrent=args.max_concurrent,
                max_rps=args.max_rps,
            )
        )

    failures = 0
    for yaml_path in yaml_paths:
        rc = _score_one(
            yaml_path,
            out=Path(args.out) if args.out else None,
            model=args.model,
            evaluator=args.evaluator,
            allow_misaligned=args.allow_misaligned,
            argv=argv,
        )
        if rc != 0:
            failures += 1
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
