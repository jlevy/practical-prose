"""Asserts the explorations workbench consumes the shared render-components.

After the rewire (epic pp-ict2 / bead pp-eece), the workbench's <head>
loads the shared CSS via `<link>` and the shared JS via `<script src>`,
and the inline `<style>` / `<script>` blocks no longer contain the
duplicated definitions. The workbench is now driven by the same files
the `pprose render` pipeline consumes.

These checks are static (no browser). For behavior verification, open
the workbench in Chrome / Safari and confirm the visualizations render
identically to the pre-rewire state.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
WORKBENCH = REPO_ROOT / "tools" / "explorations" / "visual-design" / "dimension-visualizations.html"
LIB_DIR = REPO_ROOT / "tools" / "explorations" / "visual-design" / "lib"


def _workbench_html() -> str:
    return WORKBENCH.read_text(encoding="utf-8")


def _head(html: str) -> str:
    m = re.search(r"<head>(.*?)</head>", html, re.DOTALL | re.IGNORECASE)
    assert m, "no <head> block in workbench"
    return m.group(1)


def _inline_main_script(html: str) -> str:
    """Return the workbench's main inline <script>...</script> contents.

    The workbench has multiple <script src> tags in the <head>; the main
    inline block sits at the bottom. Find the last `<script>`-without-`src`
    block.
    """
    matches = list(re.finditer(r"<script(?:\s[^>]*)?>(.*?)</script>", html, re.DOTALL))
    inline_blocks = [
        m for m in matches if not re.search(r"<script\s[^>]*\bsrc=", html[m.start() : m.end()])
    ]
    assert inline_blocks, "no inline <script> in workbench"
    # Heuristic: the main inline script is the longest one (>> 50KB).
    inline_blocks.sort(key=lambda m: len(m.group(1)), reverse=True)
    return inline_blocks[0].group(1)


# ─── Shared CSS is loaded via <link> ───────────────────────────────────────


@pytest.mark.parametrize(
    "expected_href",
    [
        "../../render-components/bi-card/card.css",
        "../../render-components/tip-panels/tip-panels.css",
        "../../render-components/theme-toggle/theme-toggle.css",
    ],
)
def test_workbench_links_shared_css(expected_href: str) -> None:
    head = _head(_workbench_html())
    assert f'href="{expected_href}"' in head, (
        f"expected <link> to {expected_href} in workbench <head>"
    )


# ─── Shared JS is loaded via <script src> ──────────────────────────────────


@pytest.mark.parametrize(
    "expected_src",
    [
        "../../render-components/bi-card/card.js",
        "../../render-components/tip-panels/tip-panels.js",
        "../../render-components/theme-toggle/theme-toggle.js",
    ],
)
def test_workbench_loads_shared_js(expected_src: str) -> None:
    head = _head(_workbench_html())
    assert f'src="{expected_src}"' in head, (
        f"expected <script src> to {expected_src} in workbench <head>"
    )


# ─── Workbench call sites use the shared namespaces ───────────────────────


def test_workbench_uses_shared_theme_toggle_mount() -> None:
    script = _inline_main_script(_workbench_html())
    assert "PracticalProseDesignColorControls.mountThemeToggle" in script, (
        "workbench should call the shared mountThemeToggle"
    )


def test_workbench_uses_shared_bi_card_via_makeApi() -> None:
    script = _inline_main_script(_workbench_html())
    assert "PracticalProseBiCard.makeApi" in script, (
        "workbench should source biCard/biDim9B/etc. from "
        "PracticalProseBiCard.makeApi() instead of redefining them inline"
    )


def test_workbench_uses_shared_tip_panels_mount() -> None:
    script = _inline_main_script(_workbench_html())
    assert "PracticalProseTipPanels.mount" in script, (
        "workbench's setupTipPanel wrapper should delegate to the shared "
        "PracticalProseTipPanels.mount()"
    )


# ─── Inline CSS no longer carries shared rules ─────────────────────────────


def _inline_style(html: str) -> str:
    m = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
    assert m, "no inline <style>"
    return m.group(1)


@pytest.mark.parametrize(
    "selector",
    [
        ".bi-card",
        ".bi-grid",
        ".bi-col",
        ".bi-group-header",
        ".bi-dim",
        ".bi-bar-track",
        ".bi-bar-fill",
        ".bi-bar-seg",
        ".bi-num-circle",
        ".bi-tick",
        ".bi-tip-panel",
        ".grp-icon",
        ".theme-toggle",
    ],
)
def test_workbench_inline_style_drops_shared_top_level_rule(selector: str) -> None:
    """No top-level rule whose first selector compound matches a shared one.

    The workbench's nested-selector rules that *qualify* a shared class are
    fine (e.g. `.bt-group-sep .grp-icon { ... }` — Visual 8 customizing
    .grp-icon inside its own context). The deletion target is the top-level
    rule that owned the class.
    """
    style = _inline_style(_workbench_html())
    # 6-space indent + selector + (whitespace or `,` or `{` or `:`) at the
    # very start of the selector list. This matches `.bi-card {`,
    # `.bi-card,`, `.bi-card .doc-kicker {`, etc. but does NOT match
    # `.something .bi-card { ... }` (where .bi-card is nested under
    # another selector).
    pattern = re.compile(rf"^      {re.escape(selector)}(?=[\s.,{{:])", re.MULTILINE)
    assert not pattern.search(style), (
        f"top-level rule `{selector}` should come from a shared render-component, "
        f"not the workbench's inline <style>"
    )


# `.surface-toggle` is workbench-only — must still be present.
def test_workbench_inline_style_keeps_surface_toggle() -> None:
    style = _inline_style(_workbench_html())
    assert ".surface-toggle" in style, (
        "the surface-toggle CSS is workbench-only and must stay inline"
    )


# ─── Inline JS no longer redefines shared function bodies ──────────────────


@pytest.mark.parametrize(
    "fn",
    [
        "biCard",
        "biDim9B",
        "_biDimPrep",
        "groupAvgChip",
        "_readScoreAlphaStep",
        "dimColorMix",
        "scoreColor",
        "segmentAlpha",
    ],
)
def test_workbench_inline_script_drops_shared_function(fn: str) -> None:
    script = _inline_main_script(_workbench_html())
    # Match the function declaration form the workbench used (top-level,
    # 6-space indent). The shared API is consumed via destructuring from
    # PracticalProseBiCard.makeApi(); a `const { fn } = biCardApi;`
    # destructure is not a "redefinition".
    pattern = re.compile(rf"^      function {re.escape(fn)}\b", re.MULTILINE)
    assert not pattern.search(script), (
        f"function `{fn}` is now sourced from PracticalProseBiCard.makeApi(); "
        f"it should no longer be redefined inline in the workbench"
    )


# ─── lib/design-color-controls.js no longer defines mountThemeToggle ──────


# ─── lib/design-color-controls.js no longer defines mountThemeToggle ──────


def test_lib_color_controls_drops_mount_theme_toggle() -> None:
    text = (LIB_DIR / "design-color-controls.js").read_text(encoding="utf-8")
    assert "function mountThemeToggle" not in text, (
        "mountThemeToggle moved to tools/render-components/theme-toggle/; "
        "the workbench's local lib should keep only mountSurfaceToggle"
    )
    # And mountSurfaceToggle should still be local (workbench-only).
    assert "function mountSurfaceToggle" in text or "mountSurfaceToggle =" in text
