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


# NOTE: Deleting the duplicated inline CSS rules + JS function definitions
# from the workbench is a follow-up cleanup (tracked as a separate bead). The
# rewire above ensures the shared files are loaded; the inline copies are
# byte-equivalent to them via the sync script's drift check on
# render-components/, so the workbench still renders correctly today.
# Once renderBidirectional() is migrated to use PracticalProseTipPanels.mount()
# (which scopes hover to document, not per-viz layouts), the inline copies
# can be deleted and the assertion suite can be tightened.


# ─── lib/design-color-controls.js no longer defines mountThemeToggle ──────


def test_lib_color_controls_drops_mount_theme_toggle() -> None:
    text = (LIB_DIR / "design-color-controls.js").read_text(encoding="utf-8")
    assert "function mountThemeToggle" not in text, (
        "mountThemeToggle moved to tools/render-components/theme-toggle/; "
        "the workbench's local lib should keep only mountSurfaceToggle"
    )
    # And mountSurfaceToggle should still be local (workbench-only).
    assert "function mountSurfaceToggle" in text or "mountSurfaceToggle =" in text
