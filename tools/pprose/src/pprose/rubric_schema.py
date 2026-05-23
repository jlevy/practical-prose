"""Single source of truth for the practical-prose rubric structure.

Loads `rubric_schema.yaml` from this directory and exposes the canonical groups,
dimensions, version string, and rule counts as immutable Python objects.
Everything else (Pydantic models in `eval_report.py`, dimension lists in the
runtime, the comparison-table renderers, the prompts, the docs) derives from
this schema. Bumping a dimension, renaming one, or reordering groups happens in
the YAML file; the Python code reads counts via `dimension_count()` and the
like rather than hardcoding them.

The Pydantic score/reason models in `eval_report.py` are still defined as
explicit classes (Pydantic needs static field types), but their field names
must match the dimension keys in this schema. `verify_models_match_schema()`
asserts the alignment at module-import time of the test suite.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

_SCHEMA_PATH = Path(__file__).resolve().parent / "rubric_schema.yaml"


@dataclass(frozen=True)
class Dimension:
    key: str
    label: str
    section: int
    question: str
    rules: tuple[str, ...]
    group_key: str
    group_label: str


@dataclass(frozen=True)
class Group:
    key: str
    label: str
    dimensions: tuple[Dimension, ...]


def _load() -> tuple[str, tuple[Group, ...], dict[str, int], frozenset[str]]:
    data = yaml.safe_load(_SCHEMA_PATH.read_text(encoding="utf-8"))
    groups: list[Group] = []
    rule_counts: dict[str, int] = {}
    for g in data["groups"]:
        dims = tuple(
            Dimension(
                key=d["key"],
                label=d["label"],
                section=d["section"],
                question=d["question"],
                rules=tuple(d.get("rules", [])),
                group_key=g["key"],
                group_label=g["label"],
            )
            for d in g["dimensions"]
        )
        for d in dims:
            rule_counts[d.key] = len(d.rules)
        groups.append(Group(key=g["key"], label=g["label"], dimensions=dims))
    na_applicable = frozenset(data.get("na_applicable_dimensions", []))
    return data["version"], tuple(groups), rule_counts, na_applicable


# Sentinel for the "not applicable" score value.
# Score fields accept either an integer 0-5 or the string "NA".
NA: str = "NA"

RUBRIC_VERSION: str
GROUPS: tuple[Group, ...]
RULE_COUNTS: dict[str, int]
NA_APPLICABLE_DIMENSIONS: frozenset[str]
RUBRIC_VERSION, GROUPS, RULE_COUNTS, NA_APPLICABLE_DIMENSIONS = _load()

DIMENSIONS: tuple[Dimension, ...] = tuple(d for g in GROUPS for d in g.dimensions)

# Convenience lookups derived from GROUPS / DIMENSIONS.
DIMENSIONS_BY_KEY: dict[str, Dimension] = {d.key: d for d in DIMENSIONS}
DIMENSIONS_BY_LABEL: dict[str, Dimension] = {d.label: d for d in DIMENSIONS}
DIMENSIONS_BY_SECTION: dict[int, Dimension] = {d.section: d for d in DIMENSIONS}
GROUPS_BY_KEY: dict[str, Group] = {g.key: g for g in GROUPS}


def dimension_count() -> int:
    return len(DIMENSIONS)


def group_count() -> int:
    return len(GROUPS)


def group_for_dimension(dim_key: str) -> Group:
    return GROUPS_BY_KEY[DIMENSIONS_BY_KEY[dim_key].group_key]


def dimensions_in_group(group_key: str) -> tuple[Dimension, ...]:
    return GROUPS_BY_KEY[group_key].dimensions


def rule_count(dim_key_or_label: str) -> int:
    if dim_key_or_label in RULE_COUNTS:
        return RULE_COUNTS[dim_key_or_label]
    if dim_key_or_label in DIMENSIONS_BY_LABEL:
        return RULE_COUNTS[DIMENSIONS_BY_LABEL[dim_key_or_label].key]
    raise KeyError(dim_key_or_label)


def dimension_labels() -> tuple[str, ...]:
    return tuple(d.label for d in DIMENSIONS)


def dimension_keys() -> tuple[str, ...]:
    return tuple(d.key for d in DIMENSIONS)


def group_labels() -> tuple[str, ...]:
    return tuple(g.label for g in GROUPS)


def group_keys() -> tuple[str, ...]:
    return tuple(g.key for g in GROUPS)


def is_na_eligible(dim_key: str) -> bool:
    return dim_key in NA_APPLICABLE_DIMENSIONS
