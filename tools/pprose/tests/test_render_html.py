"""Tests for pprose.render_html — static HTML eval report renderer."""

from __future__ import annotations

from pathlib import Path

import pytest

from pprose import rubric_schema as rs
from pprose.eval_report import EvalReport
from pprose.render_html.renderer import (
    RenderOpts,
    _build_dim_rows,
    detect_kind,
    render,
    render_eval_report,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


# Detection -----------------------------------------------------------------


def test_detect_kind_recognizes_eval_md_extension() -> None:
    assert detect_kind(FIXTURES / "rev2-net.eval.md") == "eval_report"


def test_detect_kind_returns_none_for_plain_markdown(tmp_path: Path) -> None:
    plain = tmp_path / "plain.md"
    plain.write_text("# Just a doc\n\nHello.\n", encoding="utf-8")
    assert detect_kind(plain) is None


def test_detect_kind_returns_none_for_non_markdown(tmp_path: Path) -> None:
    txt = tmp_path / "notes.txt"
    txt.write_text("not markdown", encoding="utf-8")
    assert detect_kind(txt) is None


def test_render_unsupported_kind_lists_supported_kinds(tmp_path: Path) -> None:
    bogus = tmp_path / "bogus.txt"
    bogus.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError, match="eval_report"):
        render(bogus, RenderOpts())


# Eval-report rendering -----------------------------------------------------


def _fixture_report() -> EvalReport:
    return EvalReport.from_eval_md(FIXTURES / "rev2-net.eval.md")


def test_render_fixture_produces_html_with_card_and_doc_name() -> None:
    report = _fixture_report()
    html = render_eval_report(report, RenderOpts(pprose_version="test"))
    assert "<!doctype html>" in html
    assert "Practical Prose Evaluation" in html
    assert report.artifact.label in html
    # Every rubric dimension label should appear at least once on the card.
    for d in rs.DIMENSIONS:
        assert d.label in html, f"missing dimension label: {d.label}"


def test_render_includes_overall_mean_when_derived_present() -> None:
    report = _fixture_report()
    html = render_eval_report(report, RenderOpts())
    assert "Overall mean" in html
    # The fixture has overall_mean ~3.10 — format to one of the rendered shapes.
    rollup = report.derived.rubric_rollup
    assert f"{rollup.overall_mean:.2f}" in html


def test_render_sections_subset_omits_other_pages() -> None:
    report = _fixture_report()
    html = render_eval_report(report, RenderOpts(sections=("card", "footer")))
    assert "Per-dimension Detail" not in html
    assert "Quantitative Metrics" not in html
    assert "Provenance" in html


def test_render_a4_rewrites_page_size_in_print_block() -> None:
    report = _fixture_report()
    html = render_eval_report(report, RenderOpts(page_size="a4", sections=("card",)))
    assert "size: A4;" in html
    assert "size: letter;" not in html


# Schema coverage -----------------------------------------------------------


def test_dim_rows_handle_numeric_and_sentinel_scores() -> None:
    """Build a row set from a fixture and verify NA/ERR/1-5 each render."""
    report = _fixture_report()
    rows = _build_dim_rows(report)
    assert len(rows) == rs.dimension_count()
    seen_numeric = any(isinstance(r.score, int) for r in rows)
    assert seen_numeric, "fixture should contain at least one numeric score"
    # Render with a doctored report where one row is NA and one is ERR.
    qual_dict = report.qual.model_dump()
    qual_dict["purpose"]["suitability"] = "NA"
    qual_dict["judgment"]["robustness"] = "ERR"
    report.qual = type(report.qual).model_validate(qual_dict)
    html = render_eval_report(report, RenderOpts())
    assert "is-na" in html
    assert "is-err" in html
    assert "ERR" in html
