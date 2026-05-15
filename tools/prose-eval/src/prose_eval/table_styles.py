"""Portable table-style metadata for Practical Prose eval outputs.

The metadata emitted here is a progressive enhancement for table-aware browsers.
Ordinary Markdown renderers can ignore it; the rendered table bodies stay valid
Markdown and do not depend on browser-specific code.
"""

from __future__ import annotations

from collections.abc import Sequence
from copy import deepcopy
from typing import Any

import yaml

from prose_eval import rubric_schema as rs

TableStyleMetadata = dict[str, Any]

_GROUP_STYLES: dict[str, dict[str, str]] = {
    "Purpose": {"background": "#eaf2ff", "foreground": "#173b68"},
    "Expression": {"background": "#eaf7ec", "foreground": "#175c36"},
    "Grounding": {"background": "#fff6db", "foreground": "#6b4a03"},
    "Reasoning": {"background": "#f3ecff", "foreground": "#4c1d95"},
    "Judgment": {"background": "#fff0f3", "foreground": "#8a1232"},
}

_SCORE_STYLES: dict[str, dict[str, str | int | float]] = {
    "0": {"foreground": "#6b7280", "font_weight": 400, "opacity": 0.75},
    "1": {"foreground": "#991b1b", "font_weight": 800},
    "2": {"foreground": "#92400e", "font_weight": 650},
    "3": {"foreground": "#a16207", "font_weight": 700},
    "4": {"foreground": "#166534", "font_weight": 750},
    "5": {"foreground": "#14532d", "font_weight": 850},
    "NA": {"foreground": "#6b7280", "font_weight": 400, "opacity": 0.65},
}


def _dimension_styles() -> dict[str, dict[str, str]]:
    styles: dict[str, dict[str, str]] = {}
    for group in rs.GROUPS:
        group_style = _GROUP_STYLES[group.label]
        for dim in group.dimensions:
            styles[dim.label] = dict(group_style)
    return styles


def practical_prose_table_styles(
    *,
    comparison_labels: Sequence[str] | None = None,
) -> TableStyleMetadata:
    """Return the v1 `display.table_styles` object for eval report tables.

    `comparison_labels` is optional because single-document `.eval.md` outputs can
    be described by their stable columns. Comparison tables add one column per input
    artifact, so callers that know those labels can make the selector stricter.
    """
    comparison_columns = ["Approach", "Aspect", "Measure", *(comparison_labels or ())]

    return {
        "version": 1,
        "palettes": {
            "practical_prose_groups": deepcopy(_GROUP_STYLES),
            "practical_prose_dimensions": _dimension_styles(),
            "practical_prose_scores": deepcopy(_SCORE_STYLES),
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


def practical_prose_display_metadata(
    *,
    comparison_labels: Sequence[str] | None = None,
) -> TableStyleMetadata:
    """Return a `display` metadata object containing Practical Prose table styles."""
    return {
        "table_styles": practical_prose_table_styles(comparison_labels=comparison_labels),
    }


def with_practical_prose_display_metadata(
    data: dict[str, Any],
    *,
    comparison_labels: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Copy `data` and add default display metadata when none is already present."""
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
        "display": practical_prose_display_metadata(comparison_labels=comparison_labels),
    }
    frontmatter = yaml.safe_dump(
        data,
        sort_keys=True,
        default_flow_style=False,
        indent=2,
        allow_unicode=True,
    )
    return f"---\n{frontmatter}---"
