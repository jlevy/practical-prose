"""Tests for pprose.eval_report — Pydantic eval report schema."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from pprose import rubric_schema as rs
from pprose.eval_report import (
    EvalReport,
    QualScores,
    QuantMetrics,
    compute_derived,
)


def _miss(
    dimension: str,
    rule_number: int = 1,
    description: str = "x",
    verdict: str = "violated",
) -> dict:
    """Construct a minimally-valid miss RuleFinding dict for tests."""
    return {
        "dimension": dimension,
        "rule_number": rule_number,
        "verdict": verdict,
        "description": description,
        "locations": [{"note": "stub location"}],
    }


def _write_eval_md(path: Path, data: dict) -> None:
    """Write a dict to `path` as a minimal .eval.md (frontmatter, empty body).

    Tests construct dicts directly without going through the renderer; this
    helper wraps them in `---` delimiters so `EvalReport.from_eval_md` accepts
    them. The body is left empty since these tests verify the frontmatter only.
    """
    path.write_text(f"---\n{yaml.safe_dump(data)}---\n", encoding="utf-8")


def _minimal_quant() -> dict:
    return {
        "size": {
            "words": 1000,
            "sentences": 50,
            "paragraphs": 25,
            "lines": 200,
            "pages_275wpp": 3.6,
        },
        "headings": {
            "h1": 1,
            "h2": 4,
            "h3": 10,
            "h4": 5,
            "total": 20,
        },
        "structural": {"tables": 4, "code_blocks": 0, "images": 0},
        "links": {
            "total": 10,
            "external": 6,
            "internal": 4,
            "inline": 10,
            "reference": 0,
            "autolink": 0,
            "bare_urls": 0,
        },
        "provenance": {"bracket_tags": 8, "footnote_refs": 0, "footnote_defs": 0},
        "lint": {"banned_register_hits": 0},
    }


def _minimal_qual() -> dict:
    return {
        "expression": {
            "clarity": 4,
            "coherence": 5,
            "concision": 4,
        },
        "form": {
            "organization": 5,
            "consistency": 4,
            "formatting": 5,
        },
        "purpose": {
            "suitability": 4,
            "scope": 4,
            "breadth": 4,
            "depth": 4,
        },
        "grounding": {
            "verifiability": 5,
            "factuality": 4,
            "relevance": 5,
        },
        "reasoning": {
            "discipline": 4,
            "soundness": 5,
            "precision": 4,
            "parsimony": 5,
        },
        "judgment": {"calibration": 5, "fairness": 5, "robustness": 4},
    }


def _minimal_report_dict() -> dict:
    return {
        "artifact": {"label": "TEST", "path": "test.md"},
        "quant": _minimal_quant(),
        "qual": _minimal_qual(),
        "metadata": {"eval_date": "2026-05-07", "evaluator": "pytest"},
    }


def test_load_minimal_yaml_populates_derived():
    data = _minimal_report_dict()
    report = EvalReport.model_validate(data)
    assert report.derived is not None
    assert report.derived.rubric_rollup.overall_mean == pytest.approx(
        sum(report.qual.all_scores()) / len(report.qual.all_scores()), abs=0.01
    )
    # Group means recomputed correctly.
    # Expression: 4+5+4 = 13 / 3 ≈ 4.333
    assert report.derived.rubric_rollup.expression_mean == pytest.approx(13 / 3, abs=0.01)
    # Form: 5+4+5 = 14 / 3 ≈ 4.667
    assert report.derived.rubric_rollup.form_mean == pytest.approx(14 / 3, abs=0.01)
    # Purpose: 4+4+4+4 = 16 / 4 = 4.0
    assert report.derived.rubric_rollup.purpose_mean == pytest.approx(4.0, abs=0.01)
    # Grounding: 5+4+5 = 14 / 3 ≈ 4.667
    assert report.derived.rubric_rollup.grounding_mean == pytest.approx(14 / 3, abs=0.01)
    # Reasoning: 4+5+4+5 = 18 / 4 = 4.5
    assert report.derived.rubric_rollup.reasoning_mean == pytest.approx(4.5, abs=0.01)
    # Judgment: 5+5+4 = 14 / 3 ≈ 4.667
    assert report.derived.rubric_rollup.judgment_mean == pytest.approx(14 / 3, abs=0.01)


def test_score_too_high_rejected():
    data = _minimal_report_dict()
    data["qual"]["expression"]["clarity"] = 6
    with pytest.raises(Exception):
        EvalReport.model_validate(data)


def test_missing_dimension_rejected():
    data = _minimal_report_dict()
    del data["qual"]["reasoning"]["discipline"]
    with pytest.raises(Exception):
        EvalReport.model_validate(data)


def test_unknown_field_rejected():
    data = _minimal_report_dict()
    data["qual"]["expression"]["mystery_dim"] = 5
    with pytest.raises(Exception):
        EvalReport.model_validate(data)


def test_headings_total_inconsistent_rejected():
    data = _minimal_report_dict()
    data["quant"]["headings"]["total"] = 99
    with pytest.raises(Exception):
        EvalReport.model_validate(data)


def test_literal_zero_rejected_when_rubric_version_is_current():
    """v2+ rubric: a literal `score: 0` fails validation (no migration fires)."""
    data = _minimal_report_dict()
    data["metadata"]["rubric_version"] = rs.RUBRIC_VERSION
    data["qual"]["expression"]["clarity"] = 0
    with pytest.raises(Exception):
        EvalReport.model_validate(data)


def test_err_excluded_from_rollup_means():
    """ERR scores ('scorer could not assess') should not drag down group/overall means."""
    data = _minimal_report_dict()
    # Start from a clean score-5-everywhere baseline, then mark clarity as ERR.
    for group in data["qual"].values():
        for dim in group:
            group[dim] = 5
    data["qual"]["expression"]["clarity"] = "ERR"
    report = EvalReport.model_validate(data)
    assert report.derived is not None
    rollup = report.derived.rubric_rollup
    # Expression mean is over coherence/concision (clarity excluded).
    assert rollup.expression_mean == 5.0
    assert rollup.overall_mean == 5.0
    # All but one dimension were assessed (clarity is ERR).
    assert rollup.assessed_dimensions == rs.dimension_count() - 1
    assert rollup.err_dimensions == 1
    assert rollup.na_dimensions == 0


def test_err_and_na_counted_separately_in_rollup():
    """err_dimensions and na_dimensions are independent counters."""
    data = _minimal_report_dict()
    for group in data["qual"].values():
        for dim in group:
            group[dim] = 5
    data["qual"]["expression"]["clarity"] = "ERR"
    data["qual"]["judgment"]["calibration"] = "NA"
    report = EvalReport.model_validate(data)
    assert report.derived is not None
    rollup = report.derived.rubric_rollup
    assert rollup.err_dimensions == 1
    assert rollup.na_dimensions == 1
    assert rollup.assessed_dimensions == rs.dimension_count() - 2


def test_all_err_stub_has_zero_assessed_dimensions():
    """The from-metrics all-ERR stub should report 0 assessed dimensions, mean 0.0."""
    data = _minimal_report_dict()
    for group in data["qual"].values():
        for dim in group:
            group[dim] = "ERR"
    report = EvalReport.model_validate(data)
    assert report.derived is not None
    assert report.derived.rubric_rollup.assessed_dimensions == 0
    assert report.derived.rubric_rollup.err_dimensions == rs.dimension_count()
    assert report.derived.rubric_rollup.overall_mean == 0.0


def test_round_trip_yaml():
    """Pure YAML round-trip (no .eval.md frontmatter), used to verify model_dump
    is stable across reloads. Distinct from the .eval.md round-trip elsewhere."""
    data = _minimal_report_dict()
    original = EvalReport.model_validate(data)
    text = original.to_yaml()
    reloaded = EvalReport.from_yaml(text)
    # Two dumps should be byte-identical (canonical form).
    assert original.to_yaml() == reloaded.to_yaml()


def test_derived_consistency_check_passes_when_correct():
    quant = QuantMetrics.model_validate(_minimal_quant())
    qual = QualScores.model_validate(_minimal_qual())
    derived = compute_derived(quant, qual)

    data = _minimal_report_dict()
    data["derived"] = derived.model_dump(mode="json")
    EvalReport.model_validate(data)


def test_derived_inconsistency_rejected():
    quant = QuantMetrics.model_validate(_minimal_quant())
    qual = QualScores.model_validate(_minimal_qual())
    derived = compute_derived(quant, qual).model_dump(mode="json")
    derived["rubric_rollup"]["overall_mean"] = 1.0  # bogus

    data = _minimal_report_dict()
    data["derived"] = derived
    with pytest.raises(Exception, match="inconsistent"):
        EvalReport.model_validate(data)


def test_rule_findings_default_empty():
    data = _minimal_report_dict()
    report = EvalReport.model_validate(data)
    assert report.rule_findings == []
    assert report.violations == []


def test_rule_finding_field_validation():
    data = _minimal_report_dict()
    data["rule_findings"] = [
        {
            "dimension": "Concision",
            "rule_number": 2,
            "verdict": "violated",
            "description": "duplicated fact across §1.3 and §2.1",
            "locations": [{"section": "§1.3", "quote": "duplicated fact"}],
        }
    ]
    report = EvalReport.model_validate(data)
    assert len(report.rule_findings) == 1
    assert report.rule_findings[0].dimension == "Concision"
    assert report.rule_findings[0].rule_number == 2
    # The violations convenience view surfaces misses only.
    assert len(report.violations) == 1
    assert report.violations[0].dimension == "Concision"


def test_location_requires_at_least_one_anchor():
    """A Location without any of quote / section / line_start / note is rejected."""
    data = _minimal_report_dict()
    data["rule_findings"] = [
        {
            "dimension": "Concision",
            "rule_number": 2,
            "verdict": "violated",
            "description": "x",
            "locations": [{}],
        }
    ]
    with pytest.raises(ValidationError, match="at least one anchor"):
        EvalReport.model_validate(data)


def test_miss_finding_locations_optional():
    """
    A violated/partial finding with no locations is accepted (whole-doc findings).

    There is a TODO in eval_report to tighten this once the scorer reliably emits
    a Location for every miss; for now the validator only enforces structure.
    """
    data = _minimal_report_dict()
    data["rule_findings"] = [
        {
            "dimension": "Concision",
            "rule_number": 2,
            "verdict": "violated",
            "description": "x",
            "locations": [],
        }
    ]
    report = EvalReport.model_validate(data)
    assert report.rule_findings[0].locations == []
    # Surfaces in the .violations view because verdict is a miss.
    assert len(report.violations) == 1


def test_met_finding_can_omit_location():
    """A met / na finding does not need locations — there is nothing to look up."""
    data = _minimal_report_dict()
    data["rule_findings"] = [
        {
            "dimension": "Coherence",
            "rule_number": 1,
            "verdict": "met",
            "description": "Clean topic sentences throughout.",
        }
    ]
    report = EvalReport.model_validate(data)
    assert report.rule_findings[0].verdict == "met"
    # `met` findings are not surfaced via the violations view.
    assert report.violations == []


def test_density_ratios_correct():
    data = _minimal_report_dict()
    report = EvalReport.model_validate(data)
    # words=1000, sentences=50 → 20.0 wps
    assert report.derived.density.words_per_sentence == pytest.approx(20.0)
    # words=1000, paragraphs=25 → 40.0 wpp
    assert report.derived.density.words_per_paragraph == pytest.approx(40.0)
    # tables=4 per 1000 words = 4.0 tables/1k
    assert report.derived.density.tables_per_1k_words == pytest.approx(4.0)
    # bracket_tags=8 per 1000 words = 8.0 tags/1k
    assert report.derived.density.tags_per_1k_words == pytest.approx(8.0)


def test_h4_share_of_headings():
    data = _minimal_report_dict()
    report = EvalReport.model_validate(data)
    # h4=5, total=20 → 0.25
    assert report.derived.structure.h4_share_of_headings == pytest.approx(0.25)


def test_tally_compact_handles_none():
    data = _minimal_report_dict()
    report = EvalReport.model_validate(data)
    assert report.derived.tally is None


def test_load_from_yaml_path(tmp_path: Path):
    data = _minimal_report_dict()
    path = tmp_path / "test.eval.md"
    _write_eval_md(path, data)
    report = EvalReport.from_eval_md(path)
    assert report.artifact.label == "TEST"


def test_validate_cli(tmp_path: Path):
    from pprose.eval_report import main

    data = _minimal_report_dict()
    path = tmp_path / "test.eval.md"
    _write_eval_md(path, data)
    # Minimal report has multiple sub-5 scores with no violations cited; bypass strict
    # alignment to test the schema-validation path on its own.
    rc = main(["validate", str(path), "--allow-misalignment"])
    assert rc == 0


def test_validate_cli_failure(tmp_path: Path):
    from pprose.eval_report import main

    path = tmp_path / "bad.eval.md"
    path.write_text("artifact:\n  label: X\n", encoding="utf-8")
    rc = main(["validate", str(path)])
    assert rc != 0


def test_compute_derived_cli_in_place(tmp_path: Path):
    from pprose.eval_report import main

    data = _minimal_report_dict()
    path = tmp_path / "test.eval.md"
    _write_eval_md(path, data)
    rc = main(["compute-derived", str(path), "--in-place"])
    assert rc == 0
    reloaded = EvalReport.from_eval_md(path)
    assert reloaded.derived is not None
    assert reloaded.derived.rubric_rollup is not None


# ---------------------------------------------------------------------------
# B8: from-metrics subcommand
# ---------------------------------------------------------------------------


FIXTURES = Path(__file__).resolve().parent / "test_fixtures" / "practical_prose_metrics"


def test_from_metrics_round_trip(tmp_path: Path):
    """from-metrics output validates and round-trips through the schema."""
    from pprose.eval_report import EvalReport, main

    out_path = tmp_path / "fixture.eval.md"
    rc = main(
        [
            "from-metrics",
            str(FIXTURES / "all_headings.md"),
            "--label",
            "all-headings",
            "--out",
            str(out_path),
        ]
    )
    assert rc == 0
    assert out_path.exists()

    # The output must validate cleanly.
    report = EvalReport.from_eval_md(out_path)
    assert report.artifact.label == "all-headings"
    assert report.metadata.evaluator == "TODO"
    # Stub qual is all ERR (scorer could not assess yet).
    assert all(s == "ERR" for s in report.qual.all_scores())
    # Quant block is populated from the metrics script.
    assert report.quant.headings.total == 8
    assert report.quant.headings.h1 == 2


def test_from_metrics_emits_optional_table_style_metadata(tmp_path: Path):
    from pprose.eval_report import main

    out_path = tmp_path / "fixture.eval.md"
    rc = main(
        [
            "from-metrics",
            str(FIXTURES / "all_headings.md"),
            "--label",
            "all-headings",
            "--out",
            str(out_path),
        ]
    )
    assert rc == 0

    frontmatter = yaml.safe_load(out_path.read_text(encoding="utf-8").split("---", 2)[1])
    table_styles = frontmatter["display"]["table_styles"]
    assert table_styles["version"] == 1
    assert any(
        table["id"] == "practical_prose_single_doc_qualitative" for table in table_styles["tables"]
    )


def test_from_metrics_quant_mapping_matches_metrics_script(tmp_path: Path):
    """Verify the rename/regroup in quant_from_metrics is correct end-to-end."""
    from pprose import metrics as pwm
    from pprose.eval_report import quant_from_metrics

    metrics = pwm.measure(FIXTURES / "links_mixed.md")
    quant = quant_from_metrics(metrics)

    # Field renames (B2 mapping).
    assert quant.size.pages_275wpp == metrics.pages
    assert quant.links.reference == metrics.links_reference_use
    assert quant.provenance.footnote_refs == metrics.footnote_references
    assert quant.provenance.footnote_defs == metrics.footnote_definitions

    # Regrouping.
    assert quant.structural.images == metrics.images
    assert quant.lint.banned_register_hits == metrics.banned_register_hits

    # Headings total reconstructed.
    assert quant.headings.total == metrics.headings_total


def test_from_metrics_default_label_is_file_stem(tmp_path: Path):
    from pprose.eval_report import EvalReport, main

    out_path = tmp_path / "out.eval.md"
    rc = main(
        [
            "from-metrics",
            str(FIXTURES / "links_mixed.md"),
            "--out",
            str(out_path),
        ]
    )
    assert rc == 0
    report = EvalReport.from_eval_md(out_path)
    assert report.artifact.label == "links_mixed"


def test_from_metrics_records_optional_fields(tmp_path: Path):
    from pprose.eval_report import EvalReport, main

    out_path = tmp_path / "out.eval.md"
    rc = main(
        [
            "from-metrics",
            str(FIXTURES / "all_headings.md"),
            "--evaluator",
            "test-runner",
            "--method",
            "subagent",
            "--commit-sha",
            "abc123",
            "--out",
            str(out_path),
        ]
    )
    assert rc == 0
    report = EvalReport.from_eval_md(out_path)
    assert report.metadata.evaluator == "test-runner"
    assert report.metadata.method == "subagent"
    assert report.artifact.commit_sha == "abc123"


def test_from_metrics_missing_file_returns_error(tmp_path: Path):
    from pprose.eval_report import main

    rc = main(["from-metrics", str(tmp_path / "does-not-exist.md")])
    assert rc == 1


# ---------------------------------------------------------------------------
# B13: scope_class on ArtifactMeta
# ---------------------------------------------------------------------------


def test_scope_class_optional_default_none():
    data = _minimal_report_dict()
    report = EvalReport.model_validate(data)
    assert report.artifact.scope_class is None


def test_scope_class_accepts_canonical_values():
    for v in ("status", "brief", "memo", "deep_research", "design_doc"):
        data = _minimal_report_dict()
        data["artifact"]["scope_class"] = v
        report = EvalReport.model_validate(data)
        assert report.artifact.scope_class == v


def test_scope_class_rejects_unknown():
    data = _minimal_report_dict()
    data["artifact"]["scope_class"] = "novel"  # not in the enum
    with pytest.raises(Exception):
        EvalReport.model_validate(data)


def test_from_metrics_records_scope_class(tmp_path: Path):
    from pprose.eval_report import EvalReport, main

    out_path = tmp_path / "out.eval.md"
    rc = main(
        [
            "from-metrics",
            str(FIXTURES / "all_headings.md"),
            "--scope-class",
            "deep_research",
            "--out",
            str(out_path),
        ]
    )
    assert rc == 0
    report = EvalReport.from_eval_md(out_path)
    assert report.artifact.scope_class == "deep_research"


# ---------------------------------------------------------------------------
# B12: density-ratio concerns
# ---------------------------------------------------------------------------


class TestB12_DensityConcerns:
    def test_untagged_returns_no_concerns(self):
        """Without scope_class, density is diagnostic-only — no concerns surfaced."""
        data = _minimal_report_dict()
        # Minimal has 10 links over 1000 words → 10/1k → would not flag anyway, but
        # the point is scope_class=None bypasses all checks.
        report = EvalReport.model_validate(data)
        assert report.density_concerns() == []

    def test_low_link_density_flagged_for_deep_research(self):
        data = _minimal_report_dict()
        data["artifact"]["scope_class"] = "deep_research"
        # Drop link total to below the 1.0/1k threshold (0 links / 1000 words = 0.0)
        data["quant"]["links"]["total"] = 0
        data["quant"]["links"]["external"] = 0
        data["quant"]["links"]["internal"] = 0
        data["quant"]["links"]["inline"] = 0
        report = EvalReport.model_validate(data)
        concerns = report.density_concerns()
        assert any("link density" in c for c in concerns)

    def test_status_class_does_not_flag_low_links(self):
        """Status updates legitimately have low link density."""
        data = _minimal_report_dict()
        data["artifact"]["scope_class"] = "status"
        data["quant"]["links"]["total"] = 0
        data["quant"]["links"]["external"] = 0
        data["quant"]["links"]["internal"] = 0
        data["quant"]["links"]["inline"] = 0
        report = EvalReport.model_validate(data)
        # Status has no thresholds defined → no concerns
        assert report.density_concerns() == []

    def test_high_density_passes_for_deep_research(self):
        data = _minimal_report_dict()
        data["artifact"]["scope_class"] = "deep_research"
        # Minimal has 10 links / 1000 words = 10.0 — well above 1.0 threshold
        report = EvalReport.model_validate(data)
        assert not any("link density" in c for c in report.density_concerns())

    def test_low_table_density_flagged_for_deep_research(self):
        data = _minimal_report_dict()
        data["artifact"]["scope_class"] = "deep_research"
        # 0 tables / 1000 words = 0.0 < 0.3 threshold
        data["quant"]["structural"]["tables"] = 0
        report = EvalReport.model_validate(data)
        assert any("table density" in c for c in report.density_concerns())


# ---------------------------------------------------------------------------
# B6: rubric_version field
# ---------------------------------------------------------------------------


def test_rubric_version_optional_default_none():
    """Existing YAMLs without rubric_version still validate."""
    data = _minimal_report_dict()
    report = EvalReport.model_validate(data)
    assert report.metadata.rubric_version is None


def test_rubric_version_preserved_when_set():
    data = _minimal_report_dict()
    data["metadata"]["rubric_version"] = "12-dim-v1"
    report = EvalReport.model_validate(data)
    assert report.metadata.rubric_version == "12-dim-v1"


def test_from_metrics_writes_current_rubric_version(tmp_path: Path):
    from pprose.eval_report import CURRENT_RUBRIC_VERSION, EvalReport, main

    out_path = tmp_path / "out.eval.md"
    rc = main(
        [
            "from-metrics",
            str(FIXTURES / "all_headings.md"),
            "--out",
            str(out_path),
        ]
    )
    assert rc == 0
    report = EvalReport.from_eval_md(out_path)
    assert report.metadata.rubric_version == CURRENT_RUBRIC_VERSION


def test_from_metrics_custom_rubric_version(tmp_path: Path):
    from pprose.eval_report import EvalReport, main

    out_path = tmp_path / "out.eval.md"
    rc = main(
        [
            "from-metrics",
            str(FIXTURES / "all_headings.md"),
            "--rubric-version",
            "15-dim-v2",
            "--out",
            str(out_path),
        ]
    )
    assert rc == 0
    report = EvalReport.from_eval_md(out_path)
    assert report.metadata.rubric_version == "15-dim-v2"


# ---------------------------------------------------------------------------
# B10: alignment property validator
# ---------------------------------------------------------------------------


class TestB10_AlignmentProperty:
    def test_score_below_5_without_violation_is_misaligned(self):
        data = _minimal_report_dict()
        # Minimal qual has clarity=4 with no violations cited → misaligned
        report = EvalReport.model_validate(data)
        errors = report.alignment_errors()
        # Multiple sub-5 dims with no violations cited
        assert any("Clarity" in e for e in errors)
        assert any("score=4" in e for e in errors)

    def test_score_below_5_with_matching_violation_is_aligned(self):
        data = _minimal_report_dict()
        # Minimal has clarity=4, coherence=5, concision=4, organization=5,
        # consistency=4, formatting=5, suitability=4, scope=4, breadth=4, depth=4,
        # verifiability=5, factuality=4, discipline=4, soundness=5,
        # precision=4, calibration=5, fairness=5, robustness=4. Add a violation per <5 dim.
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
        data["rule_findings"] = [_miss(d) for d in sub5_dims]
        report = EvalReport.model_validate(data)
        assert report.alignment_errors() == []

    def test_score_5_with_violation_is_misaligned(self):
        data = _minimal_report_dict()
        # Add a miss citing Coherence (which is scored 5)
        data["rule_findings"] = [_miss("Coherence")]
        report = EvalReport.model_validate(data)
        errors = report.alignment_errors()
        assert any("Coherence" in e and "score=5" in e for e in errors)

    def test_err_does_not_require_violation(self):
        """ERR means scorer-could-not-assess; outside the alignment property."""
        data = _minimal_report_dict()
        data["qual"]["expression"]["clarity"] = "ERR"
        report = EvalReport.model_validate(data)
        # Filtering: errors should not mention Clarity (score ERR)
        errors = report.alignment_errors()
        assert not any("Clarity" in e for e in errors)

    def test_dimension_name_must_be_canonical(self):
        """
        RuleFinding.dimension uses canonical labels — case variants are rejected.

        Replaces the prior case-insensitive policy. Canonical names must match exactly
        so unknown / lookalike dimensions can't sneak past alignment_errors().
        """
        data = _minimal_report_dict()
        data["rule_findings"] = [_miss("clarity")]
        with pytest.raises(ValidationError):
            EvalReport.model_validate(data)

    def test_canonical_dimension_names_validate(self):
        """All canonical names (from the rubric schema) are accepted as-is."""
        data = _minimal_report_dict()
        data["rule_findings"] = [
            _miss(name)
            for name in (
                "Clarity",
                "Concision",
                "Suitability",
                "Breadth",
                "Depth",
                "Organization",
                "Consistency",
                "Formatting",
                "Factuality",
                "Discipline",
                "Precision",
                "Robustness",
            )
        ]
        report = EvalReport.model_validate(data)
        # alignment_errors will report mismatches against the minimal report's scores;
        # the point of this test is just that the canonical names validate.
        assert isinstance(report.alignment_errors(), list)

    def test_unknown_dimension_rejected(self):
        """A 'Bogus' dimension can't slip past the validator."""
        data = _minimal_report_dict()
        data["rule_findings"] = [_miss("Bogus")]
        with pytest.raises(ValidationError):
            EvalReport.model_validate(data)

    def test_rule_number_out_of_range_rejected(self):
        """Rule 99 cited under Clarity (which has < 99 rules) must be rejected."""
        data = _minimal_report_dict()
        data["rule_findings"] = [_miss("Clarity", rule_number=99)]
        with pytest.raises(ValidationError):
            EvalReport.model_validate(data)

    def test_rule_number_zero_rejected(self):
        """rule_number=0 must be rejected; rules are 1-indexed."""
        data = _minimal_report_dict()
        data["rule_findings"] = [_miss("Clarity", rule_number=0)]
        with pytest.raises(ValidationError):
            EvalReport.model_validate(data)

    def test_validate_cli_strict_by_default_rejects_misaligned(self, tmp_path: Path):
        from pprose.eval_report import main

        data = _minimal_report_dict()  # clarity=4 with no violations
        path = tmp_path / "test.eval.md"
        _write_eval_md(path, data)
        rc = main(["validate", str(path)])
        assert rc != 0

    def test_validate_cli_allow_misalignment_passes(self, tmp_path: Path):
        from pprose.eval_report import main

        data = _minimal_report_dict()
        path = tmp_path / "test.eval.md"
        _write_eval_md(path, data)
        rc = main(["validate", str(path), "--allow-misalignment"])
        assert rc == 0

    def test_validate_complete_rejects_all_zero_stub(self, tmp_path: Path):
        """validate --complete should reject the from-metrics all-zero stub."""
        from pprose.eval_report import main

        out_path = tmp_path / "stub.eval.md"
        rc = main(
            [
                "from-metrics",
                str(FIXTURES / "all_headings.md"),
                "--out",
                str(out_path),
            ]
        )
        assert rc == 0
        rc = main(["validate", str(out_path), "--complete"])
        assert rc != 0

    def test_validate_complete_rejects_evaluator_todo(self, tmp_path: Path):
        """validate --complete should reject evaluator='TODO'."""
        from pprose.eval_report import main

        data = _minimal_report_dict()
        data["metadata"]["evaluator"] = "TODO"
        data["metadata"]["status"] = "complete"
        path = tmp_path / "test.eval.md"
        _write_eval_md(path, data)
        rc = main(["validate", str(path), "--complete", "--allow-misalignment"])
        assert rc != 0

    def test_validate_complete_rejects_draft_status(self, tmp_path: Path):
        """validate --complete should reject status='draft'."""
        from pprose.eval_report import main

        data = _minimal_report_dict()
        # _minimal_report_dict yields clarity=4 etc.; status defaults to draft.
        path = tmp_path / "test.eval.md"
        _write_eval_md(path, data)
        rc = main(["validate", str(path), "--complete", "--allow-misalignment"])
        assert rc != 0

    def test_validate_complete_accepts_filled_report(self, tmp_path: Path):
        """A filled, status=complete, with-reasons report passes --complete."""
        from pprose.eval_report import main

        data = _minimal_report_dict()
        data["metadata"]["status"] = "complete"
        data["metadata"]["evaluator"] = "test-human"
        data["metadata"]["rubric_version"] = "18-dim-v1"
        # Mark every score as 5 (no violations needed) and provide a reason for each.
        for group in data["qual"].values():
            for dim in group:
                group[dim] = 5
        data["qual_reasons"] = {
            "expression": {
                "clarity": "clean",
                "coherence": "clean",
                "concision": "clean",
            },
            "form": {
                "organization": "clean",
                "consistency": "clean",
                "formatting": "clean",
            },
            "purpose": {
                "suitability": "clean",
                "scope": "clean",
                "breadth": "clean",
                "depth": "clean",
            },
            "grounding": {"verifiability": "clean", "factuality": "clean", "relevance": "clean"},
            "reasoning": {
                "discipline": "clean",
                "soundness": "clean",
                "precision": "clean",
                "parsimony": "clean",
            },
            "judgment": {
                "calibration": "clean",
                "fairness": "clean",
                "robustness": "clean",
            },
        }
        path = tmp_path / "test.eval.md"
        _write_eval_md(path, data)
        rc = main(["validate", str(path), "--complete"])
        assert rc == 0

    def test_from_metrics_stub_passes_strict_validate(self, tmp_path: Path):
        """The from-metrics stub is all-zero qual; alignment should not flag it."""
        from pprose.eval_report import main

        out_path = tmp_path / "stub.eval.md"
        rc = main(
            [
                "from-metrics",
                str(FIXTURES / "all_headings.md"),
                "--out",
                str(out_path),
            ]
        )
        assert rc == 0
        # Now strict validate (no --allow-misalignment)
        rc = main(["validate", str(out_path)])
        assert rc == 0


def test_from_metrics_stub_qual_is_consistent_with_alignment_principle():
    """Stub qual is all ERR; rubric defines ERR as 'scorer could not assess', no
    violations needed.

    A strict validator must allow score=ERR with no violations, since ERR means
    the scorer could not assess the dimension rather than 'failed the rubric
    without citing a rule'.
    """
    from pprose.eval_report import stub_qual

    qual = stub_qual()
    from pprose import rubric_schema as rs

    assert qual.all_scores() == ["ERR"] * rs.dimension_count()


def test_compute_derived_in_place_is_idempotent(tmp_path: Path):
    """`report compute-derived --in-place` run twice is byte-stable (no churn)."""
    import shutil

    from pprose.eval_report import main as report_main

    src = Path(__file__).resolve().parent / "fixtures" / "rev1-net.eval.md"
    work = tmp_path / "r.eval.md"
    shutil.copyfile(src, work)

    assert report_main(["compute-derived", str(work), "--in-place"]) == 0
    first = work.read_text(encoding="utf-8")
    assert report_main(["compute-derived", str(work), "--in-place"]) == 0
    second = work.read_text(encoding="utf-8")
    assert first == second  # second pass changed nothing
    # And the result still validates.
    assert report_main(["validate", str(work)]) == 0
