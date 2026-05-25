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

## Color Policy

**Always express colors as `hsl()`, never as hex.** Use the modern space-separated form:
`hsl(H S% L%)` or `hsl(H S% L% / a)` for alpha — no commas inside the parentheses.

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

If perceptual uniformity across hues becomes a real contrast-tuning problem (yellow at
the same `L` reads visibly lighter than blue), consider `oklch(L C H)`. Default to
`hsl()`.

## Light & Dark Modes

Every color in the system has a **light** value and a **dark** value, and every surface
that consumes the palette is expected to support both.
The pair is the unit of color, not a single value with a “main” and a “fallback”.

| Aspect | Light mode | Dark mode |
| --- | --- | --- |
| Page surface | Cream / near-white (L ≈ 92–96%) | Near-black (L ≈ 8–12%) |
| Group surfaces | Pale tint of the family hue (L ≈ 92–95%) | Dim tint of the family hue (L ≈ 16–20%, S lowered) |
| Group ink | Dark, saturated (L ≈ 22–50%) | Light, slightly desaturated (L ≈ 60–72%) |
| Score ramp | Saturated dark colors (L ≈ 20–35%) | Saturated lighter colors (L ≈ 45–65%) |
| Muted (NA / 0) | Mid gray with opacity | Mid gray with opacity |

The same hue (`H`) is used across modes; only `L` (and sometimes `S`) flips.
A reader scanning down a column should see the same `H` in both light and dark for each
family — only the lightness flips.

### How to apply per surface

- **CSS / HTML**: define the light values on `:root`, then override the same tokens
  inside `@media (prefers-color-scheme: dark)` (and optionally inside
  `:root[data-theme="dark"]` for an explicit override).
  Surfaces read the tokens via `var(--…)` and never hard-code a value.
- **Python / YAML**: emit both palettes side-by-side.
  The convention is that a palette named `practical_prose_groups` carries the light
  values and the parallel palette `practical_prose_groups_dark` carries the dark values.
  The `_dark` suffix is a stable contract; renderers switch to it when in dark mode.
- **Terminal**: detect light/dark from `COLORFGBG` (or a `--theme` flag) and pick the
  appropriate ANSI mapping at render time.

### CSS variable naming convention

Surfaces that consume the palette in CSS should expose the tokens under stable, short
names at the `:root` level, then override the same names inside the dark media query.
Use single-letter group codes (`p / e / f / g / r / j`) in CSS so the tokens stay compact
at call sites:

```css
:root {
  --bg: hsl(40 38% 93%);            /* page background */
  --fg: hsl(30 12% 10%);            /* primary text */

  /* Group accents — the ink color of each group */
  --accent-p: hsl(72 62% 44%);      /* Purpose */
  --accent-e: hsl(206 59% 44%);     /* Expression */
  --accent-f: hsl(30 60% 38%);      /* Form */
  --accent-g: hsl(162 55% 40%);     /* Grounding */
  --accent-r: hsl(329 60% 44%);     /* Reasoning */
  --accent-j: hsl(278 30% 55%);     /* Judgment */

  /* Group surfaces — pale family-hue background tints (same H and S as the
     ink; only L is higher). */
  --surface-p: hsl(72 62% 92%);
  --surface-e: hsl(206 59% 92%);
  --surface-f: hsl(30 60% 92%);
  --surface-g: hsl(162 55% 92%);
  --surface-r: hsl(329 60% 92%);
  --surface-j: hsl(278 30% 92%);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: hsl(40 8% 8%);
    --fg: hsl(40 25% 88%);

    --accent-p: hsl(72 62% 68%);
    --accent-e: hsl(206 59% 68%);
    --accent-f: hsl(30 60% 68%);
    --accent-g: hsl(162 55% 62%);
    --accent-r: hsl(329 60% 68%);
    --accent-j: hsl(278 30% 72%);

    --surface-p: hsl(72 62% 18%);
    --surface-e: hsl(206 59% 18%);
    --surface-f: hsl(30 60% 18%);
    --surface-g: hsl(162 55% 16%);
    --surface-r: hsl(329 60% 18%);
    --surface-j: hsl(278 30% 18%);
  }
}
```

For YAML and Python the full group name (`Purpose`, `Expression`, ...) is used so the
data is self-describing without external knowledge of the short codes.

## Structure

The rubric has two display tiers.
Both share the same hue family.

| Tier | Visual weight | Role |
| --- | --- | --- |
| Group (6: Purpose, Expression, Form, Grounding, Reasoning, Judgment) | Light surface, dark ink | Cards, section headers, group-mean rollups |
| Dimension (20, distributed across the 6 groups) | Darker mark, often with a small hue offset | Per-dimension row accents, score chips, drill-down headers |

Scores are an **orthogonal axis** with their own red-to-green valence ramp.
Score color is independent of which dimension or group is being scored.

## Group Palette

Each group claims one hue.
Dimensions within the group stay inside that hue’s neighborhood, stepping along
lightness (and optionally a few degrees of hue) to give each dimension a distinguishable
sub-hue.

Each group has one hue and one saturation that all of its members (surface, ink,
dimensions) share. Lightness alone moves to switch between light/dark mode and between
surface / ink / dimension roles.

| Group | H | S | Surface (light) | Surface (dark) | Ink (light) | Ink (dark) | Icon |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Purpose | 72 | 62% | `hsl(72 62% 92%)` | `hsl(72 62% 18%)` | `hsl(72 62% 44%)` | `hsl(72 62% 68%)` | `mdi:compass-rose` |
| Expression | 206 | 59% | `hsl(206 59% 92%)` | `hsl(206 59% 18%)` | `hsl(206 59% 44%)` | `hsl(206 59% 68%)` | `mdi:quill` |
| Form | 30 | 60% | `hsl(30 60% 92%)` | `hsl(30 60% 18%)` | `hsl(30 60% 38%)` | `hsl(30 60% 68%)` | `mdi:scroll` |
| Grounding | 162 | 55% | `hsl(162 55% 92%)` | `hsl(162 55% 16%)` | `hsl(162 55% 40%)` | `hsl(162 55% 62%)` | `mdi:anchor` |
| Reasoning | 329 | 60% | `hsl(329 60% 92%)` | `hsl(329 60% 18%)` | `hsl(329 60% 44%)` | `hsl(329 60% 68%)` | `mdi:ruler` |
| Judgment | 278 | 30% | `hsl(278 30% 92%)` | `hsl(278 30% 18%)` | `hsl(278 30% 55%)` | `hsl(278 30% 72%)` | `mdi:scale-balance` |

## Dimension Palette

Dimensions inherit their group’s hue family.
The `H` column reveals family; the `L` column reveals ramp position inside that family.

Each dimension uses the same `S` as its group, rotates `H` a few degrees around the
group hue so its sub-family is distinguishable, and steps `L` so the ramp is readable
within the group. Dark variants share the same `H` and `S` and only shift `L` upward.

| Dimension | Group | Color (light) | Color (dark) |
| --- | --- | --- | --- |
| Suitability | Purpose | `hsl(68 62% 40%)` | `hsl(68 62% 65%)` |
| Scope | Purpose | `hsl(72 62% 37%)` | `hsl(72 62% 62%)` |
| Breadth | Purpose | `hsl(76 62% 34%)` | `hsl(76 62% 59%)` |
| Depth | Purpose | `hsl(80 62% 31%)` | `hsl(80 62% 56%)` |
| Clarity | Expression | `hsl(201 59% 35%)` | `hsl(201 59% 68%)` |
| Coherence | Expression | `hsl(204 59% 32%)` | `hsl(204 59% 66%)` |
| Concision | Expression | `hsl(207 59% 30%)` | `hsl(207 59% 64%)` |
| Organization | Form | `hsl(26 60% 38%)` | `hsl(26 60% 64%)` |
| Consistency | Form | `hsl(30 60% 35%)` | `hsl(30 60% 61%)` |
| Formatting | Form | `hsl(34 60% 32%)` | `hsl(34 60% 58%)` |
| Verifiability | Grounding | `hsl(158 55% 32%)` | `hsl(158 55% 62%)` |
| Factuality | Grounding | `hsl(162 55% 29%)` | `hsl(162 55% 58%)` |
| Relevance | Grounding | `hsl(166 55% 26%)` | `hsl(166 55% 54%)` |
| Discipline | Reasoning | `hsl(323 60% 40%)` | `hsl(323 60% 68%)` |
| Soundness | Reasoning | `hsl(326 60% 37%)` | `hsl(326 60% 65%)` |
| Precision | Reasoning | `hsl(329 60% 34%)` | `hsl(329 60% 62%)` |
| Parsimony | Reasoning | `hsl(332 60% 31%)` | `hsl(332 60% 59%)` |
| Calibration | Judgment | `hsl(272 30% 42%)` | `hsl(272 30% 70%)` |
| Fairness | Judgment | `hsl(278 30% 39%)` | `hsl(278 30% 67%)` |
| Robustness | Judgment | `hsl(284 30% 36%)` | `hsl(284 30% 64%)` |

## Score Palette

The score ramp is orthogonal to family.
It is a valence axis (bad to good) plus a muted variant for `0` (not applicable to this
document) and `NA` (not assessed).

| Score | Color (light) | Color (dark) | Weight | Opacity |
| --- | --- | --- | --- | --- |
| `0` | `hsl(220 10% 50%)` | `hsl(220 10% 60%)` | 400 | 0.75 |
| `1` | `hsl(0 70% 35%)` | `hsl(0 70% 60%)` | 800 | — |
| `2` | `hsl(28 80% 30%)` | `hsl(28 70% 60%)` | 650 | — |
| `3` | `hsl(40 80% 32%)` | `hsl(40 70% 60%)` | 700 | — |
| `4` | `hsl(140 60% 28%)` | `hsl(140 50% 55%)` | 750 | — |
| `5` | `hsl(140 60% 20%)` | `hsl(140 50% 45%)` | 850 | — |
| `NA` | `hsl(220 10% 50%)` | `hsl(220 10% 60%)` | 400 | 0.65 |

Font weight tracks score strength; opacity is reserved for the muted `0` and `NA`
states.

## Icons

Each top-level group has one icon, drawn from
[Material Design Icons (MDI)](https://pictogrammers.com/library/mdi/) (Apache 2.0). MDI
was chosen for the timeless, instrument-flavored draftsmanship of these particular
icons: a compass rose, a writing tool, a scroll, a fixed point, a measuring tool, and a
weighing tool — a navigator’s drafting kit.

Store the **name**, not a glyph, so the design system stays independent of font and
Unicode availability.
The local SVGs are inlined verbatim with attribution in a leading XML comment.

| Group | Name | Local file | Sense |
| --- | --- | --- | --- |
| Purpose | `mdi:compass-rose` | [purpose.svg](assets/icons/purpose.svg) | orientation toward the reader’s task |
| Expression | `mdi:quill` | [expression.svg](assets/icons/expression.svg) | language, surface form |
| Form | `mdi:scroll` | [form.svg](assets/icons/form.svg) | the document as a structured artifact |
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
.dim              { display: inline-flex; align-items: center; gap: 0.35em; }
.dim--purpose     { color: var(--accent-p); }
.dim--expression  { color: var(--accent-e); }
.dim--form        { color: var(--accent-f); }
.dim--grounding   { color: var(--accent-g); }
.dim--reasoning   { color: var(--accent-r); }
.dim--judgment    { color: var(--accent-j); }
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
.dim-stamp svg { width: 100%; height: 100%; color: var(--bg); }

/* Background uses the group ink color (light or dark via the theme tokens);
   the SVG color is the page background, so the cut-out flips with the theme. */
.dim-stamp.dim--purpose     { background: var(--accent-p); }
.dim-stamp.dim--expression  { background: var(--accent-e); }
.dim-stamp.dim--form        { background: var(--accent-f); }
.dim-stamp.dim--grounding   { background: var(--accent-g); }
.dim-stamp.dim--reasoning   { background: var(--accent-r); }
.dim-stamp.dim--judgment    { background: var(--accent-j); }
```

Sizing rule: the icon should occupy roughly 55-65% of the stamp’s diameter (set via
`padding` on the container, not by sizing the SVG). At small sizes (< 24px diameter)
prefer the rounded-square variant (`border-radius: 22%`) for legibility.

If a renderer cannot resolve a custom property, hard-code the surface color used by that
medium (`hsl(40 38% 93%)` for the cream-paper demo surface, `hsl(40 8% 8%)` for the dark
counterpart).

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
  background-color: var(--accent-p);
  mask-image: url("assets/icons/purpose.svg");
  mask-size: contain; mask-repeat: no-repeat;
}
```

#### Terminal / plain text

Maintain a small lookup that maps each name to a Unicode glyph, with a two-letter group
abbreviation as final fallback (`Pu`, `Ex`, `Fo`, `Gr`, `Re`, `Ju`).

## Adding or Changing Colors

When proposing palette changes:

1. Keep all values in `hsl()`. No hex, no `rgb()`, no commas inside the parentheses.
2. **Always change the light/dark pair together.** A token without both modes is
   incomplete; reviewers should reject single-mode color changes.
3. **Hold `H` and `S` constant within a group.** Lightness alone moves between
   light/dark and between surface / ink / dim.
   If a group needs a different hue or saturation, change the whole group, not one
   member.
4. Adjust one axis at a time so the rationale is inspectable in the diff.
5. Stay inside the family hue range for dimensions (a few degrees from the group hue);
   if a dimension needs to move outside its family’s neighborhood, the group assignment
   is the problem, not the color.
6. Verify contrast for surface/ink pairs in **both modes** at minimum WCAG AA (4.5:1 for
   body text). Any browser devtools color picker or the `contrast-ratio` CLI is
   sufficient.

## References

- [`tools/pprose/src/pprose/table_styles.py`](../../pprose/src/pprose/table_styles.py) —
  runtime source of truth for the palette; emits `hsl()` and ships both light and
  `_dark` palette variants per the convention above.
- [`tools/pprose/src/pprose/rubric_schema.yaml`](../../pprose/src/pprose/rubric_schema.yaml)
  — defines the group and dimension keys this palette binds to.
- [`tools/docs/project/specs/active/plan-2026-05-23-rendered-eval-reports.md`](../project/specs/active/plan-2026-05-23-rendered-eval-reports.md)
  — in-flight plan that will consume this system in the HTML renderer.
