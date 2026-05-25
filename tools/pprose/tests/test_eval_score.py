"""Tests for pprose.eval_score — the qualitative-scoring runner."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic_ai.messages import ModelMessage, ModelResponse, ToolCallPart
from pydantic_ai.models.function import AgentInfo, FunctionModel

from pprose.eval_render import render_single_doc_rollup
from pprose.eval_report import (
    EvalReport,
    ExpressionScores,
    FormScores,
    GroundingScores,
    JudgmentScores,
    Location,
    PurposeScores,
    QualScores,
    ReasoningScores,
    RuleFinding,
)
from pprose.eval_score import (
    ScoredResult,
    ScoreEntry,
    ScoringResponse,
    _to_scored_result,
    build_prompt,
    main,
    merge_into_report,
)

FIXTURES = Path(__file__).resolve().parent / "test_fixtures" / "practical_prose_metrics"


def _full_response(score: int = 4, with_violation: bool = True) -> ScoringResponse:
    """Build a ScoringResponse covering every rubric dimension at a uniform score."""
    from pprose import rubric_schema as rs

    findings: list[RuleFinding] = []
    if with_violation:
        findings = [
            RuleFinding(
                dimension="Clarity",
                rule_number=1,
                verdict="violated",
                description="x",
                locations=[Location(line_start=1)],
            )
        ]
    return ScoringResponse(
        scores={d.key: ScoreEntry(score=score, reason="test") for d in rs.DIMENSIONS},
        rule_findings=findings,
    )


# ---------------------------------------------------------------------------
# _to_scored_result (replaces the old parse_response tests)
# ---------------------------------------------------------------------------


def test_to_scored_result_full_valid():
    result = _to_scored_result(_full_response(score=5, with_violation=False))
    assert result.qual.expression.clarity == 5
    assert result.qual.judgment.robustness == 5
    assert result.rule_findings == []


def test_to_scored_result_extracts_reasons():
    """Per-dimension reason strings should flow into qual_reasons."""
    response = _full_response(score=4, with_violation=False)
    response.scores["clarity"].reason = "trite phrasing at L412"
    response.scores["depth"].reason = "scope not declared"
    result = _to_scored_result(response)
    assert result.qual_reasons.expression.clarity == "trite phrasing at L412"
    assert result.qual_reasons.purpose.depth == "scope not declared"


def test_to_scored_result_missing_dimension_raises():
    response = _full_response()
    del response.scores["depth"]
    with pytest.raises(ValueError, match="missing dimensions"):
        _to_scored_result(response)


def test_to_scored_result_unknown_dimension_raises():
    response = _full_response()
    response.scores["mystery"] = ScoreEntry(score=4, reason="x")
    with pytest.raises(ValueError, match="unknown dimension"):
        _to_scored_result(response)


def test_score_entry_rejects_out_of_range():
    """ScoreEntry's int|NA|ERR field rejects integers outside 1-5 at the structured-output boundary."""
    # Pydantic accepts any int for the int|Literal union, so we enforce the 1-5 bound
    # in _to_scored_result after the structured response arrives.
    response = _full_response()
    response.scores["clarity"] = ScoreEntry(score=9, reason="x")
    with pytest.raises(ValueError, match="out of 1-5 range"):
        _to_scored_result(response)


def test_to_scored_result_na_accepted():
    """The literal 'NA' is a valid score and round-trips into the qual block."""
    response = _full_response()
    response.scores["calibration"] = ScoreEntry(
        score="NA", reason="no probability or forecast claims"
    )
    result = _to_scored_result(response)
    assert result.qual.judgment.calibration == "NA"
    assert result.qual_reasons.judgment.calibration == "no probability or forecast claims"


def test_to_scored_result_keeps_well_formed_findings():
    response = _full_response()
    response.rule_findings = [
        RuleFinding(
            dimension="Clarity",
            rule_number=4,
            verdict="violated",
            description="register",
            locations=[Location(line_start=412, line_end=418)],
        ),
        RuleFinding(
            dimension="Soundness",
            rule_number=3,
            verdict="violated",
            description="method",
            locations=[Location(section="§2.7")],
        ),
    ]
    result = _to_scored_result(response)
    assert len(result.rule_findings) == 2
    assert result.rule_findings[0].locations[0].line_start == 412
    assert result.rule_findings[1].locations[0].section == "§2.7"


def test_to_scored_result_drops_out_of_range_rule_number(capsys):
    """The model occasionally invents a rule_number past the dimension's bound;
    the finding is dropped with a stderr warning instead of failing the eval."""
    response = _full_response(with_violation=False)
    # Build the finding via model_construct so the validator doesn't reject it
    # before _to_scored_result has a chance to filter.
    response.rule_findings = [
        RuleFinding.model_construct(
            dimension="Clarity",
            rule_number=99,
            verdict="violated",
            description="phantom rule",
            locations=[Location(line_start=1)],
        )
    ]
    result = _to_scored_result(response)
    assert result.rule_findings == []
    captured = capsys.readouterr()
    assert "out-of-range" in captured.err
    assert "rule_number=99" in captured.err


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

    assert "| **Purpose** | Suitability | ERR |" in body
    assert "|  | Scope | ERR |" in body
    assert "| Purpose | Scope |" not in body
    assert "|  | **Mean** |" in body
    assert "| **Purpose** | **Mean** |" not in body


def _all_fives_qual() -> QualScores:
    return QualScores(
        expression=ExpressionScores(clarity=5, coherence=5, concision=5),
        form=FormScores(organization=5, consistency="ERR", formatting="ERR"),
        purpose=PurposeScores(suitability=5, scope=5, breadth=5, depth=5),
        grounding=GroundingScores(verifiability=5, factuality=5, relevance=5),
        reasoning=ReasoningScores(discipline=5, soundness=5, precision=5, parsimony=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=5),
    )


def test_merge_replaces_qual_and_rule_findings(tmp_path: Path):
    stub = _stub_report(tmp_path)
    scored = ScoredResult(qual=_all_fives_qual(), rule_findings=[])
    merged = merge_into_report(stub, scored, evaluator="test-eval")

    assert merged.qual.expression.clarity == 5
    assert merged.rule_findings == []
    assert merged.violations == []
    assert merged.metadata.evaluator == "test-eval"
    # The stub note should be cleared (qual is no longer all-zero)
    assert merged.metadata.notes is None or "Stub" not in (merged.metadata.notes or "")
    # Quant block is preserved unchanged.
    assert merged.quant.headings.total == stub.quant.headings.total


def test_merge_preserves_existing_method(tmp_path: Path):
    stub = _stub_report(tmp_path)
    data = stub.model_dump(mode="json", exclude_none=True)
    data["metadata"]["method"] = "12-dim re-baseline"
    stub = EvalReport.model_validate(data)

    merged = merge_into_report(
        stub, ScoredResult(qual=_all_fives_qual(), rule_findings=[]), evaluator="x"
    )
    assert merged.metadata.method == "12-dim re-baseline"


def test_merge_alignment_clean_passes_strict_validate(tmp_path: Path):
    """Merging score-5-everywhere with no violations produces an alignment-clean report."""
    stub = _stub_report(tmp_path)
    merged = merge_into_report(
        stub, ScoredResult(qual=_all_fives_qual(), rule_findings=[]), evaluator="x"
    )
    assert merged.alignment_errors() == []


def test_merge_with_proper_violations_passes_alignment(tmp_path: Path):
    """A sub-5 score with a matching violation is alignment-valid after merge."""
    stub = _stub_report(tmp_path)
    qual = QualScores(
        expression=ExpressionScores(clarity=4, coherence=5, concision=5),
        form=FormScores(organization=5, consistency="ERR", formatting="ERR"),
        purpose=PurposeScores(suitability=5, scope=5, breadth=5, depth=5),
        grounding=GroundingScores(verifiability=5, factuality=5, relevance=5),
        reasoning=ReasoningScores(discipline=5, soundness=5, precision=5, parsimony=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=5),
    )
    rule_findings = [
        RuleFinding(
            dimension="Clarity",
            rule_number=4,
            verdict="violated",
            description="x",
            locations=[Location(line_start=1)],
        )
    ]
    merged = merge_into_report(
        stub, ScoredResult(qual=qual, rule_findings=rule_findings), evaluator="x"
    )
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
    # Pydantic AI provides the structured-output schema; the prompt should
    # mention ScoringResponse so the model knows what it's filling.
    assert "ScoringResponse" in prompt


def test_build_prompt_is_schema_derived():
    """The dimension list and key count are generated from the schema, not hard-coded."""
    import pprose.rubric_schema as rs

    prompt = build_prompt(FIXTURES / "all_headings.md")
    # No unsubstituted placeholders leak into the rendered prompt.
    for placeholder in ("{{CANONICAL_NAMES}}", "{{DIMENSION_COUNT}}"):
        assert placeholder not in prompt, f"unsubstituted placeholder: {placeholder}"
    # Every label appears in the canonical-name list.
    for dim in rs.DIMENSIONS:
        assert dim.label in prompt, f"missing label {dim.label}"
    # The hard-coded count matches the schema.
    assert f"all {rs.dimension_count()} keys present" in prompt


def test_build_prompt_missing_artifact_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        build_prompt(tmp_path / "does-not-exist.md")


# ---------------------------------------------------------------------------
# _resolve_model
# ---------------------------------------------------------------------------


def test_resolve_model_handles_aliases_and_full_ids():
    from pprose.eval_score import _resolve_model

    # Empty / None is rejected: every scoring call must explicitly pick a model.
    with pytest.raises(ValueError, match="model is required"):
        _resolve_model("")
    with pytest.raises(ValueError, match="model is required"):
        _resolve_model(None)  # pyright: ignore[reportArgumentType]
    # Short aliases resolve to provider-prefixed strings.
    assert _resolve_model("opus") == "anthropic:claude-opus-4-7"
    assert _resolve_model("sonnet") == "anthropic:claude-sonnet-4-6"
    assert _resolve_model("haiku") == "anthropic:claude-haiku-4-5"
    assert _resolve_model("gpt") == "openai:gpt-5.5"
    assert _resolve_model("gpt-mini") == "openai:gpt-5.4-mini"
    assert _resolve_model("gemini") == "google:gemini-3.5-flash"
    # Bare claude-* IDs get the anthropic: prefix auto-applied.
    assert _resolve_model("claude-opus-4-7-20251015") == "anthropic:claude-opus-4-7-20251015"
    # Provider-prefixed strings pass through unchanged.
    assert _resolve_model("anthropic:claude-sonnet-4-6") == "anthropic:claude-sonnet-4-6"
    assert _resolve_model("openai:gpt-5.2") == "openai:gpt-5.2"
    assert _resolve_model("google:gemini-3-pro-preview") == "google:gemini-3-pro-preview"


def test_list_models_includes_all_providers(capsys):
    """`pprose score --list-models` prints suggestions covering anthropic/openai/google."""
    rc = main(["--list-models"])
    assert rc == 0
    out = capsys.readouterr().out
    # At least one model from each provider extra appears.
    assert "anthropic:claude-opus-4-7" in out
    assert "openai:gpt-5.5" in out
    assert "google:gemini-3.5-flash" in out


def test_main_without_model_errors():
    """Scoring without --model exits non-zero with a helpful message."""
    rc = main(["some/path.eval.md"])
    assert rc != 0


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
        expression=ExpressionScores(clarity=4, coherence=5, concision=4),
        form=FormScores(organization=5, consistency=4, formatting=5),
        purpose=PurposeScores(suitability=4, scope=4, breadth=4, depth=4),
        grounding=GroundingScores(verifiability=5, factuality=4, relevance=5),
        reasoning=ReasoningScores(discipline=4, soundness=5, precision=4, parsimony=5),
        judgment=JudgmentScores(calibration=5, fairness=5, robustness=4),
    )
    sub5_dims = [
        "Clarity",
        "Concision",
        "Consistency",
        "Suitability",
        "Scope",
        "Breadth",
        "Depth",
        "Factuality",
        "Discipline",
        "Precision",
        "Robustness",
    ]
    rule_findings = [
        RuleFinding(
            dimension=d,
            rule_number=1,
            verdict="violated",
            description="x",
            locations=[Location(line_start=1)],
        )
        for d in sub5_dims
    ]
    merged = merge_into_report(
        stub, ScoredResult(qual=qual, rule_findings=rule_findings), evaluator="round-trip"
    )

    out_path = tmp_path / "merged.eval.md"
    body = render_single_doc_rollup(merged, heading_level=1)
    out_path.write_text(merged.to_eval_md(body), encoding="utf-8")
    reloaded = EvalReport.from_eval_md(out_path)

    assert reloaded.qual.expression.clarity == 4
    assert reloaded.qual.expression.coherence == 5
    assert len(reloaded.violations) == 11
    assert reloaded.metadata.evaluator == "round-trip"
    assert reloaded.metadata.status == "complete"
    assert reloaded.alignment_errors() == []


def test_merge_populates_reproducibility_metadata(tmp_path: Path):
    """A ReproContext flows through merge_into_report into metadata.*"""
    from pprose.eval_score import ReproContext

    stub = _stub_report(tmp_path)
    repro = ReproContext(
        model="anthropic:claude-opus-4-7",
        command="pprose score /tmp/x.eval.md",
        prompt_sha256="a" * 64,
        rubric_sha256="b" * 64,
        guidelines_sha256="c" * 64,
        artifact_sha256="d" * 64,
    )
    merged = merge_into_report(
        stub,
        ScoredResult(qual=_all_fives_qual(), rule_findings=[]),
        evaluator="test",
        repro=repro,
    )
    assert merged.metadata.model == "anthropic:claude-opus-4-7"
    assert merged.metadata.command == "pprose score /tmp/x.eval.md"
    assert merged.metadata.prompt_sha256 == "a" * 64
    assert merged.metadata.rubric_sha256 == "b" * 64
    assert merged.metadata.guidelines_sha256 == "c" * 64
    assert merged.metadata.artifact_sha256 == "d" * 64


def test_repro_context_persists_pydantic_ai_cache_keys(tmp_path: Path):
    """cache_stats now mirror Pydantic AI's RunUsage shape (cache_write_tokens / cache_read_tokens)."""
    from pprose.eval_score import ReproContext

    stub = _stub_report(tmp_path)
    repro = ReproContext(
        model="opus",
        model_id="claude-opus-4-7",
        sdk_version="1.93.0",
        cache_stats={
            "cache_write_tokens": 99000,
            "cache_read_tokens": 0,
            "input_tokens": 1200,
            "output_tokens": 1800,
        },
    )
    merged = merge_into_report(
        stub,
        ScoredResult(qual=_all_fives_qual(), rule_findings=[]),
        evaluator="test",
        repro=repro,
    )
    assert merged.metadata.model == "opus"
    assert merged.metadata.model_id == "claude-opus-4-7"
    assert merged.metadata.sdk_version == "1.93.0"
    assert merged.metadata.cache_stats == {
        "cache_write_tokens": 99000,
        "cache_read_tokens": 0,
        "input_tokens": 1200,
        "output_tokens": 1800,
    }


# ---------------------------------------------------------------------------
# End-to-end score path using Pydantic AI's FunctionModel
# (replaces the old _FakeAnthropic-based tests; no API calls)
# ---------------------------------------------------------------------------


def _make_function_model(response: ScoringResponse) -> FunctionModel:
    """
    Build a FunctionModel that always returns `response` as the structured output.

    Pydantic AI calls the function on each request; we look up the
    structured-output tool name from `info.output_tools` and emit a ToolCallPart
    with our payload. This lets us exercise the real Agent code path (including
    output validation) without an API call.
    """

    def _call(_messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        assert info.output_tools, "Agent was not configured with output_type"
        tool_name = info.output_tools[0].name
        return ModelResponse(
            parts=[ToolCallPart(tool_name=tool_name, args=response.model_dump())]
        )

    return FunctionModel(_call)


def test_call_scorer_returns_structured_output(monkeypatch):
    """
    call_scorer routes through the Agent and returns a CallResult with the
    structured output. Uses Agent.override to swap in a FunctionModel.
    """
    from pprose import eval_score
    from pprose.eval_score import _build_agent, call_scorer

    # The real Anthropic provider is constructed before override kicks in, so
    # it demands a key; the value is never used because the FunctionModel
    # override takes over for the actual call.
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-fake")

    response = _full_response(score=5, with_violation=False)

    # Wrap _build_agent so the override context stays active for the duration
    # of this test (the override is undone when the agent is garbage-collected;
    # holding a reference on the test scope keeps it alive).
    original_build = _build_agent
    overrides: list = []

    def wrapped_build(model: str):
        agent = original_build(model)
        ctx = agent.override(model=_make_function_model(response))
        ctx.__enter__()
        overrides.append(ctx)
        return agent

    monkeypatch.setattr(eval_score, "_build_agent", wrapped_build)

    try:
        result = call_scorer("artifact body", model="opus")
        assert result.output.scores["clarity"].score == 5
        assert result.output.rule_findings == []
    finally:
        for ctx in overrides:
            ctx.__exit__(None, None, None)


def test_main_end_to_end_writes_filled_report(tmp_path: Path, monkeypatch):
    """
    Full main() path with the LLM mocked.

    Replaces `call_scorer` with a stub returning a fixed CallResult so we
    exercise prep -> _to_scored_result -> merge -> render -> write end-to-end
    without an API call. Verifies the YAML is filled and repro metadata is set.
    """
    from pprose import eval_score
    from pprose.eval_report import main as report_main
    from pprose.eval_score import CallResult

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

    response = _full_response(score=5, with_violation=False)
    fake_call_result = CallResult(
        output=response,
        model_id="claude-opus-4-7-fake",
        cache_write_tokens=99000,
        cache_read_tokens=0,
        input_tokens=1200,
        output_tokens=1800,
    )

    monkeypatch.setattr(eval_score, "call_scorer", lambda _artifact, *, model: fake_call_result)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-fake")

    rc = main([str(stub), "--model", "opus"])
    assert rc == 0

    report = EvalReport.from_eval_md(stub)
    assert report.metadata.status == "complete"
    assert report.metadata.model == "opus"
    assert report.metadata.model_id == "claude-opus-4-7-fake"
    assert report.qual.expression.clarity == 5
    assert report.metadata.cache_stats == {
        "cache_write_tokens": 99000,
        "cache_read_tokens": 0,
        "input_tokens": 1200,
        "output_tokens": 1800,
    }
    # The .eval.md hybrid file is the only persisted scoring artifact.
    assert not (stub.parent / "stub.eval.raw.txt").exists()
