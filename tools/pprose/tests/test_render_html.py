"""Tests for pprose.render_html — JSON-payload + shared-component pipeline."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from pprose import rubric_schema as rs
from pprose.eval_report import EvalReport
from pprose.render_html.renderer import (
    RenderOpts,
    available_variants,
    build_payload,
    detect_kind,
    render,
    render_eval_report,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"
PKG_DIR = Path(__file__).resolve().parents[1]


# ─── Detection ─────────────────────────────────────────────────────────────


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


def test_detect_kind_returns_none_for_near_miss_plain_md(tmp_path: Path) -> None:
    """A plain `.md` with eval-ish-but-invalid frontmatter is not an eval report."""
    near = tmp_path / "near.md"
    near.write_text("---\ntitle: x\nfoo: 1\n---\nbody\n", encoding="utf-8")
    assert detect_kind(near) is None


def test_detect_kind_does_not_swallow_unexpected_errors(tmp_path: Path, monkeypatch) -> None:
    """The narrowed except lets genuinely unexpected errors propagate, not read as None."""
    from pprose.render_html import renderer

    def boom(_source):
        raise RuntimeError("unexpected parser failure")

    monkeypatch.setattr(renderer.EvalReport, "from_eval_md", staticmethod(boom))
    target = tmp_path / "x.md"
    target.write_text("# doc\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="unexpected parser failure"):
        detect_kind(target)


def test_render_malformed_eval_md_raises_clear_validation_error(tmp_path: Path) -> None:
    """A `.eval.md` named-but-invalid file errors clearly rather than rendering empty."""
    bad = tmp_path / "bad.eval.md"
    bad.write_text("---\ntitle: x\nfoo: 1\n---\nbody\n", encoding="utf-8")
    assert detect_kind(bad) == "eval_report"  # routed by name
    with pytest.raises(ValueError, match="(?i)eval"):
        render(bad, RenderOpts())


# ─── Variant discovery ─────────────────────────────────────────────────────


def test_available_variants_includes_interactive() -> None:
    assert "interactive" in available_variants()


def test_unknown_variant_raises_with_available_list() -> None:
    report = EvalReport.from_eval_md(FIXTURES / "rev2-net.eval.md")
    with pytest.raises(ValueError, match="interactive"):
        render_eval_report(report, RenderOpts(variant="nope"))


# ─── Payload construction ─────────────────────────────────────────────────


def _fixture_report() -> EvalReport:
    return EvalReport.from_eval_md(FIXTURES / "rev2-net.eval.md")


def test_payload_has_groups_and_dimensions() -> None:
    report = _fixture_report()
    payload = build_payload(report)
    assert len(payload["groups"]) == len(rs.GROUPS)
    assert len(payload["dimensions"]) == rs.dimension_count()
    # Each group label is present.
    group_labels = {g["label"] for g in payload["groups"]}
    for g in rs.GROUPS:
        assert g.label in group_labels


def test_payload_dim_ids_follow_design_system_convention() -> None:
    report = _fixture_report()
    payload = build_payload(report)
    # P1..P4, E1..E3, F1..F3, R1..R4, G1..G3, J1..J3
    expected_ids = {
        f"{group.key[0].upper()}{i}"
        for group in rs.GROUPS
        for i, _ in enumerate(group.dimensions, start=1)
    }
    actual_ids = {d["id"] for d in payload["dimensions"]}
    assert actual_ids == expected_ids


def test_payload_rubric_per_dim_carries_question_and_rules() -> None:
    report = _fixture_report()
    payload = build_payload(report)
    for dim in payload["dimensions"]:
        rubric = payload["rubric"][dim["id"]]
        assert "question" in rubric
        assert "rules" in rubric
        assert "group" in rubric


def test_payload_doc_has_scores_keyed_by_dim_id() -> None:
    report = _fixture_report()
    payload = build_payload(report)
    score_keys = set(payload["doc"]["scores"].keys())
    dim_ids = {d["id"] for d in payload["dimensions"]}
    assert score_keys == dim_ids


def test_payload_handles_numeric_na_and_err_scores() -> None:
    report = _fixture_report()
    qual_dict = report.qual.model_dump()
    qual_dict["purpose"]["suitability"] = "NA"
    qual_dict["judgment"]["robustness"] = "ERR"
    report.qual = type(report.qual).model_validate(qual_dict)
    payload = build_payload(report)
    assert payload["doc"]["scores"]["P1"] == "NA"
    assert payload["doc"]["scores"]["J3"] == "ERR"
    # Numeric scores stay int.
    assert any(isinstance(v, int) for v in payload["doc"]["scores"].values())


# ─── Rendered HTML shell ───────────────────────────────────────────────────


def test_render_emits_doctype_and_eval_data_block() -> None:
    report = _fixture_report()
    html = render_eval_report(report, RenderOpts(pprose_version="test"))
    assert "<!doctype html>" in html.lower()
    # The bootstrap reads from this <script> id.
    assert 'id="pp-eval-data"' in html


def test_render_inlines_three_component_mounts() -> None:
    report = _fixture_report()
    html = render_eval_report(report, RenderOpts())
    # The interactive variant's bootstrap calls all three component mounts.
    assert "PracticalProseBiCard.mount" in html
    assert "PracticalProseTipPanels.mount" in html
    assert "PracticalProseDesignColorControls.mountThemeToggle" in html


def test_render_includes_theme_toggle_markup() -> None:
    report = _fixture_report()
    html = render_eval_report(report, RenderOpts())
    assert 'class="theme-toggle"' in html
    assert 'data-theme-set="auto"' in html


def test_render_a4_rewrites_page_size_in_print_block() -> None:
    report = _fixture_report()
    html = render_eval_report(report, RenderOpts(page_size="a4"))
    assert "size: A4;" in html
    assert "size: letter;" not in html


def test_render_inlined_payload_round_trips_via_json() -> None:
    report = _fixture_report()
    html = render_eval_report(report, RenderOpts())
    # Extract the inlined payload.
    m = re.search(
        r'<script type="application/json" id="pp-eval-data">(.*?)</script>',
        html,
        re.DOTALL,
    )
    assert m, "expected the pp-eval-data <script> in the rendered HTML"
    parsed = json.loads(m.group(1))
    assert set(parsed.keys()) == {"groups", "dimensions", "rubric", "doc"}


# ─── Drift check ───────────────────────────────────────────────────────────


def test_sync_render_html_styles_in_sync() -> None:
    """Run the sync script in --check mode. Fails on any unsynced output.

    Mirrors the CI gate: if render-components/ or design-system/ has
    changed and the wheel _generated/ copies haven't been refreshed,
    this test fails with the file list.
    """
    script = PKG_DIR / "devtools" / "sync_render_html_styles.py"
    result = subprocess.run(
        [sys.executable, str(script), "--check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        "sync_render_html_styles.py --check reported drift:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}\n"
        "Run `uv run python devtools/sync_render_html_styles.py` to refresh."
    )


# ─── print.css palette drift guard (pp-lpun) ─────────────────────────────────


def _css_vars(text: str) -> dict[str, str]:
    """Extract `--name: value` custom properties from a CSS string."""
    return dict(re.findall(r"--([\w-]+):\s*([^;]+);", text))


def test_print_css_palette_tokens_match_generated_light_theme() -> None:
    """print.css mirrors the light accent/dim palette; guard against silent drift.

    print.css intentionally overrides bg/fg/card to pure-paper values, but its
    `--accent-*` / `--dim-*` tokens are copied from the light theme. The light theme
    is generated from design-system.yaml into _generated/design_system.css, so if the
    YAML palette changes, the hand-maintained print.css block would silently drift
    (the sync --check gate does not cover print.css). This locks them together.
    """
    import re as _re

    import pprose.render_html as rh

    styles = Path(rh.__file__).resolve().parent / "styles"
    design_css = (styles / "_generated" / "design_system.css").read_text(encoding="utf-8")
    print_css = (styles / "print.css").read_text(encoding="utf-8")

    # Light theme = the first `:root { ... }` block of the generated CSS.
    light_block = _re.search(r":root\s*\{([^}]*)\}", design_css)
    assert light_block, "could not find light :root block in design_system.css"
    light = _css_vars(light_block.group(1))
    printed = _css_vars(print_css)

    palette = {k: v for k, v in printed.items() if k.startswith(("accent-", "dim-"))}
    assert palette, "print.css exposes no accent-/dim- tokens — block moved?"
    mismatches = {k: (printed[k], light.get(k)) for k in palette if printed[k] != light.get(k)}
    assert not mismatches, (
        "print.css palette drifted from the generated light theme; regenerate the "
        f"design system and resync print.css: {mismatches}"
    )
