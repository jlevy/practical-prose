"""
Model-scoring runner for the qualitative rubric.

Reads an in-progress eval report YAML (typically produced by
`pprose report from-metrics`), invokes an LLM via Pydantic AI's provider-agnostic
Agent with the rubric + guidelines + artifact + structured-output schema, and
fills the YAML's qual + rule_findings + metadata.

Provider abstraction:
  The model is selected by a Pydantic AI model string (e.g. `anthropic:claude-opus-4-8`,
  `openai:gpt-5.2`). The default is the latest Claude Opus over Anthropic. Switching to a
  non-Anthropic provider requires that provider's `[extra]` in pyproject.toml
  (`pydantic-ai-slim[anthropic,openai,...]`); the call shape is identical.

Prompt caching:
  When the provider is Anthropic, the rubric + guidelines + instructions block is
  passed as `instructions` and marked cacheable via `anthropic_cache_instructions=True`.
  Subsequent calls in a batch (within the ~5 min TTL) reuse the cached prefix at
  ~0.1× the input cost. Other providers have their own caching semantics; the
  default behavior on a non-Anthropic provider is uncached.

API keys are read from the environment (e.g. `ANTHROPIC_API_KEY`). `.env` and
`.env.local` in the current directory hierarchy and `$HOME` are auto-loaded.

Run `pprose score --help` for the CLI surface.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import os
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Literal

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel, ConfigDict
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModelSettings
from pydantic_ai.settings import ModelSettings

from pprose import resources
from pprose import rubric_schema as rs
from pprose._concurrency import gather_limited
from pprose.eval_render import render_single_doc_rollup
from pprose.eval_report import (
    EvalReport,
    ExpressionReasons,
    ExpressionScores,
    FormReasons,
    FormScores,
    GroundingReasons,
    GroundingScores,
    JudgmentReasons,
    JudgmentScores,
    Location,
    PurposeReasons,
    PurposeScores,
    QualReasons,
    QualScores,
    ReasoningReasons,
    ReasoningScores,
    RuleFinding,
    Verdict,
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

# Per-call execution budget.
DEFAULT_MAX_TOKENS = 8192
DEFAULT_TIMEOUT_S = 600.0  # 10 minutes — Q10 decision


# Curated list of currently-recommended models, surfaced in --model help and via
# `--list-models`. Sourced from llm-pricing/data/llms.yml (the canonical
# tracking file for tool-capable models). Aliases on the right resolve to the
# Pydantic AI model string on the left.
#
# Users can also pass any other model string Pydantic AI accepts (e.g.
# `openai:gpt-5.2`, `google:gemini-3-pro-preview`); --model just won't suggest
# it. An unknown provider prefix raises at the agent boundary.
SUGGESTED_MODELS: tuple[tuple[str, str, str], ...] = (
    # (alias, full model string, one-line description)
    ("opus", "anthropic:claude-opus-4-8", "Anthropic Claude Opus 4.8 (flagship)"),
    ("sonnet", "anthropic:claude-sonnet-4-6", "Anthropic Claude Sonnet 4.6 (balanced)"),
    ("haiku", "anthropic:claude-haiku-4-5", "Anthropic Claude Haiku 4.5 (fast/cheap)"),
    ("gpt", "openai:gpt-5.5", "OpenAI GPT-5.5 (flagship)"),
    ("gpt-pro", "openai:gpt-5.5-pro", "OpenAI GPT-5.5 Pro (deep reasoning)"),
    ("gpt-mini", "openai:gpt-5.4-mini", "OpenAI GPT-5.4 Mini (mid-tier)"),
    ("gpt-nano", "openai:gpt-5.4-nano", "OpenAI GPT-5.4 Nano (cheapest)"),
    ("gemini", "google:gemini-3.5-flash", "Google Gemini 3.5 Flash"),
    ("gemini-pro", "google:gemini-3.1-pro-preview", "Google Gemini 3.1 Pro (preview)"),
    ("gemini-lite", "google:gemini-3.1-flash-lite", "Google Gemini 3.1 Flash Lite"),
)
_ALIAS_TO_MODEL = {alias: model for alias, model, _ in SUGGESTED_MODELS}


def _resolve_model(name: str) -> str:
    """
    Resolve a user-supplied model spec to a Pydantic AI model string.

    Accepts short aliases from SUGGESTED_MODELS, bare `claude-*` IDs (auto-
    prefixed with `anthropic:`), and any explicit `provider:model` string
    (which passes through untouched).

    Empty/None is rejected: the CLI requires --model so a misconfigured run is
    never silently routed to an unintended provider.
    """
    if not name:
        raise ValueError("model is required; pass --model or call _resolve_model with a string")
    if name in _ALIAS_TO_MODEL:
        return _ALIAS_TO_MODEL[name]
    if name.startswith("claude-") and ":" not in name:
        return f"anthropic:{name}"
    return name


def _provider_of(model: str) -> str:
    """Return the provider prefix (`anthropic`, `openai`, `google`, ...) of a resolved model."""
    return model.split(":", 1)[0] if ":" in model else "anthropic"


def _format_suggested_models() -> str:
    """Render SUGGESTED_MODELS as a human-readable block for --list-models / help."""
    width_alias = max(len(a) for a, _, _ in SUGGESTED_MODELS)
    width_model = max(len(m) for _, m, _ in SUGGESTED_MODELS)
    lines = ["Suggested models (pass any other Pydantic AI model string too):", ""]
    lines.extend(
        f"  {alias:<{width_alias}}  {model:<{width_model}}  {desc}"
        for alias, model, desc in SUGGESTED_MODELS
    )
    lines.append("")
    lines.append("Provider extras shipped: anthropic, openai, google.")
    lines.append("Bare claude-* IDs are auto-prefixed with `anthropic:`.")
    return "\n".join(lines)


def _load_env_files() -> None:
    """Load .env then .env.local from the cwd hierarchy and $HOME.

    Later files override earlier ones, so a more-specific .env.local trumps a
    less-specific .env.
    """
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
    "form": FormScores,
    "reasoning": ReasoningScores,
    "grounding": GroundingScores,
    "judgment": JudgmentScores,
}
_REASONS_CLS = {
    "purpose": PurposeReasons,
    "expression": ExpressionReasons,
    "form": FormReasons,
    "reasoning": ReasoningReasons,
    "grounding": GroundingReasons,
    "judgment": JudgmentReasons,
}
VALID_DIMENSION_KEYS = set(rs.dimension_keys())


@dataclass
class ScoredResult:
    qual: QualScores
    rule_findings: list[RuleFinding]
    qual_reasons: QualReasons = field(default_factory=QualReasons)


def _rule_bounds_appendix() -> str:
    # Inject per-dimension rule_number ranges so the model can't cite an
    # out-of-range rule (which the validator rejects, killing the whole eval).
    lines = [
        "## Rule-number bounds per dimension",
        "",
        "When citing `rule_number` under `rule_findings`, use only an integer in",
        "the range listed for that dimension. Numbers outside these ranges will",
        "fail validation and the eval will be discarded.",
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


def _cached_block_text() -> str:
    """
    Build the invariant instructions block: scoring directions + rule-bounds
    appendix + rubric + guidelines.

    Sent to the model as `instructions` (system prompt). Identical across every
    call in a batch, so when the provider is Anthropic and caching is enabled,
    the first call writes the cache and the rest read it within the ~5 min TTL.
    Pydantic AI generates the JSON schema for `ScoringResponse` automatically,
    so the template no longer carries an inline JSON example.
    """
    if not PROMPT_TEMPLATE_PATH.is_file():
        raise FileNotFoundError(f"prompt template missing: {PROMPT_TEMPLATE_PATH}")
    if not RUBRIC_PATH.is_file():
        raise FileNotFoundError(f"rubric missing: {RUBRIC_PATH}")
    if not GUIDELINES_PATH.is_file():
        raise FileNotFoundError(f"guidelines missing: {GUIDELINES_PATH}")
    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    template = template.replace("{{CANONICAL_NAMES}}", _canonical_names()).replace(
        "{{DIMENSION_COUNT}}", str(rs.dimension_count())
    )
    parts = [
        "# Inputs",
        "",
        "## Instructions",
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


# Structured output ----------------------------------------------------------
#
# Pydantic AI fills `output_type=ScoringResponse` directly from the model's
# tool call, replacing the old manual JSON-fence regex + dict-walking parser.
# The schema is generated automatically from these models and shipped to the
# model alongside the instructions; the model can no longer emit malformed
# JSON because the framework enforces conformance at the SDK boundary.


class ScoreEntry(BaseModel):
    """One score + reason for a single rubric dimension."""

    score: int | Literal["NA", "ERR"]
    reason: str = ""


class RawRuleFinding(BaseModel):
    """
    Permissive variant of RuleFinding used as the scorer's structured output.

    Mirrors RuleFinding's fields but skips the dimension/rule_number range
    validators so a single hallucinated value can be dropped in
    `_to_scored_result()` rather than failing the whole call. Surviving
    entries are re-validated through the strict RuleFinding before they reach
    the report.
    """

    model_config = ConfigDict(extra="forbid")
    dimension: str
    rule_number: int
    verdict: Verdict
    description: str
    locations: list[Location] = []


class ScoringResponse(BaseModel):
    """The validated shape of what the scoring agent emits per artifact."""

    scores: dict[str, ScoreEntry]
    rule_findings: list[RawRuleFinding] = []


def _to_scored_result(response: ScoringResponse) -> ScoredResult:
    """
    Regroup the flat ScoringResponse into the nested QualScores / QualReasons
    pair that downstream report code expects.

    Unknown dimension labels and out-of-range `rule_number` values are dropped
    with a stderr warning rather than crashing the whole eval — the model
    occasionally hallucinates one even with the bounds appendix in the prompt;
    the score and other findings remain useful. `ScoringResponse` uses
    `RawRuleFinding` (permissive) at the SDK boundary so the bad entry reaches
    this filter instead of being rejected by Pydantic AI.
    """
    missing = VALID_DIMENSION_KEYS - set(response.scores.keys())
    if missing:
        raise ValueError(f"response missing dimensions: {sorted(missing)}")
    extra = set(response.scores.keys()) - VALID_DIMENSION_KEYS
    if extra:
        raise ValueError(f"response has unknown dimension keys: {sorted(extra)}")

    def _score(key: str) -> int | str:
        s = response.scores[key].score
        if s in ("NA", "ERR"):
            return s
        if not (1 <= s <= 5):
            raise ValueError(f"dimension {key!r} score out of 1-5 range: {s!r}")
        return s

    def _reason(key: str) -> str | None:
        return response.scores[key].reason.strip() or None

    score_groups: dict[str, BaseModel] = {}
    reason_groups: dict[str, BaseModel] = {}
    for group in rs.GROUPS:
        score_groups[group.key] = _SCORES_CLS[group.key](
            **{d.key: _score(d.key) for d in group.dimensions}
        )
        reason_groups[group.key] = _REASONS_CLS[group.key](
            **{d.key: _reason(d.key) for d in group.dimensions}
        )
    qual = QualScores(**score_groups)
    qual_reasons = QualReasons(**reason_groups)

    kept_findings: list[RuleFinding] = []
    for finding in response.rule_findings:
        if finding.dimension not in rs.DIMENSIONS_BY_LABEL:
            sys.stderr.write(
                f"warning: dropping rule_finding with unknown dimension {finding.dimension!r}; "
                f"description: {finding.description[:120]!r}\n"
            )
            continue
        max_rule = rs.rule_count(finding.dimension)
        if max_rule and not (1 <= finding.rule_number <= max_rule):
            sys.stderr.write(
                f"warning: dropping out-of-range rule_finding rule_number={finding.rule_number} "
                f"for dimension {finding.dimension!r} (valid 1-{max_rule}); "
                f"description: {finding.description[:120]!r}\n"
            )
            continue
        kept_findings.append(RuleFinding.model_validate(finding.model_dump()))

    return ScoredResult(qual=qual, qual_reasons=qual_reasons, rule_findings=kept_findings)


# LLM client ----------------------------------------------------------------


@dataclass
class CallResult:
    """Wrapper around a scoring call capturing the parts we need downstream."""

    output: ScoringResponse
    model_id: str
    cache_write_tokens: int
    cache_read_tokens: int
    input_tokens: int
    output_tokens: int


def _model_settings(provider: str) -> ModelSettings | AnthropicModelSettings:
    """
    Per-provider settings.

    For Anthropic we opt into prompt caching of both the instructions block
    and the tool definitions, so a batch run amortizes the rubric + guidelines
    + schema overhead across all calls. Other providers fall back to the
    framework default.
    """
    if provider == "anthropic":
        return AnthropicModelSettings(
            max_tokens=DEFAULT_MAX_TOKENS,
            timeout=DEFAULT_TIMEOUT_S,
            anthropic_cache_instructions=True,
            anthropic_cache_tool_definitions=True,
        )
    return ModelSettings(
        max_tokens=DEFAULT_MAX_TOKENS,
        timeout=DEFAULT_TIMEOUT_S,
    )


def _build_agent(model: str) -> Agent[None, ScoringResponse]:
    """
    Construct the scoring Agent with provider-appropriate caching.

    `model` must be a non-empty string. An unknown provider prefix or model id
    raises `UserError` from Pydantic AI; we let that propagate so the CLI can
    print it and exit non-zero rather than silently scoring against the wrong
    provider.
    """
    resolved = _resolve_model(model)
    try:
        return Agent(
            model=resolved,
            output_type=ScoringResponse,
            instructions=_cached_block_text(),
            model_settings=_model_settings(_provider_of(resolved)),
        )
    except Exception as exc:
        # Re-raise with the user-facing model spec attached so the failure
        # message says what they asked for, not just the resolved string.
        raise ValueError(
            f"cannot load model {model!r} (resolved to {resolved!r}): {exc}. "
            f"Run `pprose score --list-models` for suggestions."
        ) from exc


def _result_to_call_result(result) -> CallResult:
    """Pull the output, model id, and per-call token usage out of an AgentRunResult."""
    usage = result.usage
    # The provider response is exposed at result.response with the resolved model
    # name; fall back to "unknown" if the framework didn't populate it (e.g. tests).
    model_id = getattr(getattr(result, "response", None), "model_name", "unknown")
    return CallResult(
        output=result.output,
        model_id=model_id,
        cache_write_tokens=getattr(usage, "cache_write_tokens", 0) or 0,
        cache_read_tokens=getattr(usage, "cache_read_tokens", 0) or 0,
        input_tokens=getattr(usage, "input_tokens", 0) or 0,
        output_tokens=getattr(usage, "output_tokens", 0) or 0,
    )


def call_scorer(artifact_block: str, *, model: str) -> CallResult:
    """Invoke the scoring agent synchronously."""
    agent = _build_agent(model)
    return _result_to_call_result(agent.run_sync(artifact_block))


async def call_scorer_async(artifact_block: str, *, model: str) -> CallResult:
    """Async variant of call_scorer, used by score_batch under gather_limited."""
    agent = _build_agent(model)
    return _result_to_call_result(await agent.run(artifact_block))


def _pydantic_ai_version() -> str:
    try:
        return version("pydantic-ai-slim")
    except Exception:
        return "unknown"


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
    """Return a new EvalReport with scored qual + rule_findings + evaluator merged in.

    If `repro` is provided (model-scoring path), its fields are recorded under
    metadata for reproducibility.
    """
    data = report.model_dump(mode="json", exclude_none=True)
    data.pop("derived", None)  # let validator recompute
    data["qual"] = scored.qual.model_dump(mode="json")
    data["qual_reasons"] = scored.qual_reasons.model_dump(mode="json")
    data["rule_findings"] = [v.model_dump(mode="json") for v in scored.rule_findings]
    data["metadata"]["evaluator"] = evaluator
    # Default `method` to the resolved provider so audit/comparison traceability
    # records which API actually scored the report (Anthropic, OpenAI, Google,
    # ...). Falls back to a provider-agnostic label when no repro context is
    # given (e.g. the manual-scoring + merge path in tests).
    default_method = "model (pydantic-ai)"
    if repro is not None and repro.model:
        provider = _provider_of(_resolve_model(repro.model))
        default_method = f"model ({provider} via pydantic-ai)"
    data["metadata"]["method"] = data["metadata"].get("method") or default_method
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
    if notes and notes.startswith("Stub — qual scores are "):
        data["metadata"].pop("notes", None)
    return EvalReport.model_validate(data)


@dataclass
class _ScorePrep:
    """Everything needed before the LLM call, computed once per artifact."""

    report: EvalReport
    artifact_path: Path
    artifact_block: str
    out_path: Path
    prompt_text: str


def _prepare_score(yaml_path: Path, *, out: Path | None) -> _ScorePrep:
    """Load the eval file, resolve the artifact path, build prompts + I/O paths."""
    report = EvalReport.from_eval_md(yaml_path)
    artifact_path = Path(report.artifact.path)
    if not artifact_path.is_absolute():
        artifact_path = REPO_ROOT / artifact_path

    cached_block = _cached_block_text()
    artifact_block = _artifact_block_text(artifact_path)

    out_path = out if out else yaml_path
    return _ScorePrep(
        report=report,
        artifact_path=artifact_path,
        artifact_block=artifact_block,
        out_path=out_path,
        prompt_text=cached_block + "\n\n" + artifact_block,
    )


def _apply_score(
    prep: _ScorePrep,
    result: CallResult,
    *,
    model: str,
    evaluator: str,
    allow_misaligned: bool,
    argv: list[str] | None,
    quiet: bool = False,
) -> int:
    """
    Reshape the agent's structured response, merge into the eval report, and
    write `.eval.md`.

    Returns 0 on success, 1 on alignment failure. Shared between the sync and
    async _score_one paths.
    """
    scored = _to_scored_result(result.output)

    cmd_str = " ".join(["pprose", "score"] + (argv or sys.argv[1:]))
    repro = ReproContext(
        model=model,
        model_id=result.model_id,
        command=cmd_str,
        prompt_sha256=_sha256_of_text(prep.prompt_text),
        rubric_sha256=_sha256_of_file(RUBRIC_PATH),
        guidelines_sha256=_sha256_of_file(GUIDELINES_PATH),
        artifact_sha256=_sha256_of_file(prep.artifact_path),
        sdk_version=_pydantic_ai_version(),
        cache_stats={
            "cache_write_tokens": result.cache_write_tokens,
            "cache_read_tokens": result.cache_read_tokens,
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
    model: str,
    evaluator: str,
    allow_misaligned: bool,
    argv: list[str] | None,
) -> int:
    """Score a single YAML via the sync SDK path. Returns 0 on success."""
    if not yaml_path.is_file():
        print(f"error: not a file: {yaml_path}", file=sys.stderr)
        return 1
    prep = _prepare_score(yaml_path, out=out)
    result = call_scorer(prep.artifact_block, model=model)
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
    model: str,
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
    result = await call_scorer_async(prep.artifact_block, model=model)
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
    model: str,
    evaluator: str,
    allow_misaligned: bool,
    argv: list[str] | None,
    max_concurrent: int = 8,
    max_rps: float = 4.0,
    after_success: Callable[[Path], None] | None = None,
) -> int:
    """Score N YAMLs in parallel via gather_limited.

    Prompt caching is shared across the calls (the rubric + guidelines block
    is byte-identical), so the first call writes the cache and subsequent
    calls within ~5 min read it at ~0.1× the input cost. Post-score hooks run
    only after all scoring calls finish, so synchronous work such as rendering
    does not occupy the async scoring concurrency slots.
    """
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
    for path, result in zip(yaml_paths, results, strict=True):
        if isinstance(result, BaseException):
            failures += 1
            print(f"FAIL [{path.name}]: {type(result).__name__}: {result}", file=sys.stderr)
        elif result != 0:
            failures += 1
            print(
                f"FAIL [{path.name}]: alignment / parse failure (see stderr above)", file=sys.stderr
            )
        else:
            if after_success is not None:
                try:
                    after_success(path)
                except Exception as e:
                    failures += 1
                    print(
                        f"FAIL [{path.name}]: scored OK but render failed: {type(e).__name__}: {e}",
                        file=sys.stderr,
                    )
                    continue
            print(f"OK   [{path.name}]", file=sys.stderr)

    print(
        f"batch: {len(yaml_paths) - failures}/{len(yaml_paths)} OK, {failures} failed",
        file=sys.stderr,
    )
    return 0 if failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Score the qual + rule_findings blocks of one or more eval reports "
            "via Pydantic AI. On Anthropic the rubric + guidelines block is cached "
            "across calls within ~5 minutes."
        ),
        epilog=(
            "Cost note: scoring makes a real, paid API call and --model is required. "
            "The opus alias selects the flagship model; pass a cheaper alias "
            "(sonnet/haiku/gpt-mini/gemini-lite) for smoke tests. API keys load from "
            "the environment and from .env then .env.local "
            "auto-discovered up the cwd hierarchy and in $HOME (later files override "
            "earlier). Because of that autoload, `env -u ANTHROPIC_API_KEY pprose score` "
            "can still make a billable call if a reachable .env/.env.local defines the key; "
            "use --dry-run for a no-call smoke test."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "yaml_paths",
        metavar="report_paths",
        nargs="*",
        help=(
            "One or more eval reports (typically from `pprose report from-metrics`). "
            "Multiple paths score them sequentially; pair with --batch for parallel. "
            "Omit when using --list-models."
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
            "Model to score with (required for actual scoring; not needed for "
            "--dry-run or --list-models). Accepts a short alias from --list-models "
            "(e.g. opus, gpt, gemini), a Pydantic AI model string "
            "(anthropic:claude-opus-4-8, openai:gpt-5.5, google:gemini-3.5-flash), "
            "or a bare claude-* ID (auto-prefixed with anthropic:). Unknown "
            "provider prefixes or model IDs raise at the agent boundary."
        ),
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="Print the curated list of suggested models and exit.",
    )
    parser.add_argument(
        "--evaluator",
        default="model (pydantic-ai)",
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
    # --render-html: compose with `pprose render` after the eval.md is written.
    # The render flags below mirror `pprose render --help` and are forwarded
    # verbatim. Without --render-html, score behaves exactly as before.
    parser.add_argument(
        "--render-html",
        action="store_true",
        help=(
            "After scoring, also render each report as a static HTML page next "
            "to its .eval.md (the same as running `pprose render <eval.md>`)."
        ),
    )
    parser.add_argument(
        "--render-page-size",
        choices=("letter", "a4"),
        default="letter",
        help="Page size for --render-html (default: letter).",
    )
    parser.add_argument(
        "--render-variant",
        default="interactive",
        help="Page-layout variant for --render-html (default: interactive).",
    )
    args = parser.parse_args(argv)

    if args.list_models:
        print(_format_suggested_models())
        return 0

    # Validate render options before any paid model call, but not for --dry-run,
    # which never scores or renders: a variant typo should not block printing the
    # prompt.
    if args.render_html and not args.dry_run:
        from pprose.render_html.renderer import available_variants

        variants = available_variants()
        if args.render_variant not in variants:
            available = ", ".join(variants) or "(none)"
            print(
                f"error: unknown render variant {args.render_variant!r}; available: {available}",
                file=sys.stderr,
            )
            return 2

    _load_env_files()

    yaml_paths = [Path(p) for p in args.yaml_paths]
    if not yaml_paths:
        print("error: at least one eval report path is required", file=sys.stderr)
        return 2
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

    if not args.model:
        print(
            "error: --model is required for scoring (omit only with --dry-run "
            "or --list-models). Run `pprose score --list-models` for suggestions.",
            file=sys.stderr,
        )
        return 2

    # Each provider reads its own API key from the environment. We surface the
    # missing-key error early for the resolved provider rather than waiting for
    # the SDK to raise on the first request.
    resolved = _resolve_model(args.model)
    provider = _provider_of(resolved)
    # Accepted API-key env vars per provider, canonical name first. google accepts
    # GEMINI_API_KEY too (the google-genai SDK's own name, and what many environments
    # set); when only the alias is present we bridge it to the canonical GOOGLE_API_KEY
    # that pydantic-ai's google provider reads.
    _API_KEY_ENV: dict[str, tuple[str, ...]] = {
        "anthropic": ("ANTHROPIC_API_KEY",),
        "openai": ("OPENAI_API_KEY",),
        "google": ("GOOGLE_API_KEY", "GEMINI_API_KEY"),
    }
    accepted = _API_KEY_ENV.get(provider)
    if accepted:
        present = next((name for name in accepted if os.environ.get(name)), None)
        if present is None:
            names = " or ".join(accepted)
            print(
                f"error: {names} not set (required for provider {provider!r}); "
                "add it to .env or .env.local (auto-loaded), or export it",
                file=sys.stderr,
            )
            return 2
        canonical = accepted[0]
        if present != canonical and not os.environ.get(canonical):
            os.environ[canonical] = os.environ[present]

    if args.batch:
        rc = asyncio.run(
            score_batch(
                yaml_paths,
                model=args.model,
                evaluator=args.evaluator,
                allow_misaligned=args.allow_misaligned,
                argv=argv,
                max_concurrent=args.max_concurrent,
                max_rps=args.max_rps,
                after_success=(
                    (lambda path: _render_after_score(path, args)) if args.render_html else None
                ),
            )
        )
        return rc

    failures = 0
    for yaml_path in yaml_paths:
        out_path = Path(args.out) if args.out else None
        rc = _score_one(
            yaml_path,
            out=out_path,
            model=args.model,
            evaluator=args.evaluator,
            allow_misaligned=args.allow_misaligned,
            argv=argv,
        )
        if rc != 0:
            failures += 1
            continue
        if args.render_html:
            # Mirror batch semantics: a render failure after a successful (paid)
            # scoring call is reported and reflected in the exit code, but does not
            # abort the remaining reports; the .eval.md on disk is already valid.
            target = out_path if out_path else yaml_path
            try:
                _render_after_score(target, args)
            except Exception as e:
                failures += 1
                print(
                    f"FAIL [{target.name}]: scored OK but render failed: {type(e).__name__}: {e}",
                    file=sys.stderr,
                )
    return 0 if failures == 0 else 1


def _render_after_score(eval_md_path: Path, args) -> None:
    """Compose `pprose score` + `pprose render` — render the just-written report."""
    # Imported lazily so importing eval_score doesn't import Jinja2.
    from pprose.render_html.renderer import RenderOpts, render_eval_report

    report = EvalReport.from_eval_md(eval_md_path)
    opts = RenderOpts(
        page_size=args.render_page_size,
        variant=args.render_variant,
        pprose_version=_pprose_version(),
    )
    html = render_eval_report(report, opts)
    out_html = _render_output_path(eval_md_path)
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(html, encoding="utf-8")
    print(f"OK: wrote {out_html}", file=sys.stderr)


def _render_output_path(eval_md_path: Path) -> Path:
    name = eval_md_path.name
    if name.endswith(".eval.md"):
        return eval_md_path.with_name(name[: -len(".md")] + ".html")
    return eval_md_path.with_suffix(".html")


def _pprose_version() -> str:
    try:
        return version("pprose")
    except PackageNotFoundError:
        return "dev"


if __name__ == "__main__":
    raise SystemExit(main())
