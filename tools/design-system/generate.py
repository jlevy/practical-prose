#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pyyaml==6.0.3",
#   "pydantic==2.13.4",
# ]
# ///
"""CLI: validate ``design-system.yaml`` and emit derivative JS / CSS / Python.

Run with::

    uv run --script tools/design-system/generate.py

Or, to verify that generated files are up-to-date without rewriting them
(useful for pre-commit / CI)::

    uv run --script tools/design-system/generate.py --check

Outputs (all under ``_generated/`` folders; never edit by hand):
    tools/design-system/_generated/design_system.js
    tools/design-system/_generated/design_system.global.js
    tools/design-system/_generated/design_system.css
    tools/pprose/src/pprose/_generated/design_system.py

The YAML is the single source of truth.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

# Allow running this script directly without installing it as a package.
sys.path.insert(0, str(Path(__file__).parent))

from schema import (  # noqa: E402 — adjusted path above
    DesignSystem,
    Dimension,
    Group,
    Score,
    dim_color,
    group_ink_color,
    group_surface_color,
)

# Resolve project paths relative to this file so the script runs from anywhere.
# Layout: <repo>/tools/design-system/generate.py — parents[2] is the repo root.
REPO_ROOT = Path(__file__).resolve().parents[2]
DESIGN_DIR = Path(__file__).resolve().parent
YAML_PATH = DESIGN_DIR / "design-system.yaml"
GEN_DIR = DESIGN_DIR / "_generated"
JS_OUT = GEN_DIR / "design_system.js"
JS_GLOBAL_OUT = GEN_DIR / "design_system.global.js"
CSS_OUT = GEN_DIR / "design_system.css"
PY_OUT = REPO_ROOT / "tools/pprose/src/pprose/_generated/design_system.py"

# The name attached to `window` by the global-script variant.  Stable contract
# — HTML consumers reference `window.PracticalProseDesignSystem`.
GLOBAL_NAME = "PracticalProseDesignSystem"

HEADER_NOTICE = (
    "AUTO-GENERATED from tools/design-system/design-system.yaml — do not edit by hand.\n"
    "Regenerate with: uv run --script tools/design-system/generate.py"
)


# ──────────────── Resolve YAML into a fully-derived plain dict ────────────────


def _resolve(ds: DesignSystem) -> dict:
    """Return a plain dict with all derived HSL strings expanded.

    Groups grow ``ink: {light, dark}`` and ``surface: {light, dark}`` as full
    ``hsl(...)`` strings (the YAML only carries the L values).  Dimensions
    grow ``color: {light, dark}`` from group H/S plus per-dim H offset and L.
    Other fields pass through unchanged.
    """
    groups_by_id: dict[str, Group] = {g.id: g for g in ds.groups}

    def group_dict(g: Group) -> dict:
        return {
            "id": g.id,
            "label": g.label,
            "spread": g.spread,
            "ink": {
                "light": group_ink_color(g, "light"),
                "dark": group_ink_color(g, "dark"),
            },
            "surface": {
                "light": group_surface_color(g, "light"),
                "dark": group_surface_color(g, "dark"),
            },
            "icon": g.icon,
            "sense": g.sense,
        }

    def dim_dict(d: Dimension) -> dict:
        g = groups_by_id[d.group]
        return {
            "id": d.id,
            "label": d.label,
            "short": d.short,
            "group": d.group,
            "h_offset": d.h_offset,
            "color": {
                "light": dim_color(d, g, "light"),
                "dark": dim_color(d, g, "dark"),
            },
        }

    def score_dict(s: Score) -> dict:
        out = {
            "level": s.level,
            "color": {"light": s.color.light, "dark": s.color.dark},
            "weight": s.weight,
        }
        if s.opacity is not None:
            out["opacity"] = s.opacity
        return out

    return {
        "version": ds.version,
        "surfaces": ds.surfaces.model_dump(),
        "tones": ds.tones.model_dump(),
        "groups": [group_dict(g) for g in ds.groups],
        "dimensions": [dim_dict(d) for d in ds.dimensions],
        "scores": [score_dict(s) for s in ds.scores],
        "interactions": ds.interactions.model_dump(),
        "typography": ds.typography.model_dump(),
        "scoring": ds.scoring.model_dump(),
    }


# ──────────────── Emitters ────────────────


def _js_literal(value: object, indent: int = 0) -> str:
    """Render a Python value as compact JS using JSON (objects, arrays, strings,
    numbers, null).  JSON is a valid JS expression."""
    return json.dumps(value, indent=2 if indent else None, ensure_ascii=False)


def emit_js(resolved: dict) -> str:
    body = json.dumps(resolved, indent=2, ensure_ascii=False)
    return (
        f"/* {HEADER_NOTICE} */\n"
        "\n"
        "/** The full resolved Practical Prose design system. */\n"
        f"export const designSystem = Object.freeze({body});\n"
        "\n"
        "/** Convenience accessors keyed by id. */\n"
        "export const groupsById     = Object.freeze(Object.fromEntries(designSystem.groups.map(g => [g.id, g])));\n"
        "export const dimensionsById = Object.freeze(Object.fromEntries(designSystem.dimensions.map(d => [d.id, d])));\n"
        "export const scoresByLevel  = Object.freeze(Object.fromEntries(designSystem.scores.map(s => [s.level, s])));\n"
    )


def emit_js_global(resolved: dict) -> str:
    """Plain-script variant that attaches to ``window``.

    Needed because ES-module imports don't work from ``file://`` URLs in most
    browsers — and the design-system HTML pages are opened that way for quick
    iteration.  HTML consumers reference ``window.PracticalProseDesignSystem``.
    """
    body = json.dumps(resolved, indent=2, ensure_ascii=False)
    return (
        f"/* {HEADER_NOTICE} */\n"
        "\n"
        "(function () {\n"
        f"  const designSystem = Object.freeze({body});\n"
        "  const groupsById     = Object.freeze(Object.fromEntries(designSystem.groups.map(g => [g.id, g])));\n"
        "  const dimensionsById = Object.freeze(Object.fromEntries(designSystem.dimensions.map(d => [d.id, d])));\n"
        "  const scoresByLevel  = Object.freeze(Object.fromEntries(designSystem.scores.map(s => [s.level, s])));\n"
        f"  globalThis.{GLOBAL_NAME} = Object.freeze({{ designSystem, groupsById, dimensionsById, scoresByLevel }});\n"
        "})();\n"
    )


def emit_css(resolved: dict) -> str:
    surfaces = resolved["surfaces"]
    groups = resolved["groups"]
    dims = resolved["dimensions"]
    scores = resolved["scores"]

    def vars_for(mode: str) -> list[str]:
        lines: list[str] = []
        # Surface tokens
        for name, v in surfaces.items():
            lines.append(f"  --{name}: {v[mode]};")
        lines.append("")
        # Group ink (--accent-*)
        lines.append("  /* Group ink (primary accent per group) */")
        for g in groups:
            lines.append(f"  --accent-{g['id'].lower()}: {g['ink'][mode]};")
        lines.append("")
        # Group surface (--surface-*)
        lines.append("  /* Group surface (pale family-hue background) */")
        for g in groups:
            lines.append(f"  --surface-{g['id'].lower()}: {g['surface'][mode]};")
        lines.append("")
        # Per-dimension colors (--dim-*)
        lines.append("  /* Per-dimension colors */")
        for d in dims:
            lines.append(f"  --dim-{d['id']}: {d['color'][mode]};")
        lines.append("")
        # Score ramp (--score-*)
        lines.append("  /* Score valence ramp (orthogonal to family) */")
        for s in scores:
            level = s["level"].lower()
            lines.append(f"  --score-{level}: {s['color'][mode]};")
        return lines

    light_vars = "\n".join(vars_for("light"))
    dark_vars = "\n".join(vars_for("dark"))

    # Score weight + opacity are theme-independent — emit once outside the
    # mode-specific blocks.
    weight_lines = ["  /* Score font weights + opacities (theme-independent) */"]
    for s in scores:
        level = s["level"].lower()
        weight_lines.append(f"  --score-{level}-weight: {s['weight']};")
        if "opacity" in s:
            weight_lines.append(f"  --score-{level}-opacity: {s['opacity']};")
    weight_block = "\n".join(weight_lines)

    # Interaction tokens — theme-independent (translucent grays + CSS time
    # values).  Emitted once at the top of :root so they're inherited everywhere.
    interactions = resolved["interactions"]
    hover = interactions["hover"]
    interaction_lines = [
        "  /* Hover affordance (theme-independent) */",
        f"  --hover-bg: {hover['bg']};",
        f"  --hover-bg-strong: {hover['bg_strong']};",
        f"  --hover-duration: {hover['duration']};",
        f"  --hover-easing: {hover['easing']};",
        f"  --hover-transition: background-color {hover['duration']} {hover['easing']}, "
        f"color {hover['duration']} {hover['easing']}, "
        f"border-color {hover['duration']} {hover['easing']}, "
        f"transform {hover['duration']} {hover['easing']};",
    ]
    interaction_block = "\n".join(interaction_lines)

    # Typography tokens — small-caps eyebrow tracking + weights and
    # the numeric weight for quantitative readouts.  Theme-independent.
    # These travel together because the letter-spacing rule in
    # design-system.md fires only on uppercase text.
    caps = resolved["typography"]["caps"]
    numeric = resolved["typography"]["numeric"]
    typography_lines = [
        "  /* Typography — small-caps eyebrow tokens */",
        f"  --tracking-caps: {caps['tracking']};",
        f"  --weight-caps: {caps['weight']};",
        f"  --weight-caps-strong: {caps['weight_strong']};",
        "",
        "  /* Typography — quantitative numbers (scores, counts, stats) */",
        f"  --weight-num: {numeric['weight']};",
    ]
    typography_block = "\n".join(typography_lines)

    # Tone tokens — single mode-independent colors used in chrome
    # decoration (icons, dim labels, NA bg).  Edited live via the
    # Tone-overrides panel in the slider exploration HTML.
    tones = resolved["tones"]
    tone_lines = [
        "  /* Tones — mode-independent chrome tokens */",
        f"  --icon-color: {tones['icon']};",
        f"  --dim-label-color: {tones['dim_label']};",
        f"  --na-color: {tones['na']};",
    ]
    tone_block = "\n".join(tone_lines)

    # Scoring presentation — alpha step modulates how vivid a scored
    # mark reads.  Used by JS consumers to compute the bar / chip color
    # via `color-mix(in srgb, var(--dim-XN) <pct>%, transparent)`.
    scoring = resolved["scoring"]
    scoring_lines = [
        "  /* Scoring presentation — alpha modulation per score level */",
        f"  --score-alpha-step: {scoring['alpha_step']};",
    ]
    scoring_block = "\n".join(scoring_lines)

    return (
        f"/* {HEADER_NOTICE} */\n"
        "\n"
        ":root {\n"
        f"{light_vars}\n"
        "\n"
        f"{weight_block}\n"
        "\n"
        f"{interaction_block}\n"
        "\n"
        f"{typography_block}\n"
        "\n"
        f"{tone_block}\n"
        "\n"
        f"{scoring_block}\n"
        "}\n"
        "\n"
        "@media (prefers-color-scheme: dark) {\n"
        "  :root {\n"
        f"{dark_vars.replace(chr(10) + '  ', chr(10) + '    ')}\n"
        "  }\n"
        "}\n"
        "\n"
        "/* Explicit overrides — win over the media query when set. */\n"
        ':root[data-theme="dark"] {\n'
        f"{dark_vars}\n"
        "}\n"
        ':root[data-theme="light"] {\n'
        f"{light_vars}\n"
        "}\n"
    )


def emit_py(resolved: dict) -> str:
    # Use json.dumps for the data — it's valid Python for our subset (dicts of
    # str/int/float/None/list).  Avoids importing pprint and keeps formatting
    # deterministic.  json.dumps emits ``true/false/null`` though — we have
    # no booleans or nulls in this payload, so it's fine.
    body = json.dumps(resolved, indent=4, ensure_ascii=False)
    return (
        '"""AUTO-GENERATED from tools/design-system/design-system.yaml — do not edit by hand.\n'
        "\n"
        "Regenerate with::\n"
        "\n"
        "    uv run python tools/design-system/generate.py\n"
        '"""\n'
        "\n"
        "from __future__ import annotations\n"
        "\n"
        "from typing import Any\n"
        "\n"
        f"DESIGN_SYSTEM: dict[str, Any] = {body}\n"
        "\n"
        "# Convenience accessors keyed by id.\n"
        'GROUPS_BY_ID = {g["id"]: g for g in DESIGN_SYSTEM["groups"]}\n'
        'DIMENSIONS_BY_ID = {d["id"]: d for d in DESIGN_SYSTEM["dimensions"]}\n'
        'SCORES_BY_LEVEL = {s["level"]: s for s in DESIGN_SYSTEM["scores"]}\n'
    )


# ──────────────── Driver ────────────────


def _write(path: Path, content: str, *, check: bool) -> bool:
    """Write ``content`` to ``path``.  In check mode, only verify it matches.

    Returns True if any change would be (or was) made.
    """
    existing = path.read_text() if path.exists() else None
    if existing == content:
        return False
    if check:
        print(f"✗ {path.relative_to(REPO_ROOT)} is stale", file=sys.stderr)
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"✓ wrote {path.relative_to(REPO_ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify generated files match the YAML without rewriting them; "
        "exit non-zero if any are stale.",
    )
    args = parser.parse_args()

    raw = yaml.safe_load(YAML_PATH.read_text())
    ds = DesignSystem.model_validate(raw)
    resolved = _resolve(ds)

    js = emit_js(resolved)
    js_global = emit_js_global(resolved)
    css = emit_css(resolved)
    py = emit_py(resolved)

    stale = False
    stale |= _write(JS_OUT, js, check=args.check)
    stale |= _write(JS_GLOBAL_OUT, js_global, check=args.check)
    stale |= _write(CSS_OUT, css, check=args.check)
    stale |= _write(PY_OUT, py, check=args.check)

    if args.check and stale:
        print("\nRun without --check to regenerate.", file=sys.stderr)
        return 1
    if not args.check:
        print(
            f"\nValidated {len(ds.groups)} groups, {len(ds.dimensions)} dimensions, "
            f"{len(ds.scores)} scores."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
