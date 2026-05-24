"""Portable table-style metadata for Practical Prose eval outputs.

The metadata emitted here is a progressive enhancement for table-aware browsers.
Ordinary Markdown renderers can ignore it; the rendered table bodies stay valid
Markdown and do not depend on browser-specific code.

The palette is the runtime mirror of the canonical design system at
``tools/docs/design/design-system.md``.  Two design system rules are enforced
here:

* All colors are expressed as ``hsl(H S% L%)`` — no hex, no commas.
* Every palette has a light and a dark variant.  Light values live under the
  canonical palette name (e.g. ``practical_prose_groups``); dark values live
  under the same name with a ``_dark`` suffix (e.g.
  ``practical_prose_groups_dark``).  Renderers pick which to apply based on
  ``prefers-color-scheme`` or an explicit theme override.

Each group has one hue and one saturation that all of its members share; only
lightness moves to switch between light/dark mode and between
surface / ink / dim roles.
"""

from __future__ import annotations

from collections.abc import Sequence
from copy import deepcopy
from typing import Any

import yaml

from pprose import rubric_schema as rs

TableStyleMetadata = dict[str, Any]

# Group palette — light mode.  Background is the family surface tint; foreground
# is the family ink.  Both share the same H and S; only L differs.
_GROUP_STYLES_LIGHT: dict[str, dict[str, str]] = {
    "Purpose": {"background": "hsl(72 62% 92%)", "foreground": "hsl(72 62% 44%)"},
    "Expression": {"background": "hsl(206 59% 92%)", "foreground": "hsl(206 59% 44%)"},
    "Form": {"background": "hsl(30 60% 92%)", "foreground": "hsl(30 60% 38%)"},
    "Grounding": {"background": "hsl(162 55% 92%)", "foreground": "hsl(162 55% 40%)"},
    "Reasoning": {"background": "hsl(329 60% 92%)", "foreground": "hsl(329 60% 44%)"},
    "Judgment": {"background": "hsl(278 30% 92%)", "foreground": "hsl(278 30% 55%)"},
}

# Group palette — dark mode.  Same H and S as light; L flips so the surface is
# dim and the ink is light.
_GROUP_STYLES_DARK: dict[str, dict[str, str]] = {
    "Purpose": {"background": "hsl(72 62% 18%)", "foreground": "hsl(72 62% 68%)"},
    "Expression": {"background": "hsl(206 59% 18%)", "foreground": "hsl(206 59% 68%)"},
    "Form": {"background": "hsl(30 60% 18%)", "foreground": "hsl(30 60% 68%)"},
    "Grounding": {"background": "hsl(162 55% 16%)", "foreground": "hsl(162 55% 62%)"},
    "Reasoning": {"background": "hsl(329 60% 18%)", "foreground": "hsl(329 60% 68%)"},
    "Judgment": {"background": "hsl(278 30% 18%)", "foreground": "hsl(278 30% 72%)"},
}

# Score ramp — light mode.  Bad-to-good valence in red→amber→green, plus muted
# variants for 0 (not applicable to this document) and NA (not assessed).
_SCORE_STYLES_LIGHT: dict[str, dict[str, str | int | float]] = {
    "0": {"foreground": "hsl(220 10% 50%)", "font_weight": 400, "opacity": 0.75},
    "1": {"foreground": "hsl(0 70% 35%)", "font_weight": 800},
    "2": {"foreground": "hsl(28 80% 30%)", "font_weight": 650},
    "3": {"foreground": "hsl(40 80% 32%)", "font_weight": 700},
    "4": {"foreground": "hsl(140 60% 28%)", "font_weight": 750},
    "5": {"foreground": "hsl(140 60% 20%)", "font_weight": 850},
    "NA": {"foreground": "hsl(220 10% 50%)", "font_weight": 400, "opacity": 0.65},
}

# Score ramp — dark mode.  Same hues, lighter L so the colors read against a
# dark background.  Weight and opacity are mode-independent.
_SCORE_STYLES_DARK: dict[str, dict[str, str | int | float]] = {
    "0": {"foreground": "hsl(220 10% 60%)", "font_weight": 400, "opacity": 0.75},
    "1": {"foreground": "hsl(0 70% 60%)", "font_weight": 800},
    "2": {"foreground": "hsl(28 70% 60%)", "font_weight": 650},
    "3": {"foreground": "hsl(40 70% 60%)", "font_weight": 700},
    "4": {"foreground": "hsl(140 50% 55%)", "font_weight": 750},
    "5": {"foreground": "hsl(140 50% 45%)", "font_weight": 850},
    "NA": {"foreground": "hsl(220 10% 60%)", "font_weight": 400, "opacity": 0.65},
}


def _dimension_styles(group_styles: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    """Expand a group palette into a per-dimension palette.

    Each dimension inherits the surface and ink of its parent group.  Per-dim
    hue variation (the rotation around the group hue documented in
    `design-system.md`) is reserved for visualizations that draw the dim mark
    directly; for cell backgrounds in tables the uniform group color reads as
    a clearer block.
    """
    styles: dict[str, dict[str, str]] = {}
    for group in rs.GROUPS:
        base = group_styles[group.label]
        for dim in group.dimensions:
            styles[dim.label] = dict(base)
    return styles


def practical_prose_table_styles(
    *,
    comparison_labels: Sequence[str] | None = None,
) -> TableStyleMetadata:
    """Return the ``display.table_styles`` object for eval report tables.

    The returned object ships **both** light and dark palettes.  The convention
    is that a palette named ``practical_prose_groups`` carries the light values
    and the parallel palette ``practical_prose_groups_dark`` carries the dark
    values; same for ``practical_prose_dimensions`` and
    ``practical_prose_scores``.  Renderers switch to the ``_dark`` variant when
    the host is in dark mode (``prefers-color-scheme: dark`` or an explicit
    user override).

    ``comparison_labels`` is optional because single-document ``.eval.md``
    outputs can be described by their stable columns.  Comparison tables add
    one column per input artifact, so callers that know those labels can make
    the selector stricter.
    """
    comparison_columns = ["Approach", "Aspect", "Measure", *(comparison_labels or ())]

    return {
        "version": 1,
        "palettes": {
            "practical_prose_groups": deepcopy(_GROUP_STYLES_LIGHT),
            "practical_prose_groups_dark": deepcopy(_GROUP_STYLES_DARK),
            "practical_prose_dimensions": _dimension_styles(_GROUP_STYLES_LIGHT),
            "practical_prose_dimensions_dark": _dimension_styles(_GROUP_STYLES_DARK),
            "practical_prose_scores": deepcopy(_SCORE_STYLES_LIGHT),
            "practical_prose_scores_dark": deepcopy(_SCORE_STYLES_DARK),
        },
        "theme_alternates": {
            "practical_prose_groups": "practical_prose_groups_dark",
            "practical_prose_dimensions": "practical_prose_dimensions_dark",
            "practical_prose_scores": "practical_prose_scores_dark",
        },
        "tables": [
            {
                "id": "practical_prose_single_doc_qualitative",
                "match": {"columns": ["Group", "Dimension", "Score", "Reason"]},
                "encodings": [
                    {
                        "channel": "background",
                        "source": "row",
                        "field": "Dimension",
                        "palette": "practical_prose_dimensions",
                        "target": "row",
                    },
                    {
                        "channel": "foreground",
                        "source": "cell",
                        "field": "Score",
                        "palette": "practical_prose_scores",
                        "target": "cell",
                        "columns": ["Score"],
                    },
                    {
                        "channel": "font_weight",
                        "source": "cell",
                        "field": "Score",
                        "scale": {
                            "type": "linear",
                            "domain": [0, 5],
                            "range": [400, 850],
                        },
                        "target": "cell",
                        "columns": ["Score"],
                    },
                ],
                "headers": [
                    {
                        "match": {"column": "Score"},
                        "style": {"align": "center", "font_weight": 700},
                    }
                ],
            },
            {
                "id": "practical_prose_single_doc_quantitative",
                "match": {"columns": ["Section", "Measure", "Value"]},
                "headers": [
                    {
                        "match": {"column": "Value"},
                        "style": {"align": "right", "font_weight": 700},
                    }
                ],
            },
            {
                "id": "practical_prose_unified_comparison",
                "match": {"columns": comparison_columns},
                "encodings": [
                    {
                        "channel": "background",
                        "source": "row",
                        "field": "Measure",
                        "palette": "practical_prose_dimensions",
                        "target": "row",
                    }
                ],
                "headers": [
                    {
                        "match": {"column": "Measure"},
                        "style": {"font_weight": 700},
                    }
                ],
            },
        ],
    }


def with_practical_prose_display_metadata(
    data: dict[str, Any],
    *,
    comparison_labels: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Copy ``data`` and add default display metadata when none is already present."""
    out = deepcopy(data)
    display = out.setdefault("display", {})
    if not isinstance(display, dict):
        return out
    display.setdefault(
        "table_styles",
        practical_prose_table_styles(comparison_labels=comparison_labels),
    )
    return out


def render_table_style_frontmatter(
    *,
    comparison_labels: Sequence[str] | None = None,
) -> str:
    """Render a YAML frontmatter block containing only display metadata."""
    data = {
        "display": {
            "table_styles": practical_prose_table_styles(comparison_labels=comparison_labels)
        },
    }
    frontmatter = yaml.safe_dump(
        data,
        sort_keys=True,
        default_flow_style=False,
        indent=2,
        allow_unicode=True,
    )
    return f"---\n{frontmatter}---"
