#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "chopdiff>=0.1.0",
#   "pydantic>=2.0",
#   "pyyaml>=6.0",
# ]
# ///
"""
Model-scoring runner for the qualitative rubric (calls `claude` CLI).

Reads an in-progress eval-report YAML (typically produced by
`eval_report.py from-metrics`), invokes the local `claude` CLI with the
rubric / guidelines / artifact / structured-output prompt, parses the JSON block
out of the response, and fills the YAML's qual + violations + metadata.evaluator.

Companion to (paths relative to the repository root):
  - scripts/eval_report.py (schema + from-metrics)
  - scripts/prompts/eval-rubric-score.md (the structured-output prompt)
  - docs/practical-prose-rubric.md (the rubric)

Usage:
  eval_score.py path/to/artifact.eval.yaml                         # update in place
  eval_score.py path/to/artifact.eval.yaml --out filled.eval.yaml  # write elsewhere
  eval_score.py path/to/artifact.eval.yaml --model sonnet          # specify Claude model
  eval_score.py path/to/artifact.eval.yaml --dry-run               # build prompt, skip API call
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rubric_schema as rs  # noqa: E402
from eval_report import (  # noqa: E402
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

BUNDLE_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = BUNDLE_ROOT.parents[3]
PROMPT_TEMPLATE_PATH = Path(__file__).resolve().parent / "prompts" / "eval-rubric-score.md"
RUBRIC_PATH = BUNDLE_ROOT / "docs" / "practical-prose-rubric.md"
GUIDELINES_PATH = BUNDLE_ROOT / "docs" / "practical-prose-guidelines.md"

JSON_FENCE_RE = re.compile(r"```json\s*\n(.+?)\n```", re.DOTALL)

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


def build_prompt(artifact_path: Path) -> str:
    """Compose the full prompt: instructions + rubric appendix + guidelines + artifact."""
    if not PROMPT_TEMPLATE_PATH.is_file():
        raise FileNotFoundError(f"prompt template missing: {PROMPT_TEMPLATE_PATH}")
    if not RUBRIC_PATH.is_file():
        raise FileNotFoundError(f"rubric missing: {RUBRIC_PATH}")
    if not GUIDELINES_PATH.is_file():
        raise FileNotFoundError(f"guidelines missing: {GUIDELINES_PATH}")
    if not artifact_path.is_file():
        raise FileNotFoundError(f"artifact missing: {artifact_path}")

    parts = [
        "# Inputs",
        "",
        "## Instructions and output format",
        "",
        PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8"),
        "",
        "## Rubric (practical-prose-rubric.md)",
        "",
        RUBRIC_PATH.read_text(encoding="utf-8"),
        "",
        "## Prescriptive guidelines (practical-prose-guidelines.md)",
        "",
        GUIDELINES_PATH.read_text(encoding="utf-8"),
        "",
        f"## Artifact under review ({artifact_path})",
        "",
        artifact_path.read_text(encoding="utf-8"),
    ]
    return "\n".join(parts)


def extract_json_block(text: str) -> dict:
    """Pull the first ```json fence out of the model response and parse it."""
    m = JSON_FENCE_RE.search(text)
    if not m:
        raise ValueError(
            "no ```json``` block in response; "
            f"got {len(text)} chars starting: {text[:200]!r}"
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
            raise ValueError(
                f"dimension {key!r} score must be int 0-5 or the literal 'NA': {s!r}"
            )
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
        violations.append(
            Violation(
                dimension=v["dimension"],
                rule_number=rn,
                description=v["description"],
                location=v.get("location"),
            )
        )
    return ScoredResult(qual=qual, qual_reasons=qual_reasons, violations=violations)


def call_claude(prompt: str, model: str | None = None) -> str:
    """Invoke the local `claude` CLI with the prompt, return stdout."""
    if shutil.which("claude") is None:
        raise RuntimeError(
            "claude CLI not found on PATH; install Claude Code or pass --dry-run"
        )
    cmd = ["claude", "-p", prompt]
    if model:
        cmd[1:1] = ["--model", model]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"claude CLI exited {result.returncode}: {result.stderr.strip()}"
        )
    return result.stdout


@dataclass
class ReproContext:
    """Reproducibility metadata captured at model-invocation time."""
    model: str | None = None
    command: str | None = None
    raw_response_path: str | None = None
    prompt_sha256: str | None = None
    rubric_sha256: str | None = None
    guidelines_sha256: str | None = None
    artifact_sha256: str | None = None


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
    data["metadata"]["method"] = data["metadata"].get("method") or "model (claude CLI)"
    data["metadata"]["status"] = "complete"
    if repro is not None:
        for key, value in (
            ("model", repro.model),
            ("command", repro.command),
            ("raw_response_path", repro.raw_response_path),
            ("prompt_sha256", repro.prompt_sha256),
            ("rubric_sha256", repro.rubric_sha256),
            ("guidelines_sha256", repro.guidelines_sha256),
            ("artifact_sha256", repro.artifact_sha256),
        ):
            if value is not None:
                data["metadata"][key] = value
    notes = data["metadata"].get("notes")
    stub_marker = "Stub — qual scores are 0"
    if notes and stub_marker in notes:
        data["metadata"].pop("notes", None)
    return EvalReport.model_validate(data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Score the qual + violations blocks of an eval-report YAML via the local claude CLI.",
    )
    parser.add_argument("yaml_path", help="Path to eval-report YAML (typically from `eval_report.py from-metrics`).")
    parser.add_argument("--out", default=None, help="Output path (default: rewrite in place).")
    parser.add_argument("--model", default=None, help="Claude model to invoke (passes through to `claude --model`).")
    parser.add_argument(
        "--evaluator", default="model (claude CLI)",
        help="Identity to record in metadata.evaluator.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Build the prompt and write it to stdout; do not call claude.",
    )
    parser.add_argument(
        "--allow-misaligned", action="store_true",
        help=(
            "Write the eval YAML even if the model's response violates the "
            "alignment property (score < 5 without a matching violation, or "
            "score 5 with one). Use only for inspection / debugging."
        ),
    )
    args = parser.parse_args(argv)

    yaml_path = Path(args.yaml_path)
    if not yaml_path.is_file():
        print(f"error: not a file: {yaml_path}", file=sys.stderr)
        return 1

    report = EvalReport.from_yaml(yaml_path)
    artifact_path = Path(report.artifact.path)
    if not artifact_path.is_absolute():
        artifact_path = REPO_ROOT / artifact_path

    prompt = build_prompt(artifact_path)

    if args.dry_run:
        sys.stdout.write(prompt)
        return 0

    response = call_claude(prompt, model=args.model)
    payload = extract_json_block(response)
    scored = parse_response(payload)

    out_path = Path(args.out) if args.out else yaml_path
    # Persist the raw model response next to the eval YAML so parse bugs and score
    # disputes are auditable later. Suffix `.eval.raw.txt` is stable + greppable.
    raw_path = out_path.with_suffix(out_path.suffix + ".raw.txt") \
        if not out_path.name.endswith(".eval.yaml") \
        else out_path.parent / (out_path.name[: -len(".eval.yaml")] + ".eval.raw.txt")
    raw_path.write_text(response, encoding="utf-8")

    cmd_str = " ".join(["eval_score.py"] + (argv or sys.argv[1:]))
    repro = ReproContext(
        model=args.model,
        command=cmd_str,
        raw_response_path=str(raw_path.relative_to(REPO_ROOT))
            if raw_path.is_relative_to(REPO_ROOT)
            else str(raw_path),
        prompt_sha256=_sha256_of_text(prompt),
        rubric_sha256=_sha256_of_file(RUBRIC_PATH),
        guidelines_sha256=_sha256_of_file(GUIDELINES_PATH),
        artifact_sha256=_sha256_of_file(artifact_path),
    )
    filled = merge_into_report(report, scored, evaluator=args.evaluator, repro=repro)

    align_errors = filled.alignment_errors()
    if align_errors and not args.allow_misaligned:
        print(
            f"error: model response violates the alignment principle:",
            file=sys.stderr,
        )
        for e in align_errors:
            print(f"  {e}", file=sys.stderr)
        print(
            f"  raw response preserved at: {raw_path}",
            file=sys.stderr,
        )
        print(
            "  hint: pass --allow-misaligned to write the YAML anyway for inspection",
            file=sys.stderr,
        )
        return 1
    if align_errors:
        print(
            f"warning: writing misaligned YAML (--allow-misaligned): "
            f"{len(align_errors)} alignment issue(s)",
            file=sys.stderr,
        )

    output = filled.to_yaml()
    out_path.write_text(output, encoding="utf-8")
    print(f"OK: wrote {out_path}", file=sys.stderr)
    print(f"     raw response: {raw_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
