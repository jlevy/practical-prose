"""Asset bundling for single-file HTML output.

The renderer concatenates the bundled stylesheets in a deterministic
order and hands the result to the base template, which drops it into a
<style> block. The SVG icon set is similarly read once and inlined where
the template references it.

Folder mode (`--format folder`) writes the HTML alongside a sibling
`assets/` directory carrying the same files as sidecars, so a developer
can edit them in place during iteration without rebuilding.
"""

from __future__ import annotations

from pathlib import Path

_STYLES_DIR = Path(__file__).resolve().parent / "styles"
_ASSETS_DIR = Path(__file__).resolve().parent / "assets"

# Concatenation order:
#   1. _generated/design_system.css — canonical tokens written by
#      tools/design-system/generate.py from design-system.yaml.  Single
#      source of truth for colors, fonts, weights, sizes.  Never hand-edit.
#   2. local_extras.css — tokens the renderer needs but that aren't
#      (yet) in the design system YAML: --font-mono, --score-na-fill,
#      --score-err-fill.
#   3. surface_white.css — page surface override (white instead of the
#      design system's warm cream).  Drop from this list to revert.
#   4. base / per-section rules (consume the tokens above).
#   5. print.css last so its @media print rules override on-screen.
_STYLESHEET_ORDER = (
    "_generated/design_system.css",
    "local_extras.css",
    "surface_white.css",
    "base.css",
    "card.css",
    "detail.css",
    "metrics.css",
    "print.css",
)


def bundled_css(page_size: str = "letter") -> str:
    """Return the concatenated stylesheet, with @page size rewritten."""
    parts: list[str] = []
    for name in _STYLESHEET_ORDER:
        parts.append(f"/* --- {name} --- */")
        parts.append((_STYLES_DIR / name).read_text(encoding="utf-8"))
    css = "\n".join(parts)
    if page_size.lower() == "a4":
        css = css.replace("size: letter;", "size: A4;")
    return css


def bundled_icons_svg() -> str:
    """Return the inline SVG symbol set."""
    return (_ASSETS_DIR / "icons.svg").read_text(encoding="utf-8")


def write_folder_assets(out_dir: Path) -> None:
    """Copy stylesheets + icons into <out_dir>/assets/ for folder mode."""
    asset_dir = out_dir / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    for name in _STYLESHEET_ORDER:
        dest = asset_dir / name
        # _generated/design_system.css lives in a subdir — make sure it
        # exists before writing.
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(
            (_STYLES_DIR / name).read_text(encoding="utf-8"), encoding="utf-8"
        )
    (asset_dir / "icons.svg").write_text(bundled_icons_svg(), encoding="utf-8")
