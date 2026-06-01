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

GroupId = Literal["P", "E", "F", "R", "G", "J"]
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


class Tones(_Frozen):
    """Mode-independent tone tokens used in chrome decoration.

    Each value is a single ``hsl()`` string applied identically in light
    and dark mode (overriding any per-mode fallbacks in the viz).
    """

    icon: str = Field(min_length=1)
    dim_label: str = Field(min_length=1)
    na: str = Field(min_length=1)
    na_label: str = Field(min_length=1)

    @field_validator("icon", "dim_label", "na", "na_label")
    @classmethod
    def _hsl(cls, v: str) -> str:
        return _validate_hsl(v)


# ──────────────── Groups ────────────────


class LightDarkLightness(_Frozen):
    """A light/dark pair of L values (0..100) used for tokens inside a group's
    hue family — H and S come from the group itself."""

    light: float = Field(ge=0, le=100)
    dark: float = Field(ge=0, le=100)


class Group(_Frozen):
    id: GroupId
    label: str = Field(min_length=1)
    spread: float = Field(
        ge=0,
        le=60,
        description=(
            "Total H range (in degrees) across this group's dimensions.  Documented "
            "design parameter — not part of any single color."
        ),
    )
    ink_light: str = Field(min_length=1, description="hsl(H S% L%) for light mode ink.")
    ink_dark: str = Field(min_length=1, description="hsl(H S% L%) for dark mode ink.")
    surface_light: str = Field(min_length=1)
    surface_dark: str = Field(min_length=1)
    icon: str = Field(
        pattern=r"^[a-z0-9_-]+:[a-z0-9_-]+$",
        description="Iconify-style name: <prefix>:<icon> (e.g. mdi:compass-rose).",
    )
    sense: str = Field(min_length=1)

    @field_validator("ink_light", "ink_dark", "surface_light", "surface_dark")
    @classmethod
    def _hsl(cls, v: str) -> str:
        return _validate_hsl(v)


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
        if not re.match(r"^[PEFRGJ]\d+$", v):
            raise ValueError(f"dimension id must match /^[PEFRGJ]\\d+$/, got {v!r}")
        return v


# ──────────────── Scores ────────────────


class Score(_Frozen):
    level: ScoreLevel
    color: LightDarkHsl
    weight: int = Field(ge=100, le=900)
    opacity: float | None = Field(default=None, ge=0, le=1)


# ──────────────── Interactions ────────────────


class HoverTokens(_Frozen):
    """Hover affordance tokens — theme-independent.

    ``bg`` / ``bg_strong`` are translucent neutral grays that lift subtly on any
    background (light or dark) without committing to a hue.  ``duration`` is a
    CSS time string; ``easing`` is a CSS timing-function string.
    """

    bg: str = Field(min_length=1)
    bg_strong: str = Field(min_length=1)
    duration: str = Field(pattern=r"^\d+m?s$")
    easing: str = Field(min_length=1)


class Interactions(_Frozen):
    hover: HoverTokens


# ──────────────── Typography ────────────────


class CapsTokens(_Frozen):
    """Small-caps eyebrow tracking — the one piece of the eyebrow pattern that
    isn't derivable from the font weight tokens.  Per ``design-system.md`` the
    letter-spacing rule fires only on uppercase text, so every consumer that
    opts into small caps reaches for ``--tracking-caps``.

    Weight came from here historically; it now collapses to ``fonts.sans.weight_bold``
    (see ``--weight-caps`` derivation in ``generate.py``).
    """

    tracking: str = Field(min_length=1)


# Font source — drives generated ``@font-face`` emission.
FontSource = str  # validated by regex below


_SOURCE_PATTERN = re.compile(r"^(system|fontsource:[a-z0-9-]+(?::vf)?)$")


def _validate_font_source(v: str) -> str:
    if not isinstance(v, str) or not _SOURCE_PATTERN.match(v):
        raise ValueError(
            f"font source must be `system` or `fontsource:<font-id>[:vf]`; got {v!r}"
        )
    return v


class FontRole(_Frozen):
    """One role's worth of font configuration (sans or serif).

    ``family`` is the primary font (what ``@font-face`` declares and what the
    generated CSS stack leads with).  ``stack`` is the fallback list appended
    after the primary family.  ``source`` tells the generator how to load the
    primary: ``system`` skips ``@font-face`` (rely on locally-installed fonts);
    ``fontsource:<id>[:vf]`` emits the standard fontsource CDN cuts.
    """

    family: str = Field(min_length=1)
    stack: str = Field(min_length=1)
    source: FontSource = Field(min_length=1)
    size_px: float = Field(ge=8, le=32)
    weight: int = Field(ge=100, le=900)
    weight_medium: int = Field(ge=100, le=900)
    weight_bold: int = Field(ge=100, le=900)

    @field_validator("source")
    @classmethod
    def _src(cls, v: str) -> str:
        return _validate_font_source(v)


class FontsTokens(_Frozen):
    sans: FontRole
    serif: FontRole


class Typography(_Frozen):
    caps: CapsTokens
    fonts: FontsTokens


# ──────────────── Scoring presentation ────────────────


class Scoring(_Frozen):
    """Score-value-driven presentation tokens.

    `alpha_step` modulates how vivid a scored mark reads: bar fills and
    score chips mix with `transparent` by ``(5 - score) * alpha_step``
    so a 5 reads vivid and a 1 reads faint.  The effect is symmetric in
    light + dark mode because the surface shows through the alpha.
    """

    alpha_step: float = Field(ge=0, le=0.5)


# ──────────────── Root ────────────────


class DesignSystem(_Frozen):
    version: int = Field(ge=1)
    surfaces: Surfaces
    tones: Tones
    groups: list[Group]
    dimensions: list[Dimension]
    scores: list[Score]
    interactions: Interactions
    typography: Typography
    scoring: Scoring

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


_HSL_PARSE = re.compile(r"^hsl\(\s*([\d.]+)\s+([\d.]+)%\s+([\d.]+)%(?:\s*/\s*[\d.]+)?\s*\)$")


def _parse_hsl(s: str) -> tuple[float, float, float]:
    """Parse 'hsl(H S% L%)' → (h, s, l) tuple."""
    m = _HSL_PARSE.match(s)
    if not m:
        raise ValueError(f"bad HSL string: {s!r}")
    return float(m.group(1)), float(m.group(2)), float(m.group(3))


def group_hs(g: Group) -> tuple[float, float]:
    """Family (H, S) — the constants every member of the group shares.

    Read from the LIGHT ink as the canonical source; light/dark vary only L."""
    h, s, _ = _parse_hsl(g.ink_light)
    return h, s


def group_ink_color(g: Group, mode: Literal["light", "dark"]) -> str:
    return g.ink_light if mode == "light" else g.ink_dark


def group_surface_color(g: Group, mode: Literal["light", "dark"]) -> str:
    return g.surface_light if mode == "light" else g.surface_dark


def dim_color(d: Dimension, g: Group, mode: Literal["light", "dark"]) -> str:
    gh, gs = group_hs(g)
    h = (gh + d.h_offset) % 360
    lightness = d.l.light if mode == "light" else d.l.dark
    return fmt_hsl(h, gs, lightness)
