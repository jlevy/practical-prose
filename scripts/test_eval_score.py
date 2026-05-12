#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "chopdiff>=0.1.0",
#   "pydantic>=2.0",
#   "pyyaml>=6.0",
#   "pytest>=8.0",
# ]
# ///
"""Tests for scripts/eval_score.py — subagent runner for qualitative scoring.

Run:
  uv run --script scripts/test_eval_score.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from eval_score import (  # noqa: E402
    build_prompt,
    extract_json_block,
    main,
    merge_into_report,
    parse_response,
)
from eval_report import (  # noqa: E402
    EvalReport,
    ExpressionScores,
    GroundingScores,
    JudgmentScores,
    PurposeScores,
    QualScores,
    ReasoningScores,
    Violation,
)

SCRIPTS_DIR = Path(__file__).resolve().parent
FIXTURES = SCRIPTS_DIR / "test_fixtures" / "practical_prose_metrics"


def _full_payload(score: int = 4, with_violation: bool = True) -> dict:
    """Build a JSON payload covering every rubric dimension at a uniform score."""
    import rubric_schema as rs
    payload = {
        "scores": {
            d.key: {"score": score, "reason": "test"} for d in rs.DIMENSIONS
        },
        "violations": [],
    }
    if with_violation:
        payload["violations"] = [
            {"dimension": "Clarity", "rule_number": 1, "description": "x", "location": "L1"}
        ]
    return payload


# ---------------------------------------------------------------------------
# extract_json_block
# ---------------------------------------------------------------------------


def test_extract_json_block_basic():
    text = 'Some prose.\n\n```json\n{"a": 1}\n```\n\nMore prose.'
    assert extract_json_block(text) == {"a": 1}


def test_extract_json_block_no_fence_raises():
    with pytest.raises(ValueError, match="no .*json.* block"):
        extract_json_block("just prose, no fence")


def test_extract_json_block_invalid_json_raises():
    with pytest.raises(ValueError, match="did not parse"):
        extract_json_block("```json\n{not valid}\n```")


def test_extract_json_block_takes_first_fence():
    text = '```json\n{"a": 1}\n```\n```json\n{"b": 2}\n```'
    assert extract_json_block(text) == {"a": 1}


# ---------------------------------------------------------------------------
# parse_response
# ---------------------------------------------------------------------------


def test_parse_response_full_valid():
    result = parse_response(_full_payload(score=5, with_violation=False))
    assert result.qual.expression.clarity == 5
    assert result.qual.judgment.robustness == 5
    assert result.violations == []


def test_parse_response_extracts_reasons():
    """Per-dimension reason strings should flow into qual_reasons."""
    payload = _full_payload(score=4, with_violation=False)
    payload["scores"]["clarity"]["reason"] = "trite phrasing at L412"
    payload["scores"]["depth"]["reason"] = "scope not declared"
    result = parse_response(payload)
    assert result.qual_reasons.expression.clarity == "trite phrasing at L412"
    assert result.qual_reasons.purpose.depth == "scope not declared"
    # Whitespace-only reasons become None
    assert result.qual_reasons.judgment.robustness is not None


def test_parse_response_missing_dimension_raises():
    payload = _full_payload()
    del payload["scores"]["depth"]
    with pytest.raises(ValueError, match="missing dimensions"):
        parse_response(payload)


def test_parse_response_unknown_dimension_raises():
    payload = _full_payload()
    payload["scores"]["mystery"] = {"score": 4, "reason": "x"}
    with pytest.raises(ValueError, match="unknown dimension"):
        parse_response(payload)


def test_parse_response_score_out_of_range_raises():
    payload = _full_payload()
    payload["scores"]["clarity"] = {"score": 9, "reason": "x"}
    with pytest.raises(ValueError, match="must be int 0-5 or the literal 'NA'"):
        parse_response(payload)


def test_parse_response_score_not_int_raises():
    payload = _full_payload()
    payload["scores"]["clarity"] = {"score": "four", "reason": "x"}
    with pytest.raises(ValueError, match="must be int 0-5 or the literal 'NA'"):
        parse_response(payload)


def test_parse_response_score_na_accepted():
    """The literal 'NA' is a valid score and round-trips into the qual block."""
    payload = _full_payload()
    payload["scores"]["calibration"] = {
        "score": "NA",
        "reason": "no probability or forecast claims",
    }
    result = parse_response(payload)
    assert result.qual.judgment.calibration == "NA"
    assert result.qual_reasons.judgment.calibration == "no probability or forecast claims"


def test_parse_response_violations_parsed():
    payload = _full_payload()
    payload["violations"] = [
        {"dimension": "Clarity", "rule_number": 4, "description": "register", "location": "L412"},
        {"dimension": "Soundness", "rule_number": 3, "description": "method", "location": "§2.7"},
    ]
    result = parse_response(payload)
    assert len(result.violations) == 2
    assert result.violations[0].dimension == "Clarity"
    assert result.violations[1].rule_number == 3


def test_parse_response_violations_optional_location():
    payload = _full_payload()
    payload["violations"] = [{"dimension": "Clarity", "rule_number": 4, "description": "x"}]
    result = parse_response(payload)
    assert result.violations[0].location is None


def test_parse_response_no_scores_object_raises():
    with pytest.raises(ValueError, match="missing 'scores'"):
        parse_response({"violations": []})


# ---------------------------------------------------------------------------
# merge_into_report
# ---------------------------------------------------------------------------


def _stub_report(tmp_path: Path) -> EvalReport:
    from eval_report import main as report_main
    out = tmp_path / "stub.eval.yaml"
    rc = report_main([
        "from-metrics",
        str(FIXTURES / "all_headings.md"),
        "--out", str(out),
    ])
    assert rc == 0
    return EvalReport.from_yaml(out)


def test_merge_replaces_qual_and_violations(tmp_path: Path):
    stub = _stub_report(tmp_path)
    qual = QualScores(
        expression=ExpressionScores(clarity=5, coherence=5, concision=5, organization=5, style_consistency=0, formatting=0),
        purpose=PurposeScores(suitability=5, breadth=5, depth=5),
        grounding=GroundingScores(verifiability=5, factuality=5),
        reasoning=ReasoningScores(inference_discipline=5, soundness=5, precision=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=5),
    )
    from eval_score import ScoredResult

    scored = ScoredResult(qual=qual, violations=[])
    merged = merge_into_report(stub, scored, evaluator="test-eval")

    assert merged.qual.expression.clarity == 5
    assert merged.violations == []
    assert merged.metadata.evaluator == "test-eval"
    # The stub note should be cleared (qual is no longer all-zero)
    assert merged.metadata.notes is None or "Stub" not in (merged.metadata.notes or "")
    # Quant block is preserved unchanged.
    assert merged.quant.headings.total == stub.quant.headings.total


def test_merge_preserves_existing_method(tmp_path: Path):
    stub = _stub_report(tmp_path)
    # Pre-set a method
    data = stub.model_dump(mode="json", exclude_none=True)
    data["metadata"]["method"] = "12-dim re-baseline"
    stub = EvalReport.model_validate(data)

    qual = QualScores(
        expression=ExpressionScores(clarity=5, coherence=5, concision=5, organization=5, style_consistency=0, formatting=0),
        purpose=PurposeScores(suitability=5, breadth=5, depth=5),
        grounding=GroundingScores(verifiability=5, factuality=5),
        reasoning=ReasoningScores(inference_discipline=5, soundness=5, precision=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=5),
    )
    from eval_score import ScoredResult

    merged = merge_into_report(stub, ScoredResult(qual=qual, violations=[]), evaluator="x")
    assert merged.metadata.method == "12-dim re-baseline"


def test_merge_alignment_clean_passes_strict_validate(tmp_path: Path):
    """Merging score-5-everywhere with no violations produces an alignment-clean report."""
    stub = _stub_report(tmp_path)
    qual = QualScores(
        expression=ExpressionScores(clarity=5, coherence=5, concision=5, organization=5, style_consistency=0, formatting=0),
        purpose=PurposeScores(suitability=5, breadth=5, depth=5),
        grounding=GroundingScores(verifiability=5, factuality=5),
        reasoning=ReasoningScores(inference_discipline=5, soundness=5, precision=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=5),
    )
    from eval_score import ScoredResult

    merged = merge_into_report(stub, ScoredResult(qual=qual, violations=[]), evaluator="x")
    assert merged.alignment_errors() == []


def test_merge_with_proper_violations_passes_alignment(tmp_path: Path):
    """A sub-5 score with a matching violation is alignment-valid after merge."""
    stub = _stub_report(tmp_path)
    qual = QualScores(
        expression=ExpressionScores(clarity=4, coherence=5, concision=5, organization=5, style_consistency=0, formatting=0),
        purpose=PurposeScores(suitability=5, breadth=5, depth=5),
        grounding=GroundingScores(verifiability=5, factuality=5),
        reasoning=ReasoningScores(inference_discipline=5, soundness=5, precision=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=5),
    )
    from eval_score import ScoredResult

    violations = [Violation(dimension="Clarity", rule_number=4, description="x", location="L1")]
    merged = merge_into_report(stub, ScoredResult(qual=qual, violations=violations), evaluator="x")
    assert merged.alignment_errors() == []


# ---------------------------------------------------------------------------
# build_prompt
# ---------------------------------------------------------------------------


def test_build_prompt_includes_all_inputs():
    """The prompt should contain the rubric, guidelines, artifact, and instructions."""
    prompt = build_prompt(FIXTURES / "all_headings.md")
    assert "practical-prose-rubric.md" in prompt
    assert "practical-prose-guidelines.md" in prompt
    assert "Artifact under review" in prompt
    # The fixture has known h1 content
    assert "h1" in prompt.lower() or "heading" in prompt.lower()
    # Output-format instructions are present
    assert "```json" in prompt


def test_build_prompt_missing_artifact_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        build_prompt(tmp_path / "does-not-exist.md")


# ---------------------------------------------------------------------------
# main CLI (dry-run path; no API call)
# ---------------------------------------------------------------------------


def test_main_dry_run_writes_prompt_to_stdout(tmp_path: Path, capsys):
    from eval_report import main as report_main

    stub = tmp_path / "stub.eval.yaml"
    rc = report_main([
        "from-metrics",
        str(FIXTURES / "all_headings.md"),
        "--out", str(stub),
    ])
    assert rc == 0

    rc = main([str(stub), "--dry-run"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "practical-prose-rubric.md" in out
    assert "Artifact under review" in out


def test_main_missing_yaml_returns_error(tmp_path: Path):
    rc = main([str(tmp_path / "missing.eval.yaml"), "--dry-run"])
    assert rc == 1


# ---------------------------------------------------------------------------
# Round-trip via merge → YAML → from_yaml
# ---------------------------------------------------------------------------


def test_round_trip_merge_then_load(tmp_path: Path):
    stub = _stub_report(tmp_path)
    qual = QualScores(
        expression=ExpressionScores(clarity=4, coherence=5, concision=4, organization=5, style_consistency=4, formatting=5),
        purpose=PurposeScores(suitability=4, breadth=4, depth=4),
        grounding=GroundingScores(verifiability=5, factuality=4),
        reasoning=ReasoningScores(inference_discipline=4, soundness=5, precision=4),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=4),
    )
    sub5_dims = [
        "Clarity", "Concision", "Style Consistency", "Suitability", "Breadth", "Depth",
        "Factuality", "Inference Discipline", "Precision", "Robustness",
    ]
    violations = [
        Violation(dimension=d, rule_number=1, description="x", location="L1") for d in sub5_dims
    ]
    from eval_score import ScoredResult

    merged = merge_into_report(stub, ScoredResult(qual=qual, violations=violations), evaluator="round-trip")

    out_path = tmp_path / "merged.eval.yaml"
    out_path.write_text(merged.to_yaml(), encoding="utf-8")
    reloaded = EvalReport.from_yaml(out_path)

    assert reloaded.qual.expression.clarity == 4
    assert reloaded.qual.expression.coherence == 5
    assert len(reloaded.violations) == 10
    assert reloaded.metadata.evaluator == "round-trip"
    assert reloaded.metadata.status == "complete"
    assert reloaded.alignment_errors() == []


def test_merge_populates_reproducibility_metadata(tmp_path: Path):
    """A ReproContext flows through merge_into_report into metadata.*"""
    from eval_score import ReproContext, ScoredResult

    stub = _stub_report(tmp_path)
    qual = QualScores(
        expression=ExpressionScores(clarity=5, coherence=5, concision=5, organization=5, style_consistency=0, formatting=0),
        purpose=PurposeScores(suitability=5, breadth=5, depth=5),
        grounding=GroundingScores(verifiability=5, factuality=5),
        reasoning=ReasoningScores(inference_discipline=5, soundness=5, precision=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=5),
    )
    repro = ReproContext(
        model="claude-opus-4-7",
        command="eval_score.py /tmp/x.eval.yaml",
        raw_response_path="/tmp/x.eval.raw.txt",
        prompt_sha256="a" * 64,
        rubric_sha256="b" * 64,
        guidelines_sha256="c" * 64,
        artifact_sha256="d" * 64,
    )
    merged = merge_into_report(
        stub, ScoredResult(qual=qual, violations=[]), evaluator="test", repro=repro
    )
    assert merged.metadata.model == "claude-opus-4-7"
    assert merged.metadata.command == "eval_score.py /tmp/x.eval.yaml"
    assert merged.metadata.raw_response_path == "/tmp/x.eval.raw.txt"
    assert merged.metadata.prompt_sha256 == "a" * 64
    assert merged.metadata.rubric_sha256 == "b" * 64
    assert merged.metadata.guidelines_sha256 == "c" * 64
    assert merged.metadata.artifact_sha256 == "d" * 64


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
