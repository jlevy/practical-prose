"""Tests for prose_eval.eval_compare, the Markdown comparison generator.

Run:
  uv run pytest tests/test_eval_compare.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml  # noqa: E402

from prose_eval.eval_compare import (  # noqa: E402
    QUALITATIVE_SCORE_NOTE,
    _bold_indices,
    check_rubric_versions,
    check_scope_classes,
    collect_density_concerns,
    main,
    render_per_pair_deltas,
    render_section_drilldown,
    render_unified_table,
)
from prose_eval.eval_report import EvalReport  # noqa: E402


def _write_eval_md(path: Path, report: EvalReport) -> None:
    """Write a report to `path` as a minimal .eval.md (frontmatter, empty body).

    Tests that construct in-memory reports and write them to disk for the CLI
    to read back use this helper to produce a valid .eval.md without going
    through the renderer (which is exercised separately by render-shape tests).
    """
    data = report.model_dump(mode="json", exclude_none=True)
    path.write_text(f"---\n{yaml.safe_dump(data)}---\n", encoding="utf-8")


FIXTURE_DIR = Path(__file__).parent / "fixtures"
GOLDEN = FIXTURE_DIR / "expected-comparison.md"
ALL_FIXTURES = [
    FIXTURE_DIR / "figma-ddog-r1.eval.md",
    FIXTURE_DIR / "figma-ddog-r2.eval.md",
    FIXTURE_DIR / "figma-ddog-r4.eval.md",
    FIXTURE_DIR / "figma-net-r1.eval.md",
    FIXTURE_DIR / "figma-net-r2.eval.md",
    FIXTURE_DIR / "figma-net-r4.eval.md",
]


def _load(paths: list[Path]) -> list[EvalReport]:
    return [EvalReport.from_eval_md(p) for p in paths]


def test_golden_six_way_unified_with_pairs(capsys: pytest.CaptureFixture[str]):
    # The figma fixtures retain their original 12-dim score values where alignment
    # was clean and demote everything else to 0 ("applicable but unassessable")
    # under 18-dim-v1, so --allow-misalignment is not needed.
    args = [str(p) for p in ALL_FIXTURES] + [
        "--format",
        "unified",
        "--pairs",
        "DDOG-r1=DDOG-r4",
        "NET-r1=NET-r4",
        "DDOG-r2=DDOG-r4",
        "NET-r2=NET-r4",
    ]
    rc = main(args)
    assert rc == 0
    captured = capsys.readouterr().out
    assert captured == GOLDEN.read_text(encoding="utf-8")


def test_bold_max_picks_unique_max():
    indices = _bold_indices([1, 2, 3, 2], rule="max", mode="max")
    assert indices == {2}


def test_bold_max_picks_all_ties():
    indices = _bold_indices([5, 5, 3], rule="max", mode="max")
    assert indices == {0, 1}


def test_bold_no_marking_when_all_equal():
    indices = _bold_indices([4, 4, 4], rule="max", mode="max")
    assert indices == set()


def test_bold_min_for_lint():
    indices = _bold_indices([3, 1, 2], rule="min", mode="max")
    assert indices == {1}


def test_bold_none_rule():
    indices = _bold_indices([1, 5, 3], rule="none", mode="max")
    assert indices == set()


def test_bold_skips_none_values():
    indices = _bold_indices([None, 5, 3], rule="max", mode="max")
    assert indices == {1}


def test_bold_materially_different_threshold():
    # Threshold: max - median >= 1 (inclusive) counts as material.
    # median=3, max=5 → diff=2 → bold
    assert _bold_indices([1, 3, 3, 5], rule="max", mode="materially-different") == {3}
    # median=4, max=5 → diff=1 → exactly at threshold → bold
    assert _bold_indices([4, 4, 5], rule="max", mode="materially-different") == {2}
    # median=4.5, max=5 → diff=0.5 → not material
    assert _bold_indices([4, 4, 5, 5, 5], rule="max", mode="materially-different") == set()


def test_unified_renders_header_and_rows():
    reports = _load(ALL_FIXTURES[:2])
    text = render_unified_table(reports)
    lines = text.splitlines()
    assert lines[0] == "| Approach | Aspect | Measure | DDOG-r1 | DDOG-r2 |"
    assert lines[1].startswith("| --- | --- | --- |")
    assert lines[1].endswith("---: |")


def test_cell_coalescing_blanks_repeated_approach_aspect():
    reports = _load(ALL_FIXTURES[:2])
    text = render_unified_table(reports)
    # First Qualitative row should have **Qualitative...** in approach column.
    # The second row within the same group should have empty approach + aspect cells.
    qual_rows = [
        line for line in text.splitlines() if "| Suitability |" in line or "| Scope |" in line
    ]
    assert "**Qualitative" in qual_rows[0]
    assert qual_rows[1].startswith("|  |  |")  # both approach + aspect coalesced


def test_pair_deltas_compute_correctly():
    reports = _load(ALL_FIXTURES)
    text = render_per_pair_deltas(reports, [("DDOG-r1", "DDOG-r4")])
    assert "Delta: DDOG-r1 → DDOG-r4" in text
    assert "| Calibration | +2 |" in text
    # Inference Discipline = old Discipline; unchanged in the figma mechanical migration.
    assert "| Inference Discipline | 0 |" in text
    # Mean delta sign is the regression-test signal (DDOG-r4 still higher than DDOG-r1).
    assert "**Mean** | **+" in text


def test_pair_deltas_unknown_label_raises():
    reports = _load(ALL_FIXTURES[:2])
    with pytest.raises(ValueError, match="unknown label"):
        render_per_pair_deltas(reports, [("DDOG-r1", "BOGUS")])


def test_invalid_pair_spec_raises(capsys: pytest.CaptureFixture[str]):
    with pytest.raises(SystemExit, match="invalid"):
        main(
            [
                str(ALL_FIXTURES[0]),
                str(ALL_FIXTURES[1]),
                "--allow-misalignment",
                "--pairs",
                "no-equals",
            ]
        )


def test_format_sections_emits_per_aspect_tables(capsys: pytest.CaptureFixture[str]):
    rc = main([str(p) for p in ALL_FIXTURES[:2]] + ["--allow-misalignment", "--format", "sections"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "### Qualitative — Expression" in out
    assert "### Quantitative — Size" in out
    assert "### Derived — Density" in out


def test_unified_cli_emits_score_note_below_table(capsys: pytest.CaptureFixture[str]):
    rc = main([str(p) for p in ALL_FIXTURES[:2]] + ["--allow-misalignment", "--format", "unified"])
    assert rc == 0
    out = capsys.readouterr().out
    assert QUALITATIVE_SCORE_NOTE in out
    assert out.index(QUALITATIVE_SCORE_NOTE) > out.index("| Approach | Aspect | Measure |")


def test_table_styles_flag_prepends_portable_frontmatter(capsys: pytest.CaptureFixture[str]):
    rc = main(
        [str(p) for p in ALL_FIXTURES[:2]]
        + ["--allow-misalignment", "--format", "unified", "--table-styles"]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "&id" not in out
    assert "*id" not in out
    lines = out.splitlines()
    assert lines[0] == "---"
    end = lines.index("---", 1)
    frontmatter = yaml.safe_load("\n".join(lines[1:end]))

    table_styles = frontmatter["display"]["table_styles"]
    assert table_styles["version"] == 1
    comparison_table = next(
        table
        for table in table_styles["tables"]
        if table["id"] == "practical_prose_unified_comparison"
    )
    assert comparison_table["match"]["columns"] == [
        "Approach",
        "Aspect",
        "Measure",
        "DDOG-r1",
        "DDOG-r2",
    ]
    assert "| Approach | Aspect | Measure | DDOG-r1 | DDOG-r2 |" in "\n".join(lines[end + 1 :])


def test_determinism():
    reports = _load(ALL_FIXTURES)
    a = render_unified_table(reports)
    b = render_unified_table(reports)
    assert a == b


def test_lint_row_bolds_minimum():
    reports = _load(ALL_FIXTURES)
    text = render_unified_table(reports)
    for line in text.splitlines():
        if "Banned-register hits" in line:
            # DDOG-r4 (0) and NET-r4 (0) should be bolded — both tied at min.
            # Values appear in column order: DDOG-r1=1, DDOG-r2=1, DDOG-r4=0, NET-r1=3, NET-r2=2, NET-r4=0
            # Expected: third and sixth values bold.
            assert line.count("**0**") == 2
            return
    pytest.fail("Banned-register hits row not found")


# ---------------------------------------------------------------------------
# B6: rubric_version cross-version warning
# ---------------------------------------------------------------------------


def _make_report(
    label: str,
    rubric_version: str | None,
    *,
    judgment_na: bool = False,
) -> EvalReport:
    """Build a minimal EvalReport with the given rubric_version tag."""
    data = {
        "artifact": {"label": label, "path": f"{label}.md"},
        "quant": {
            "size": {
                "words": 1000,
                "sentences": 50,
                "paragraphs": 25,
                "lines": 200,
                "pages_275wpp": 3.6,
            },
            "headings": {"h1": 1, "h2": 4, "h3": 10, "h4": 5, "total": 20},
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
        },
        "qual": {
            "expression": {
                "clarity": 4,
                "coherence": 5,
                "concision": 4,
                "organization": 5,
                "style_consistency": 0,
                "formatting": 0,
            },
            "purpose": {"suitability": 4, "breadth": 4, "depth": 4},
            "grounding": {"verifiability": 5, "factuality": 4},
            "reasoning": {"inference_discipline": 4, "soundness": 5, "precision": 4},
            "judgment": (
                {"calibration": "NA", "fairness": "NA", "robustness": "NA"}
                if judgment_na
                else {"calibration": 5, "fairness": 5, "robustness": 4}
            ),
        },
        "metadata": {"eval_date": "2026-05-09", "evaluator": "test"},
    }
    if rubric_version is not None:
        data["metadata"]["rubric_version"] = rubric_version
    return EvalReport.model_validate(data)


def test_all_na_group_mean_renders_dash():
    reports = [
        _make_report("scored", "18-dim-v1"),
        _make_report("all-na", "18-dim-v1", judgment_na=True),
    ]

    assert "| *Mean* | 4.67 | — |" in render_section_drilldown(reports)
    assert "|  |  | *Mean* | 4.67 | — |" in render_unified_table(reports)


def test_check_rubric_versions_all_same():
    reports = [
        _make_report("a", "15-dim-v1"),
        _make_report("b", "15-dim-v1"),
    ]
    assert check_rubric_versions(reports) is None


def test_check_rubric_versions_all_untagged():
    reports = [_make_report("a", None), _make_report("b", None)]
    assert check_rubric_versions(reports) is None


def test_check_rubric_versions_cross_version_warns():
    reports = [
        _make_report("a", "12-dim-v1"),
        _make_report("b", "15-dim-v1"),
    ]
    msg = check_rubric_versions(reports)
    assert msg is not None
    assert "12-dim-v1" in msg
    assert "15-dim-v1" in msg


def test_check_rubric_versions_mixed_tagged_and_untagged_warns():
    reports = [
        _make_report("a", "15-dim-v1"),
        _make_report("b", None),
    ]
    msg = check_rubric_versions(reports)
    assert msg is not None
    assert "15-dim-v1" in msg
    assert "untagged" in msg


def test_unified_table_emits_warning_block_on_mismatch(capsys):
    """When versions mismatch, the rendered output begins with a warning block."""
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        a = _make_report("A", "12-dim-v1")
        b = _make_report("B", "15-dim-v1")
        a_path = td_path / "a.eval.md"
        b_path = td_path / "b.eval.md"
        _write_eval_md(a_path, a)
        _write_eval_md(b_path, b)

        rc = main(
            [
                str(a_path),
                str(b_path),
                "--allow-draft",
                "--allow-misalignment",
                "--format",
                "unified",
            ]
        )
    assert rc == 0
    out = capsys.readouterr()
    assert "Rubric-version warning" in out.out
    assert "12-dim-v1" in out.out


# ---------------------------------------------------------------------------
# B13: scope-class cross-class warning
# ---------------------------------------------------------------------------


def _make_report_with_scope(label: str, scope_class: str | None) -> EvalReport:
    data = {
        "artifact": {"label": label, "path": f"{label}.md"},
        "quant": {
            "size": {
                "words": 1000,
                "sentences": 50,
                "paragraphs": 25,
                "lines": 200,
                "pages_275wpp": 3.6,
            },
            "headings": {"h1": 1, "h2": 4, "h3": 10, "h4": 5, "total": 20},
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
        },
        "qual": {
            "expression": {
                "clarity": 4,
                "coherence": 5,
                "concision": 4,
                "organization": 5,
                "style_consistency": 0,
                "formatting": 0,
            },
            "purpose": {"suitability": 4, "breadth": 4, "depth": 4},
            "grounding": {"verifiability": 5, "factuality": 4},
            "reasoning": {"inference_discipline": 4, "soundness": 5, "precision": 4},
            "judgment": {"calibration": 5, "fairness": 5, "robustness": 4},
        },
        "metadata": {"eval_date": "2026-05-09", "evaluator": "test", "rubric_version": "15-dim-v1"},
    }
    if scope_class is not None:
        data["artifact"]["scope_class"] = scope_class
    return EvalReport.model_validate(data)


def test_check_scope_classes_all_same():
    reports = [
        _make_report_with_scope("a", "deep_research"),
        _make_report_with_scope("b", "deep_research"),
    ]
    assert check_scope_classes(reports) is None


def test_check_scope_classes_cross_class_warns():
    reports = [
        _make_report_with_scope("a", "status"),
        _make_report_with_scope("b", "deep_research"),
    ]
    msg = check_scope_classes(reports)
    assert msg is not None
    assert "status" in msg
    assert "deep_research" in msg


def test_check_scope_classes_mixed_tagged_untagged_warns():
    reports = [
        _make_report_with_scope("a", "deep_research"),
        _make_report_with_scope("b", None),
    ]
    msg = check_scope_classes(reports)
    assert msg is not None
    assert "untagged" in msg


# ---------------------------------------------------------------------------
# B12: density-concerns collection
# ---------------------------------------------------------------------------


def test_collect_density_concerns_returns_only_flagged():
    """Only reports with non-empty density_concerns() show up."""
    healthy = _make_report_with_scope("healthy", "deep_research")
    # Build an unhealthy report with 0 links
    unhealthy_data = {
        "artifact": {"label": "lownet", "path": "lownet.md", "scope_class": "deep_research"},
        "quant": {
            "size": {
                "words": 5000,
                "sentences": 250,
                "paragraphs": 125,
                "lines": 800,
                "pages_275wpp": 18.2,
            },
            "headings": {"h1": 1, "h2": 5, "h3": 10, "h4": 4, "total": 20},
            "structural": {"tables": 4, "code_blocks": 0, "images": 0},
            "links": {
                "total": 0,
                "external": 0,
                "internal": 0,
                "inline": 0,
                "reference": 0,
                "autolink": 0,
                "bare_urls": 0,
            },
            "provenance": {"bracket_tags": 0, "footnote_refs": 0, "footnote_defs": 0},
            "lint": {"banned_register_hits": 0},
        },
        "qual": {
            "expression": {
                "clarity": 4,
                "coherence": 5,
                "concision": 4,
                "organization": 5,
                "style_consistency": 0,
                "formatting": 0,
            },
            "purpose": {"suitability": 4, "breadth": 4, "depth": 4},
            "grounding": {"verifiability": 5, "factuality": 4},
            "reasoning": {"inference_discipline": 4, "soundness": 5, "precision": 4},
            "judgment": {"calibration": 5, "fairness": 5, "robustness": 4},
        },
        "metadata": {"eval_date": "2026-05-09", "evaluator": "test", "rubric_version": "15-dim-v1"},
    }
    unhealthy = EvalReport.model_validate(unhealthy_data)
    concerns = collect_density_concerns([healthy, unhealthy])
    assert len(concerns) == 1
    assert concerns[0][0] == "lownet"
    assert any("link density" in c for c in concerns[0][1])


def test_unified_emits_scope_warning_block(capsys):
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        a = _make_report_with_scope("A", "status")
        b = _make_report_with_scope("B", "deep_research")
        a_path = td_path / "a.eval.md"
        b_path = td_path / "b.eval.md"
        _write_eval_md(a_path, a)
        _write_eval_md(b_path, b)

        rc = main(
            [
                str(a_path),
                str(b_path),
                "--allow-draft",
                "--allow-misalignment",
                "--format",
                "unified",
            ]
        )
    assert rc == 0
    out = capsys.readouterr().out
    assert "Scope-class warning" in out


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
