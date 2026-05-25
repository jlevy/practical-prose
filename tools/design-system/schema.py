"""Pydantic schema for the Practical Prose design-system YAML.

This is the Python-side validation gate for ``design-system.yaml``.
``generate.py`` parses the YAML through these models, then emits the JS / CSS /
Python derivatives.  Any YAML edit that breaks the contract fails at generation
time, so consumers always get a validated payload.

The mirror schema on the JS/TS side lives at ``lib/design-system.js`` (Zod).
Both schemas describe the same shape; keep them in sync when adding fields.

Conventions echoed from ``design-system.md``:
- HSL is the only color primitive (three components: h, s, l).
- "Spread" is a separate group-level setting (the H range across a group's
  dimensions); not part of any single color.
- Every color has a light and a dark value; the pair is the unit.
- Within a group, H and S are family constants.  Lightness alone moves between
  light/dark and between surface / ink / dim roles.  Per-dimension H drifts a
  few degrees from the group hue via ``h_offset``.
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Matches the modern space-separated HSL syntax this project standardizes on,
# optionally with an alpha component using slash syntax.  Rejects commas inside
# the parentheses and any other color function (rgb, hex, etc).
HSL_PATTERN = re.compile(
    r"^hsl\(\s*\d+(?:\.\d+)?\s+\d+(?:\.\d+)?%\s+\d+(?:\.\d+)?%(?:\s*/\s*\d*(?:\.\d+)?)?\s*\)$"
)

GroupId = Literal["P", "E", "F", "G", "R", "J"]
DimId = str  # validated by regex in Dimension.id_must_match_pattern
ScoreLevel = Literal["0", "1", "2", "3", "4", "5", "NA", "ERR"]


class _Frozen(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class HslString(str):
    """An ``hsl(H S% L%)`` string (modern space-separated form).

    Pydantic v2 accepts plain ``str`` here; we validate via field_validator on
    the parents that use HSL strings.
    """


def _validate_hsl(v: str) -> str:
    if not isinstance(v, str) or not HSL_PATTERN.match(v):
        raise ValueError(
            f"expected hsl(H S% L%) — got {v!r}.  "
            "Use the modern space-separated form: hsl(40 38% 93%) — no commas, no hex."
        )
    return v


# ──────────────── Surface tokens ────────────────


class LightDarkHsl(_Frozen):
    """A light/dark pair of full HSL strings (used for page-level surfaces and scores)."""

    light: str
    dark: str

    @field_validator("light", "dark")
    @classmethod
    def _hsl(cls, v: str) -> str:
        return _validate_hsl(v)


class Surfaces(_Frozen):
    bg: LightDarkHsl
    fg: LightDarkHsl
    muted: LightDarkHsl
    card: LightDarkHsl
    border: LightDarkHsl
    rule: LightDarkHsl


# ──────────────── Groups ────────────────


class LightDarkLightness(_Frozen):
    """A light/dark pair of L values (0..100) used for tokens inside a group's
    hue family — H and S come from the group itself."""

    light: float = Field(ge=0, le=100)
    dark: float = Field(ge=0, le=100)


class Group(_Frozen):
    id: GroupId
    label: str = Field(min_length=1)
    h: float = Field(ge=0, le=360, description="Family hue, in degrees.")
    s: float = Field(ge=0, le=100, description="Family saturation, in percent.")
    spread: float = Field(
        ge=0,
        le=60,
        description=(
            "Total H range (in degrees) across this group's dimensions.  Documented "
            "design parameter — not part of any single color."
        ),
    )
    ink: LightDarkLightness
    surface: LightDarkLightness
    icon: str = Field(
        pattern=r"^[a-z0-9_-]+:[a-z0-9_-]+$",
        description="Iconify-style name: <prefix>:<icon> (e.g. mdi:compass-rose).",
    )
    sense: str = Field(min_length=1)


# ──────────────── Dimensions ────────────────


class Dimension(_Frozen):
    id: DimId
    label: str = Field(min_length=1)
    short: str = Field(min_length=1, max_length=10)
    group: GroupId
    h_offset: float = Field(
        ge=-30,
        le=30,
        description="Degrees of H drift from the group hue.  Combined: dim.h = group.h + h_offset.",
    )
    l: LightDarkLightness  # noqa: E741 — `l` mirrors the YAML key

    @field_validator("id")
    @classmethod
    def _id_pattern(cls, v: str) -> str:
        if not re.match(r"^[PEFGRJ]\d+$", v):
            raise ValueError(f"dimension id must match /^[PEFGRJ]\\d+$/, got {v!r}")
        return v


# ──────────────── Scores ────────────────


class Score(_Frozen):
    level: ScoreLevel
    color: LightDarkHsl
    weight: int = Field(ge=100, le=900)
    opacity: float | None = Field(default=None, ge=0, le=1)


# ──────────────── Root ────────────────


class DesignSystem(_Frozen):
    version: int = Field(ge=1)
    surfaces: Surfaces
    groups: list[Group]
    dimensions: list[Dimension]
    scores: list[Score]

    @field_validator("dimensions")
    @classmethod
    def _dim_groups_exist(cls, dims: list[Dimension]) -> list[Dimension]:
        # Cross-field check: every dimension's group must be declared.
        # Pydantic v2 doesn't expose siblings here, so we re-check in __init__
        # via model_validator below.  This validator only verifies id uniqueness.
        seen: set[str] = set()
        for d in dims:
            if d.id in seen:
                raise ValueError(f"duplicate dimension id: {d.id}")
            seen.add(d.id)
        return dims

    def model_post_init(self, _: object) -> None:
        # Cross-reference validation.
        group_ids = {g.id for g in self.groups}
        for d in self.dimensions:
            if d.group not in group_ids:
                raise ValueError(
                    f"dimension {d.id} references unknown group {d.group!r}; "
                    f"declared groups are {sorted(group_ids)}"
                )
        # Score levels must be unique.
        seen: set[str] = set()
        for s in self.scores:
            if s.level in seen:
                raise ValueError(f"duplicate score level: {s.level!r}")
            seen.add(s.level)


# ──────────────── Derivation helpers ────────────────
# These compute the fully-resolved HSL strings consumers need.  Kept here so
# both the generator and any future Python consumer share one implementation.


def fmt_hsl(h: float, s: float, lightness: float) -> str:
    """Format an HSL triple as the canonical modern string."""

    def n(x: float) -> str:
        # Drop trailing ".0" so integers stay integers in the output.
        return f"{x:g}"

    return f"hsl({n(h)} {n(s)}% {n(lightness)}%)"


def group_ink_color(g: Group, mode: Literal["light", "dark"]) -> str:
    lightness = g.ink.light if mode == "light" else g.ink.dark
    return fmt_hsl(g.h, g.s, lightness)


def group_surface_color(g: Group, mode: Literal["light", "dark"]) -> str:
    lightness = g.surface.light if mode == "light" else g.surface.dark
    return fmt_hsl(g.h, g.s, lightness)


def dim_color(d: Dimension, g: Group, mode: Literal["light", "dark"]) -> str:
    h = (g.h + d.h_offset) % 360
    lightness = d.l.light if mode == "light" else d.l.dark
    return fmt_hsl(h, g.s, lightness)
