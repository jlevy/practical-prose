"""Asset bundling for single-file HTML output.

Reads from `styles/_generated/` and `js/_generated/` (mirrored by
`devtools/sync_render_html_styles.py`), plus the renderer-owned
`styles/base.css` and `styles/print.css`. Concatenates CSS into one
inlined `<style>` block and JS into one inlined `<script>` block. The SVG
icon sprite is read from `assets/icons.svg` and inlined as-is.

The hand-edited files under styles/ are `base.css` (screen html/body
foundation) and `print.css` (@media print overrides). The `_generated/`
subdirectory carries an "AUTO-GENERATED" provenance in each source file;
never edit those directly.
"""

from __future__ import annotations

from pathlib import Path

_RENDER_HTML_DIR = Path(__file__).resolve().parent
_STYLES_DIR = _RENDER_HTML_DIR / "styles"
_STYLES_GEN_DIR = _STYLES_DIR / "_generated"
_JS_GEN_DIR = _RENDER_HTML_DIR / "js" / "_generated"
_ASSETS_DIR = _RENDER_HTML_DIR / "assets"

# CSS concatenation order — design-system tokens first so component CSS
# can reference them; base.css next so the html/body foundation applies the
# tokens before components layer on top; print.css last so its @media print
# rules win over on-screen rules.
_CSS_ORDER = (
    _STYLES_GEN_DIR / "design_system.css",
    _STYLES_DIR / "base.css",
    _STYLES_GEN_DIR / "bi-card.css",
    _STYLES_GEN_DIR / "tip-panels.css",
    _STYLES_GEN_DIR / "theme-toggle.css",
    _STYLES_DIR / "print.css",
)

# JS concatenation order — marked (the markdown lib) first because
# tip-panels.js references `window.marked` at mount time; then the three
# components in dependency order (bi-card before tip-panels because
# tip-panels mirrors a card row via the bi-card api).
_JS_ORDER = (
    _JS_GEN_DIR / "marked.min.js",
    _JS_GEN_DIR / "bi-card.js",
    _JS_GEN_DIR / "tip-panels.js",
    _JS_GEN_DIR / "theme-toggle.js",
)


def bundled_css(page_size: str = "letter") -> str:
    """Return the concatenated stylesheet, with @page size rewritten."""
    parts: list[str] = []
    for path in _CSS_ORDER:
        parts.append(f"/* --- {path.name} --- */")
        parts.append(path.read_text(encoding="utf-8"))
    css = "\n".join(parts)
    if page_size.lower() == "a4":
        css = css.replace("size: letter;", "size: A4;")
    return css


def bundled_js() -> str:
    """Return the concatenated JavaScript bundle."""
    parts: list[str] = []
    for path in _JS_ORDER:
        parts.append(f"/* --- {path.name} --- */")
        parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts)


def bundled_icons_svg() -> str:
    """Return the inline SVG symbol set."""
    return (_ASSETS_DIR / "icons.svg").read_text(encoding="utf-8")
