#!/usr/bin/env python3
"""Mirror shared render-components into the pprose wheel.

This script is the **only** path that writes into
`tools/pprose/src/pprose/render_html/styles/_generated/` and
`tools/pprose/src/pprose/render_html/js/_generated/`. Run it after every
change to any source; never hand-edit the generated files. Sources:

1. `tools/design-system/_generated/design_system.css` — mirrored verbatim
   into `styles/_generated/design_system.css`.

2. `tools/render-components/<name>/` — one per shared component
   (bi-card, tip-panels, theme-toggle). Each component carries a `.css`,
   a `.js`, and (optionally) a `.html.jinja` partial. The CSS goes to
   `styles/_generated/<name>.css`; the JS goes to `js/_generated/<name>.js`;
   the Jinja partial goes to `templates/<name>.html.jinja`.

3. `tools/render-components/vendor/marked.min.js` — third-party markdown
   library the tip-panels component depends on at runtime. Mirrored to
   `js/_generated/marked.min.js`.

4. `tools/design-system/assets/icons.svg` — group icon sprite, inlined
   into the rendered HTML. Mirrored to
   `src/pprose/render_html/assets/icons.svg`.

Every output is byte-for-byte identical to its source. The script prepends
nothing; provenance lives in each source file's leading comment.

Usage:
    uv run python devtools/sync_render_html_styles.py            # write
    uv run python devtools/sync_render_html_styles.py --check    # exit 1 on drift
"""

from __future__ import annotations

import sys
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parents[1]  # tools/pprose
REPO_ROOT = Path(__file__).resolve().parents[3]  # repo root

DESIGN_SYSTEM_DIR = REPO_ROOT / "tools" / "design-system"
COMPONENTS_DIR = REPO_ROOT / "tools" / "render-components"
PKG_RENDER_HTML = PKG_DIR / "src" / "pprose" / "render_html"

STYLES_GEN = PKG_RENDER_HTML / "styles" / "_generated"
JS_GEN = PKG_RENDER_HTML / "js" / "_generated"
TEMPLATES = PKG_RENDER_HTML / "templates"
ASSETS = PKG_RENDER_HTML / "assets"

# Manifest of shared components. The sync script copies each tuple into the
# wheel without touching its contents. Adding a new component is a one-line
# append here plus a new directory under tools/render-components/.
COMPONENTS = ("bi-card", "tip-panels", "theme-toggle")


# (src_relative_to_repo_root, dst_absolute) pairs.
def _build_jobs() -> list[tuple[Path, Path]]:
    jobs: list[tuple[Path, Path]] = []

    # Design-system tokens.
    jobs.append(
        (
            DESIGN_SYSTEM_DIR / "_generated" / "design_system.css",
            STYLES_GEN / "design_system.css",
        )
    )

    # Per-component CSS + JS, plus optional Jinja partials.
    for name in COMPONENTS:
        comp_dir = COMPONENTS_DIR / name
        # CSS named the same as the directory (e.g. bi-card/card.css for
        # bi-card; tip-panels/tip-panels.css for tip-panels). The legacy
        # bi-card uses `card.css` / `card.js`; everything else matches the
        # component name. Probe both, prefer the directory-named file.
        css_candidates = [comp_dir / f"{name}.css", comp_dir / "card.css"]
        css_src = next((p for p in css_candidates if p.is_file()), None)
        if css_src is None:
            raise FileNotFoundError(
                f"missing CSS for component {name!r}; tried: "
                + ", ".join(str(p.relative_to(REPO_ROOT)) for p in css_candidates)
            )
        jobs.append((css_src, STYLES_GEN / f"{name}.css"))

        js_candidates = [comp_dir / f"{name}.js", comp_dir / "card.js"]
        js_src = next((p for p in js_candidates if p.is_file()), None)
        if js_src is None:
            raise FileNotFoundError(
                f"missing JS for component {name!r}; tried: "
                + ", ".join(str(p.relative_to(REPO_ROOT)) for p in js_candidates)
            )
        jobs.append((js_src, JS_GEN / f"{name}.js"))

        partial = comp_dir / f"{name}.html.jinja"
        if partial.is_file():
            jobs.append((partial, TEMPLATES / f"{name}.html.jinja"))

    # Vendor: marked.js (markdown library used by tip-panels).
    jobs.append(
        (
            COMPONENTS_DIR / "vendor" / "marked.min.js",
            JS_GEN / "marked.min.js",
        )
    )

    # Group icon sprite.
    jobs.append(
        (
            DESIGN_SYSTEM_DIR / "assets" / "icons.svg",
            ASSETS / "icons.svg",
        )
    )

    return jobs


def _drift(src: Path, dst: Path) -> bool:
    if not dst.is_file():
        return True
    return src.read_bytes() != dst.read_bytes()


def main(argv: list[str]) -> int:
    check = "--check" in argv
    jobs = _build_jobs()

    drifted: list[Path] = []
    for src, dst in jobs:
        if not src.is_file():
            print(
                f"error: missing source {src.relative_to(REPO_ROOT)}",
                file=sys.stderr,
            )
            return 1
        if check:
            if _drift(src, dst):
                drifted.append(dst)
                print(
                    f"OUT OF SYNC: {dst.relative_to(REPO_ROOT)}",
                    file=sys.stderr,
                )
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(src.read_bytes())
            print(f"wrote {dst.relative_to(REPO_ROOT)}  ({src.stat().st_size:,} bytes)")

    if check and drifted:
        print(
            f"\n{len(drifted)} file(s) out of sync. "
            "Run `uv run python devtools/sync_render_html_styles.py` "
            "to refresh.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
