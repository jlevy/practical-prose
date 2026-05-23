"""Tests for scripts/eval_score.py — subagent runner for qualitative scoring.

Run:
  uv run --script scripts/test_eval_score.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from pprose.eval_render import render_single_doc_rollup
from pprose.eval_report import (  # noqa: E402
    EvalReport,
    ExpressionScores,
    GroundingScores,
    JudgmentScores,
    PurposeScores,
    QualScores,
    ReasoningScores,
    Violation,
)
from pprose.eval_score import (  # noqa: E402
    build_prompt,
    extract_json_block,
    main,
    merge_into_report,
    parse_response,
)

SCRIPTS_DIR = Path(__file__).resolve().parent
FIXTURES = SCRIPTS_DIR / "test_fixtures" / "practical_prose_metrics"


def _full_payload(score: int = 4, with_violation: bool = True) -> dict:
    """Build a JSON payload covering every rubric dimension at a uniform score."""
    from pprose import rubric_schema as rs

    payload = {
        "scores": {d.key: {"score": score, "reason": "test"} for d in rs.DIMENSIONS},
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
    from pprose.eval_report import main as report_main

    out = tmp_path / "stub.eval.md"
    rc = report_main(
        [
            "from-metrics",
            str(FIXTURES / "all_headings.md"),
            "--out",
            str(out),
        ]
    )
    assert rc == 0
    return EvalReport.from_eval_md(out)


def test_single_doc_rollup_coalesces_qualitative_groups(tmp_path: Path):
    stub = _stub_report(tmp_path)
    body = render_single_doc_rollup(stub, heading_level=1)

    assert "| **Purpose** | Suitability | 0 |" in body
    assert "|  | Scope | 0 |" in body
    assert "| Purpose | Scope |" not in body
    assert "|  | **Mean** |" in body
    assert "| **Purpose** | **Mean** |" not in body


def test_merge_replaces_qual_and_violations(tmp_path: Path):
    stub = _stub_report(tmp_path)
    qual = QualScores(
        expression=ExpressionScores(
            clarity=5, coherence=5, concision=5, organization=5, consistency=0, formatting=0
        ),
        purpose=PurposeScores(suitability=5, breadth=5, depth=5),
        grounding=GroundingScores(verifiability=5, factuality=5, relevance=5),
        reasoning=ReasoningScores(discipline=5, soundness=5, precision=5, parsimony=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=5),
    )
    from pprose.eval_score import ScoredResult

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
        expression=ExpressionScores(
            clarity=5, coherence=5, concision=5, organization=5, consistency=0, formatting=0
        ),
        purpose=PurposeScores(suitability=5, breadth=5, depth=5),
        grounding=GroundingScores(verifiability=5, factuality=5, relevance=5),
        reasoning=ReasoningScores(discipline=5, soundness=5, precision=5, parsimony=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=5),
    )
    from pprose.eval_score import ScoredResult

    merged = merge_into_report(stub, ScoredResult(qual=qual, violations=[]), evaluator="x")
    assert merged.metadata.method == "12-dim re-baseline"


def test_merge_alignment_clean_passes_strict_validate(tmp_path: Path):
    """Merging score-5-everywhere with no violations produces an alignment-clean report."""
    stub = _stub_report(tmp_path)
    qual = QualScores(
        expression=ExpressionScores(
            clarity=5, coherence=5, concision=5, organization=5, consistency=0, formatting=0
        ),
        purpose=PurposeScores(suitability=5, breadth=5, depth=5),
        grounding=GroundingScores(verifiability=5, factuality=5, relevance=5),
        reasoning=ReasoningScores(discipline=5, soundness=5, precision=5, parsimony=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=5),
    )
    from pprose.eval_score import ScoredResult

    merged = merge_into_report(stub, ScoredResult(qual=qual, violations=[]), evaluator="x")
    assert merged.alignment_errors() == []


def test_merge_with_proper_violations_passes_alignment(tmp_path: Path):
    """A sub-5 score with a matching violation is alignment-valid after merge."""
    stub = _stub_report(tmp_path)
    qual = QualScores(
        expression=ExpressionScores(
            clarity=4, coherence=5, concision=5, organization=5, consistency=0, formatting=0
        ),
        purpose=PurposeScores(suitability=5, breadth=5, depth=5),
        grounding=GroundingScores(verifiability=5, factuality=5, relevance=5),
        reasoning=ReasoningScores(discipline=5, soundness=5, precision=5, parsimony=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=5),
    )
    from pprose.eval_score import ScoredResult

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


def test_build_prompt_is_schema_derived():
    """The dimension list, JSON skeleton, and key count are generated from the
    schema, not hard-coded in the template. Adding a dimension to the YAML must
    flow into the prompt without editing the template."""
    import pprose.rubric_schema as rs

    prompt = build_prompt(FIXTURES / "all_headings.md")
    # No unsubstituted placeholders leak into the rendered prompt.
    for placeholder in ("{{CANONICAL_NAMES}}", "{{SCORES_JSON}}", "{{DIMENSION_COUNT}}"):
        assert placeholder not in prompt, f"unsubstituted placeholder: {placeholder}"
    # Every dimension key appears as a JSON score key, and every label appears in
    # the canonical-name list.
    for dim in rs.DIMENSIONS:
        assert f'"{dim.key}":' in prompt, f"missing key {dim.key}"
        assert dim.label in prompt, f"missing label {dim.label}"
    # The hard-coded count matches the schema.
    assert f"all {rs.dimension_count()} keys present" in prompt


def test_build_prompt_missing_artifact_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        build_prompt(tmp_path / "does-not-exist.md")


# ---------------------------------------------------------------------------
# main CLI (dry-run path; no API call)
# ---------------------------------------------------------------------------


def test_main_dry_run_writes_prompt_to_stdout(tmp_path: Path, capsys):
    from pprose.eval_report import main as report_main

    stub = tmp_path / "stub.eval.md"
    rc = report_main(
        [
            "from-metrics",
            str(FIXTURES / "all_headings.md"),
            "--out",
            str(stub),
        ]
    )
    assert rc == 0

    rc = main([str(stub), "--dry-run"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "practical-prose-rubric.md" in out
    assert "Artifact under review" in out


def test_main_missing_yaml_returns_error(tmp_path: Path):
    rc = main([str(tmp_path / "missing.eval.md"), "--dry-run"])
    assert rc == 1


# ---------------------------------------------------------------------------
# Round-trip via merge → YAML → from_yaml
# ---------------------------------------------------------------------------


def test_round_trip_merge_then_load(tmp_path: Path):
    stub = _stub_report(tmp_path)
    qual = QualScores(
        expression=ExpressionScores(
            clarity=4, coherence=5, concision=4, organization=5, consistency=4, formatting=5
        ),
        purpose=PurposeScores(suitability=4, breadth=4, depth=4),
        grounding=GroundingScores(verifiability=5, factuality=4, relevance=5),
        reasoning=ReasoningScores(discipline=4, soundness=5, precision=4, parsimony=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=4),
    )
    sub5_dims = [
        "Clarity",
        "Concision",
        "Consistency",
        "Suitability",
        "Breadth",
        "Depth",
        "Factuality",
        "Discipline",
        "Precision",
        "Robustness",
    ]
    violations = [
        Violation(dimension=d, rule_number=1, description="x", location="L1") for d in sub5_dims
    ]
    from pprose.eval_score import ScoredResult

    merged = merge_into_report(
        stub, ScoredResult(qual=qual, violations=violations), evaluator="round-trip"
    )

    out_path = tmp_path / "merged.eval.md"
    body = render_single_doc_rollup(merged, heading_level=1)
    out_path.write_text(merged.to_eval_md(body), encoding="utf-8")
    reloaded = EvalReport.from_eval_md(out_path)

    assert reloaded.qual.expression.clarity == 4
    assert reloaded.qual.expression.coherence == 5
    assert len(reloaded.violations) == 10
    assert reloaded.metadata.evaluator == "round-trip"
    assert reloaded.metadata.status == "complete"
    assert reloaded.alignment_errors() == []


def test_merge_populates_reproducibility_metadata(tmp_path: Path):
    """A ReproContext flows through merge_into_report into metadata.*"""
    from pprose.eval_score import ReproContext, ScoredResult

    stub = _stub_report(tmp_path)
    qual = QualScores(
        expression=ExpressionScores(
            clarity=5, coherence=5, concision=5, organization=5, consistency=0, formatting=0
        ),
        purpose=PurposeScores(suitability=5, breadth=5, depth=5),
        grounding=GroundingScores(verifiability=5, factuality=5, relevance=5),
        reasoning=ReasoningScores(discipline=5, soundness=5, precision=5, parsimony=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=5),
    )
    repro = ReproContext(
        model="claude-opus-4-7",
        command="eval_score.py /tmp/x.eval.md",
        prompt_sha256="a" * 64,
        rubric_sha256="b" * 64,
        guidelines_sha256="c" * 64,
        artifact_sha256="d" * 64,
    )
    merged = merge_into_report(
        stub, ScoredResult(qual=qual, violations=[]), evaluator="test", repro=repro
    )
    assert merged.metadata.model == "claude-opus-4-7"
    assert merged.metadata.command == "eval_score.py /tmp/x.eval.md"
    assert merged.metadata.prompt_sha256 == "a" * 64
    assert merged.metadata.rubric_sha256 == "b" * 64
    assert merged.metadata.guidelines_sha256 == "c" * 64
    assert merged.metadata.artifact_sha256 == "d" * 64


# ---------------------------------------------------------------------------
# SDK message shape (Phase 1)
# ---------------------------------------------------------------------------


def test_build_messages_has_cached_invariant_and_uncached_artifact():
    """The Anthropic message list must mark the rubric+guidelines block as cached."""
    from pprose.eval_score import _artifact_block_text, _build_messages, _cached_block_text

    messages = _build_messages(
        _cached_block_text(), _artifact_block_text(FIXTURES / "all_headings.md")
    )
    assert len(messages) == 1
    blocks = messages[0]["content"]
    assert len(blocks) == 2, "expected exactly two content blocks: cached + artifact"
    # Block 1: invariant, marked ephemeral.
    assert blocks[0]["type"] == "text"
    assert blocks[0]["cache_control"] == {"type": "ephemeral"}
    assert "practical-prose-rubric.md" in blocks[0]["text"]
    assert "Prescriptive guidelines" in blocks[0]["text"]
    # Block 2: artifact, NOT cached (every doc varies).
    assert blocks[1]["type"] == "text"
    assert "cache_control" not in blocks[1]
    assert "Artifact under review" in blocks[1]["text"]


def test_resolve_model_handles_aliases_and_full_ids():
    from pprose.eval_score import DEFAULT_MODEL, _resolve_model

    assert _resolve_model(None) == DEFAULT_MODEL
    assert _resolve_model("") == DEFAULT_MODEL
    assert _resolve_model("sonnet") == "claude-sonnet-4-5"
    assert _resolve_model("opus") == "claude-opus-4-1"
    assert _resolve_model("haiku") == "claude-haiku-4-5"
    # Full IDs pass through unchanged.
    assert _resolve_model("claude-sonnet-4-6") == "claude-sonnet-4-6"
    assert _resolve_model("claude-opus-4-7-20251015") == "claude-opus-4-7-20251015"


def test_repro_context_persists_sdk_fields(tmp_path: Path):
    """sdk_version + model_id + cache_stats flow through merge_into_report."""
    from pprose.eval_score import ReproContext, ScoredResult

    stub = _stub_report(tmp_path)
    qual = QualScores(
        expression=ExpressionScores(
            clarity=5, coherence=5, concision=5, organization=5, consistency=5, formatting=5
        ),
        purpose=PurposeScores(suitability=5, breadth=5, depth=5),
        grounding=GroundingScores(verifiability=5, factuality=5, relevance=5),
        reasoning=ReasoningScores(discipline=5, soundness=5, precision=5, parsimony=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=5),
    )
    repro = ReproContext(
        model="sonnet",
        model_id="claude-sonnet-4-5-20250929",
        sdk_version="0.39.0",
        cache_stats={
            "creation_input_tokens": 99000,
            "read_input_tokens": 0,
            "input_tokens": 1200,
            "output_tokens": 1800,
        },
    )
    merged = merge_into_report(
        stub, ScoredResult(qual=qual, violations=[]), evaluator="test", repro=repro
    )
    assert merged.metadata.model == "sonnet"
    assert merged.metadata.model_id == "claude-sonnet-4-5-20250929"
    assert merged.metadata.sdk_version == "0.39.0"
    assert merged.metadata.cache_stats == {
        "creation_input_tokens": 99000,
        "read_input_tokens": 0,
        "input_tokens": 1200,
        "output_tokens": 1800,
    }


class _FakeBlock:
    def __init__(self, text: str, type_: str = "text"):
        self.text = text
        self.type = type_


class _FakeUsage:
    def __init__(
        self,
        cache_creation_input_tokens: int = 99000,
        cache_read_input_tokens: int = 0,
        input_tokens: int = 1200,
        output_tokens: int = 1800,
    ):
        self.cache_creation_input_tokens = cache_creation_input_tokens
        self.cache_read_input_tokens = cache_read_input_tokens
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens


class _FakeResponse:
    def __init__(self, text: str, model_id: str, usage: _FakeUsage | None = None):
        self.content = [_FakeBlock(text)]
        self.model = model_id
        self.usage = usage or _FakeUsage()


class _FakeMessages:
    def __init__(self, response: _FakeResponse, capture: dict):
        self._response = response
        self._capture = capture

    def create(self, **kwargs):
        self._capture.update(kwargs)
        return self._response


class _FakeAnthropic:
    """Drop-in replacement for anthropic.Anthropic for tests."""

    last_capture: dict = {}

    def __init__(self, *args, **kwargs):
        _FakeAnthropic.last_capture = {"client_kwargs": kwargs}
        self.messages = _FakeMessages(
            _FakeAnthropic.next_response,
            _FakeAnthropic.last_capture,
        )

    @classmethod
    def stub(cls, text: str, model_id: str = "claude-sonnet-4-5-fake"):
        cls.next_response = _FakeResponse(text, model_id)


def test_call_anthropic_extracts_text_and_usage(monkeypatch):
    """call_anthropic returns text + cache usage from the SDK response."""
    import anthropic

    from pprose.eval_score import call_anthropic

    _FakeAnthropic.stub("hello world", model_id="claude-sonnet-4-5-fake")
    monkeypatch.setattr(anthropic, "Anthropic", _FakeAnthropic)

    result = call_anthropic([{"role": "user", "content": "x"}], model="sonnet")
    assert result.text == "hello world"
    assert result.model_id == "claude-sonnet-4-5-fake"
    assert result.cache_creation_input_tokens == 99000
    assert result.cache_read_input_tokens == 0
    # The SDK invocation gets the resolved model and our default max_tokens.
    captured = _FakeAnthropic.last_capture
    assert captured["model"] == "claude-sonnet-4-5"
    assert captured["max_tokens"] == 8192


def test_main_end_to_end_calls_sdk_and_persists_cache_stats(tmp_path: Path, monkeypatch):
    """Full main() path: SDK mocked, YAML written, cache_stats recorded."""
    import anthropic

    from pprose.eval_report import main as report_main
    from pprose.eval_score import main as score_main

    # Stub: a model response that scores every dimension at 5 (no violations needed).
    payload = _full_payload(score=5, with_violation=False)
    response_text = "Looks good.\n\n```json\n" + __import__("json").dumps(payload) + "\n```\n"
    _FakeAnthropic.stub(response_text, model_id="claude-sonnet-4-5-fake")
    monkeypatch.setattr(anthropic, "Anthropic", _FakeAnthropic)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-fake")

    stub = tmp_path / "stub.eval.md"
    rc = report_main(
        [
            "from-metrics",
            str(FIXTURES / "all_headings.md"),
            "--out",
            str(stub),
        ]
    )
    assert rc == 0

    rc = score_main([str(stub), "--model", "sonnet"])
    assert rc == 0

    report = EvalReport.from_eval_md(stub)
    assert report.metadata.status == "complete"
    assert report.metadata.model == "sonnet"
    assert report.metadata.model_id == "claude-sonnet-4-5-fake"
    assert report.metadata.cache_stats == {
        "creation_input_tokens": 99000,
        "read_input_tokens": 0,
        "input_tokens": 1200,
        "output_tokens": 1800,
    }
    assert report.metadata.sdk_version  # something non-empty
    # The .eval.md hybrid file is the only persisted scoring artifact.
    raw_path = stub.parent / "stub.eval.raw.txt"
    assert not raw_path.exists()


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
