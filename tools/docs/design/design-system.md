---
title: Practical Prose Design System
description: Colors, icons, scores, and shared visual conventions for any Practical Prose surface that displays rating data.
---
# Practical Prose Design System

Visual design guidance for any Practical Prose surface that displays rating data:
eval-report frontmatter, Markdown rollups, static HTML reports, comparison tables, and
any future renderer (terminal, PDF).

The runtime palette source of truth is
[`tools/pprose/src/pprose/table_styles.py`](../../pprose/src/pprose/table_styles.py).
This document is the human-readable rationale and the canonical color values.

> **Note**: The runtime currently emits hex codes that pre-date the HSL rule below.
> Migrate `table_styles.py` to `hsl()` when next touched.

## Color Policy

**Always express colors as `hsl()`, never as hex.**

Hex codes hide the structure of the system.
`hsl(H S% L%)` makes the relationships visible directly in the source: a reader can scan
down a column and see at a glance which colors share a hue (same family), which share a
lightness (same ramp position), and whether the system is internally consistent.

Concretely:

- Two values with matching `H` belong to the same family.
- Two values with matching `L` sit at the same ramp position.
- Surface vs ink for any one family share `H` and `S`; only `L` differs.

This applies to palette YAML, CSS, design tokens, and any structured color data the
project emits. Renderers convert to other color spaces at draw time (`colorsys` in the
stdlib handles ANSI fallbacks; no extra dependency needed).

Use slash syntax for alpha (`hsl(H S% L% / a)`) rather than a separate opacity field
when the schema allows it.

If perceptual uniformity across hues becomes a real contrast-tuning problem (yellow at
the same `L` reads visibly lighter than blue), consider `oklch(L C H)`. Default to
`hsl()`.

## Structure

The rubric has two display tiers.
Both share the same hue family.

| Tier | Visual weight | Role |
| --- | --- | --- |
| Group (5: Purpose, Expression, Grounding, Reasoning, Judgment) | Light surface, dark ink | Cards, section headers, group-mean rollups |
| Dimension (20, distributed across the 5 groups) | Darker mark, often with a small hue offset | Per-dimension row accents, score chips, drill-down headers |

Scores are an **orthogonal axis** with their own red-to-green valence ramp.
Score color is independent of which dimension or group is being scored.

## Group Palette

Each group claims one hue.
Dimensions within the group stay inside that hue’s neighborhood, stepping along
lightness (and optionally a few degrees of hue) to give each dimension a distinguishable
sub-hue.

| Group | Hue | Surface | Ink | Icon |
| --- | --- | --- | --- | --- |
| Purpose | 214 (blue) | `hsl(214 60% 95%)` | `hsl(214 55% 25%)` | `mdi:compass-rose` |
| Expression | 140 (green) | `hsl(140 50% 94%)` | `hsl(140 55% 22%)` | `mdi:quill` |
| Grounding | 38 (amber) | `hsl(38 80% 93%)` | `hsl(38 80% 22%)` | `mdi:anchor` |
| Reasoning | 265 (violet) | `hsl(265 55% 95%)` | `hsl(265 65% 32%)` | `mdi:ruler` |
| Judgment | 348 (rose) | `hsl(348 75% 95%)` | `hsl(348 55% 30%)` | `mdi:scale-balance` |

## Dimension Palette

Dimensions inherit their group’s hue family.
The `H` column reveals family; the `L` column reveals ramp position inside that family.

| Dimension | Group | Color |
| --- | --- | --- |
| Suitability | Purpose | `hsl(210 55% 40%)` |
| Scope | Purpose | `hsl(214 55% 35%)` |
| Breadth | Purpose | `hsl(218 55% 30%)` |
| Depth | Purpose | `hsl(222 55% 25%)` |
| Clarity | Expression | `hsl(132 50% 35%)` |
| Coherence | Expression | `hsl(138 50% 32%)` |
| Concision | Expression | `hsl(144 50% 30%)` |
| Organization | Expression | `hsl(150 50% 28%)` |
| Consistency | Expression | `hsl(156 50% 26%)` |
| Formatting | Expression | `hsl(162 50% 24%)` |
| Verifiability | Grounding | `hsl(34 75% 32%)` |
| Factuality | Grounding | `hsl(40 75% 28%)` |
| Relevance | Grounding | `hsl(46 75% 26%)` |
| Discipline | Reasoning | `hsl(258 60% 38%)` |
| Soundness | Reasoning | `hsl(265 60% 35%)` |
| Precision | Reasoning | `hsl(272 60% 32%)` |
| Parsimony | Reasoning | `hsl(279 60% 30%)` |
| Calibration | Judgment | `hsl(342 45% 38%)` |
| Fairness | Judgment | `hsl(348 45% 35%)` |
| Robustness | Judgment | `hsl(354 45% 32%)` |

## Score Palette

The score ramp is orthogonal to family.
It is a valence axis (bad to good) plus a muted variant for `0` (not applicable to this
document) and `NA` (not assessed).

| Score | Color | Weight | Opacity |
| --- | --- | --- | --- |
| `0` | `hsl(220 10% 50%)` | 400 | 0.75 |
| `1` | `hsl(0 70% 35%)` | 800 | — |
| `2` | `hsl(28 80% 30%)` | 650 | — |
| `3` | `hsl(40 80% 32%)` | 700 | — |
| `4` | `hsl(140 60% 28%)` | 750 | — |
| `5` | `hsl(140 60% 20%)` | 850 | — |
| `NA` | `hsl(220 10% 50%)` | 400 | 0.65 |

Font weight tracks score strength; opacity is reserved for the muted `0` and `NA`
states.

## Icons

Each top-level group has one icon, drawn from
[Material Design Icons (MDI)](https://pictogrammers.com/library/mdi/) (Apache 2.0). MDI
was chosen for the timeless, instrument-flavored draftsmanship of these particular
icons: a compass rose, a writing tool, a fixed point, a measuring tool, and a weighing
tool — a navigator’s drafting kit.

Store the **name**, not a glyph, so the design system stays independent of font and
Unicode availability.
The local SVGs are inlined verbatim with attribution in a leading XML comment.

| Group | Name | Local file | Sense |
| --- | --- | --- | --- |
| Purpose | `mdi:compass-rose` | [purpose.svg](assets/icons/purpose.svg) | orientation toward the reader’s task |
| Expression | `mdi:quill` | [expression.svg](assets/icons/expression.svg) | language, surface form |
| Grounding | `mdi:anchor` | [grounding.svg](assets/icons/grounding.svg) | tied to sources and facts |
| Reasoning | `mdi:ruler` | [reasoning.svg](assets/icons/reasoning.svg) | inference, measurement, rigor |
| Judgment | `mdi:scale-balance` | [judgment.svg](assets/icons/judgment.svg) | weighing claims, calibration |

### Presentation modes

Three canonical presentations.
Stay inside this set unless the design system grows a new one.

1. **Inline** — icon-as-glyph in flowing text, sized to the surrounding type.
   The default, used in body copy, table cells, and chart legends.
2. **Outlined badge** — icon framed in a thin square, rounded square, or hairline
   circle. Used for column headers, group cards, and section bugs where a frame helps the
   icon read as a label rather than as decoration.
3. **Solid stamp** — a filled circle (or rounded square) in the group’s ink color, with
   the icon rendered in the page’s surface color so it appears cut out.
   The wax-seal treatment.
   Used for the strongest visual anchors: report headers, navigation chips, dimension
   medallions in summary visualizations.

#### Inline

Inline the SVG from [`assets/icons/`](assets/icons/) directly.
All five use `fill="currentColor"`, so they inherit the surrounding CSS color.
Pair with the group’s ink color via one `color:` declaration:

```html
<span class="dim dim--purpose">
  <!-- contents of assets/icons/purpose.svg -->
  <svg viewBox="0 0 24 24" width="1em" height="1em"><path fill="currentColor" d="…"/></svg>
  Purpose
</span>
```

```css
.dim         { display: inline-flex; align-items: center; gap: 0.35em; }
.dim--purpose    { color: hsl(214 55% 25%); }
.dim--expression { color: hsl(140 55% 22%); }
.dim--grounding  { color: hsl(38 80% 22%); }
.dim--reasoning  { color: hsl(265 65% 32%); }
.dim--judgment   { color: hsl(348 55% 30%); }
```

#### Outlined badge

A frame around the inline icon.
The frame border picks up the same ink color via `currentColor`:

```html
<span class="dim-badge dim--purpose">
  <svg viewBox="0 0 24 24" width="1em" height="1em"><path fill="currentColor" d="…"/></svg>
</span>
```

```css
.dim-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2em; height: 2em;
  border: 1.5px solid currentColor;
  border-radius: 25%;        /* square: 0; rounded square: 18-25%; circle: 50% */
  box-sizing: border-box;
  padding: 0.25em;
}
.dim-badge svg { width: 100%; height: 100%; }
```

#### Solid stamp (filled circle, cut-out icon)

The wax-seal treatment.
The container fills with the group’s ink color, and the inline SVG is set to the page’s
surface color so it reads as a cut-out:

```html
<span class="dim-stamp dim--purpose">
  <svg viewBox="0 0 24 24" width="1em" height="1em"><path fill="currentColor" d="…"/></svg>
</span>
```

```css
.dim-stamp {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.25em; height: 2.25em;
  border-radius: 50%;          /* circle; use 22% for rounded-square stamp */
  padding: 0.45em;
  box-sizing: border-box;
}
.dim-stamp svg { width: 100%; height: 100%; color: var(--paper, #ffffff); }

/* Background uses the group ink color; the SVG color is the paper color. */
.dim-stamp.dim--purpose    { background: hsl(214 55% 25%); }
.dim-stamp.dim--expression { background: hsl(140 55% 22%); }
.dim-stamp.dim--grounding  { background: hsl(38 80% 22%); }
.dim-stamp.dim--reasoning  { background: hsl(265 65% 32%); }
.dim-stamp.dim--judgment   { background: hsl(348 55% 30%); }
```

Sizing rule: the icon should occupy roughly 55-65% of the stamp’s diameter (set via
`padding` on the container, not by sizing the SVG). At small sizes (< 24px diameter)
prefer the rounded-square variant (`border-radius: 22%`) for legibility.

The `--paper` variable should resolve to the page or card surface color, so the cut-out
matches the medium the stamp sits on (default: `#ffffff`; on the cream-paper demo
surface, `hsl(38 80% 95%)` or similar).
If a renderer cannot resolve a custom property, hard-code the surface color used by that
medium.

#### External-file reference (`<img>` or CSS `mask`)

When the icon must be loaded as a separate file (e.g. email, Markdown renderers that
strip inline SVG), use `<img>` for fixed-color cases or CSS `mask-image` for recolorable
cases:

```html
<img src="assets/icons/purpose.svg" width="20" height="20" alt="Purpose">
```

`<img>` cannot recolor a `currentColor` SVG. For recoloring without inlining, use
`mask-image`:

```css
.icon-purpose {
  width: 1em; height: 1em;
  background-color: hsl(214 55% 25%);
  mask-image: url("assets/icons/purpose.svg");
  mask-size: contain; mask-repeat: no-repeat;
}
```

#### Terminal / plain text

Maintain a small lookup that maps each name to a Unicode glyph, with a two-letter group
abbreviation as final fallback (`Pu`, `Ex`, `Gr`, `Re`, `Ju`).

## Adding or Changing Colors

When proposing palette changes:

1. Keep all values in `hsl()`. No hex, no `rgb()`.
2. Adjust one axis at a time (hue, saturation, or lightness) so the rationale is
   inspectable in the diff.
3. Stay inside the family hue range for dimensions; if a dimension needs to move outside
   its family’s neighborhood, the group assignment is the problem, not the color.
4. Verify contrast for surface/ink pairs at minimum WCAG AA (4.5:1 for body text).
   Tooling like the `contrast-ratio` CLI or any browser devtools color picker is
   sufficient.

## References

- [`tools/pprose/src/pprose/table_styles.py`](../../pprose/src/pprose/table_styles.py) —
  runtime source of truth for the palette (currently hex; migrate to `hsl()`).
- [`tools/pprose/src/pprose/rubric_schema.yaml`](../../pprose/src/pprose/rubric_schema.yaml)
  — defines the group and dimension keys this palette binds to.
- [`tools/docs/project/specs/active/plan-2026-05-23-rendered-eval-reports.md`](../project/specs/active/plan-2026-05-23-rendered-eval-reports.md)
  — in-flight plan that will consume this system in the HTML renderer.
