---
title: Static HTML eval report (Visual 9B)
description: Extract the Visual 9B mockup into a clean, shareable, print-friendly static HTML rendering pipeline shipped with the pprose CLI
author: Joshua Levy (github.com/jlevy) with LLM assistance
---
# Feature: Static HTML Eval Report (Visual 9B)

**Date:** 2026-05-29

**Author:** Joshua Levy

**Status:** Implemented (shipped in v0.1.0; `pprose render` with the variant
architecture). Outcome notes: the planned `--sections` flag became `--variant`, and the
per-section templates became `variants/*.html.jinja`. Manual print verification is
tracked as pp-kmv5.

## Overview

Ship a first-class static-HTML rendering of a Practical Prose evaluation, extracted from
the **Visual 9B** mockup in
[tools/explorations/visual-design/dimension-visualizations.html](../../../../tools/explorations/visual-design/dimension-visualizations.html).
The pipeline takes a single `.eval.md` file (or an in-memory `EvalReport`) and emits a
clean, self-contained HTML page that renders well on screen and prints cleanly to PDF
via the browser’s “Save as PDF” / print dialog.

The output is the canonical *shareable artifact* for a single-doc eval — sitting
alongside the existing Markdown rollup
([eval_render.py](../../../../tools/pprose/src/pprose/eval_render.py)) and the canonical
YAML frontmatter ([eval_report.py](../../../../tools/pprose/src/pprose/eval_report.py)).

## Goals

- One command turns an `.eval.md` into a shareable HTML file that looks good both on
  screen and on paper.
- Two workflows are both first-class and supported by composing the same primitive:
  1. **End-to-end**: `pprose score <doc.md> --render-html` runs scoring → writes the
     structured `.eval.md` (YAML frontmatter) and the Markdown rollup body → also emits
     the HTML page. One invocation, all three artifacts.
  2. **Render-only**: `pprose render <doc.eval.md>` re-emits the HTML from an existing
     `.eval.md`. No model call, no rescoring; pure presentation.
     Use when iterating on the visual, sharing a previously scored doc, or rendering an
     eval produced by a separate run of `pprose score`. The combined workflow is exactly
     the standalone scoring step followed by the standalone render step — no new logic,
     just composition.
- The page renders to PDF cleanly via the browser’s print dialog (Letter and A4 both
  paginate reasonably).
- Visual 9B is the source of truth for the layout and tokens; no design re-derivation.
- The renderer ships *inside* the `pprose` wheel — no extra install step, no `uvx`
  download at render time, no external CDN dependency at view time.
- The template, CSS, and asset layout are organized so adding a new section (e.g., a
  per-dim findings page, a comparison page, a different card variant) is a focused edit
  to one template, not a rewrite.
- The renderer is **input-aware by design**. `pprose render <path>` dispatches on the
  detected input kind (eval report today; plain Markdown document and other artifact
  types later) so the same command and visual scaffolding can grow to new inputs without
  a parallel CLI surface.
- The renderer is **eval-profile-aware by design**. The pipeline accommodates more than
  one type of eval today and in the future — a stripped-down “basic” eval, the current
  standard rubric, and a future “advanced” eval that may carry per-passage annotations.
  The renderer chooses a layout appropriate to the profile rather than assuming a single
  fixed shape.
- Tests cover golden HTML for a fixture eval, so regressions are caught.

## Non-Goals

- **Multi-document HTML comparison.** `pprose compare` already emits Markdown; the HTML
  compare variant can mirror this template later, but is not in scope.
- **Server-side PDF generation.** No headless Chromium, weasyprint, or wkhtmltopdf
  dependency. PDF is produced via the user’s browser print dialog.
- **Interactive features.** No JavaScript hover panel like the explorations file.
  The static page renders all content for static reading; per-dim detail (rubric
  question, rules, score reasoning, rule findings) is laid out on the page itself, not
  gated behind hover.
- **Dark-mode print.** The print stylesheet is always light; on-screen may support
  light/dark via `prefers-color-scheme` if free, but is not required for MVP.
- **A new design system.** The renderer reads from
  [tools/design-system/design-system.yaml](../../../../tools/design-system/design-system.yaml)
  and existing palette tokens; no new palette is introduced.
- **Custom font hosting / embedding.** Use system font stacks (serif + sans + mono); no
  `@font-face` web font downloads.
  Print fidelity is “looks consistent on common OSes”, not “pixel-perfect across
  machines”.
- **Rendering of inputs other than `.eval.md`.** Phase 1 only renders eval reports.
  The CLI is *designed* to dispatch on input kind so plain Markdown documents and future
  eval profiles can be added cleanly (see “Input detection and dispatch” below), but
  Phase 1 does not implement any non-eval renderer.
- **Embedded source-document annotation rendering.** The forward-looking “advanced” eval
  profile may embed the source document inside the `EvalReport` so the renderer can
  overlay per-passage annotations.
  Phase 1 does not implement this; it only ensures the architecture has room for it (the
  eval renderer is one entry in the dispatch table, and emits sections based on which
  data blocks the report carries).

## Background

### What exists today

- **Visual 9B mockup** lives inside the explorations file
  [tools/explorations/visual-design/dimension-visualizations.html](../../../../tools/explorations/visual-design/dimension-visualizations.html)
  (4867 lines), bundled with nine other variants, runtime YAML fetching, hover-driven
  tip panels, and a slider-based design-token playground.
  It is not a publishable surface.
- **Eval data model**:
  [eval_report.py](../../../../tools/pprose/src/pprose/eval_report.py) defines
  `EvalReport` (Pydantic), the schema for `.eval.md` frontmatter.
  The `qual`, `qual_reasons`, `rule_findings`, `quant`, `derived`, and `artifact` blocks
  are the data this page renders.
- **Markdown rollup**:
  [eval_render.py](../../../../tools/pprose/src/pprose/eval_render.py) produces a
  per-doc Markdown body from an `EvalReport`. The HTML renderer is a peer of this
  module, not a replacement.
- **Design system**: [tools/design-system/](../../../../tools/design-system/) holds the
  YAML source of truth, generator script, and the existing
  [_generated/design_system.css](../../../../tools/design-system/_generated/design_system.css)
  containing palette tokens and the `--accent-p` / `--surface-p` / etc.
  variables that Visual 9B consumes.
- **CLI surface**: [cli.py](../../../../tools/pprose/src/pprose/cli.py) dispatches
  subcommands via a `COMMANDS` dict mapping `name → CommandSpec(summary, main, group)`.

### Patterns to borrow from `kash` / `textpress`

The user’s existing repos [/Users/levy/wrk/kmd/kash](file:///Users/levy/wrk/kmd/kash)
and [/Users/levy/wrk/kmd/textpress](file:///Users/levy/wrk/kmd/textpress) already solve
“Python CLI emits a static HTML page from a template”:

- **Jinja2 with template inheritance** as the templating layer; CSS pulled in via
  `{% include %}` inside a `<style>` block, which is the simplest way to ship a single
  self-contained HTML file.
  See `/Users/levy/wrk/kmd/kash/src/kash/web_gen/template_render.py`.
- **Print CSS via `@media print` + `@page`** in
  `/Users/levy/wrk/kmd/textpress/src/textpress/docs/templates/textpress_webpage.html.jinja`.
- **`frontmatter_format` library** (already a kash/textpress dep) is the user’s
  established choice for Markdown + YAML frontmatter parsing.
  We may or may not adopt it here; `pprose` currently uses a tiny inline parser plus
  `pydantic` validation.

### Why now

- `pprose eval` (score → report → metrics → rollup) is in place and producing `.eval.md`
  artifacts.
- Visual 9B was approved as the canonical single-doc visual ("9b looks good").
- The next external touchpoint for the project is *sharing an eval result with someone
  else*. A clean HTML/PDF artifact is the natural shareable.

## Design

### Approach

The renderer is a **standalone primitive**: a new `pprose render` subcommand that takes
an `.eval.md` path and writes an HTML file to disk.
This is the only place the HTML-rendering logic lives.

The end-to-end flow is implemented by **composing** the existing `pprose score`
subcommand (which produces the structured `.eval.md` plus its Markdown rollup body) with
the new renderer. The wiring is a thin `--render-html` flag on `pprose score`: after
`score` finishes writing the `.eval.md`, it calls the renderer’s public API
(`render_html.renderer.render_eval_report`) on the just-written report and writes the
HTML alongside it. Same primitive, no logic duplication.

Equivalently a user can run the two steps as separate commands:

```
pprose score doc.md                    # → doc.eval.md
pprose render doc.eval.md              # → doc.eval.html
```

…which is exactly what `pprose score doc.md --render-html` does in one shot.

By default, the HTML is **single-file and self-contained**: CSS, SVG icons, and any
small static assets are inlined into the document.
The renderer also supports emitting a folder with sidecar files for development, gated
by a flag.

Rendering is Jinja2-driven.
Templates and CSS live in `tools/pprose/src/pprose/render_html/` and are bundled into
the wheel via `importlib.resources` so the command works anywhere `pprose` is installed.

Print-friendliness is baked into the stylesheet, not a separate pipeline: `@media print`
\+ `@page` rules with `size: letter` (configurable to `a4`) and explicit
`break-inside: avoid` boundaries around the card, the per-dim detail blocks, and any
multi-dim sections. The expectation is that a user opens the HTML in any modern browser,
hits ⌘P, picks “Save as PDF”, and gets a clean N-page document.

### Output layout

The page is structured as a sequence of clearly bounded sections, each designed to fit
cleanly on one printed page (or break at a sensible boundary):

1. **Page 1 — Visual 9B card.** The bidirectional-bars rubric rollup, sized to fit on a
   single Letter/A4 page.
   Includes the doc kicker, doc title, six group headers with averages, twenty per-dim
   rows, overall mean, and an evaluator/date footer line.
2. **Page 2+ — Per-dimension detail.** One block per dimension with: dim id + label,
   group, score, rubric question, score reasoning (from `qual_reasons`), and rule
   findings (from `rule_findings`). Flows across pages with `break-inside: avoid` on
   each block.
3. **Page N — Quantitative metrics.** A compact rendering of `quant` / `derived` (word
   count, page count, heading distribution, density ratios).
   Approximately the Visual 10 layout, simplified for static print.
4. **Final page — Provenance footer.** Eval method, model, rubric version, eval date,
   source-doc reference (path + hash), pprose version.

Pages 1 and 4 are required; pages 2 and 3 are gated by `--sections` so a user who just
wants the one-page rollup can have that.

### Components

```
tools/pprose/src/pprose/render_html/
  __init__.py
  cli.py                    # `pprose render` subcommand entry point
  renderer.py               # input-kind dispatch + public API
                            #   detect_kind(path)         -> "eval_report" | ...
                            #   render(path|obj, opts)    -> HTML string
                            #   render_eval_report(...)   -> Phase 1 sole entry
  inliner.py                # CSS / SVG inlining for single-file output
  templates/
    base.html.jinja         # <html> shell, <head>, inlined <style>, print rules
    page_card.html.jinja    # Visual 9B card
    page_detail.html.jinja  # per-dim details
    page_metrics.html.jinja # quant metrics
    page_footer.html.jinja  # provenance
  styles/
    base.css                # page chrome, typography, print rules
    card.css                # Visual 9B card (extracted from explorations file)
    detail.css              # per-dim detail blocks
    metrics.css             # quant metrics
    tokens.css              # palette + scale tokens (from design system)
  assets/
    icons.svg               # group icon symbol set (extracted from design system)
```

The `styles/` and `assets/` folders are loaded at render time by `inliner.py` and
inlined into the final HTML.

### CLI surface

**Standalone render** — the primitive:

```
pprose render <eval-md-path> [options]

Options:
  -o, --output PATH         Output HTML path. Default: <eval-md-stem>.html.
  --format single|folder    Single-file (inlined) or folder with sidecar assets.
                            Default: single.
  --page-size letter|a4     Print page size. Default: letter.
  --sections SECTION,...    Comma-list of sections to include from:
                            card,detail,metrics,footer. Default: all.
  --open                    Open the rendered HTML in the default browser
                            (for quick preview while iterating).
```

**End-to-end** — score plus render in one shot:

```
pprose score <doc-md-path> [scoring options] --render-html [render options]

The render options above (--page-size, --sections, --format, --open) are also
accepted here and forwarded verbatim to the renderer. --output defaults to
<doc-md-stem>.eval.html, sitting next to the <doc-md-stem>.eval.md that score
writes.
```

`--render-html` is the only new flag on `pprose score`; without it, `score` behaves
exactly as it does today.
The flag flips on a post-score call into the renderer’s public API.

### Data flow

1. Parse `.eval.md` → `EvalReport` (reuses existing `pprose.eval_report` parsing).
2. Build a Jinja2 context from the `EvalReport` + design-system tokens.
3. Render `base.html.jinja`, which `{% include %}`s the per-section templates and the
   inlined CSS.
4. Write the final HTML to disk (single file) or to a folder (HTML + assets/).

### Input detection and dispatch

`pprose render <path>` does not assume its input is an `.eval.md`. It dispatches on the
detected input kind:

1. **Detect.** Inspect file extension and (for `.md`) the YAML frontmatter shape.
   - `.eval.md` (or `.md` whose frontmatter validates as an `EvalReport`) → eval
     renderer.
   - Anything else → out of scope for Phase 1; the renderer raises a clear error naming
     the detected kind and listing the kinds it supports.
2. **Route.** A small dispatch table in `renderer.py` maps input kind → render function.
   Phase 1 ships exactly one entry (`eval_report`). Future entries (plain Markdown
   document, “advanced” eval variants, comparison bundles) are added as new functions
   and a new table entry — no CLI changes needed.
3. **Render.** The selected render function produces the HTML string; the inliner and
   writer steps are shared across all kinds.

This keeps the renderer’s *surface* stable (one command, one set of flags) while the
*behavior* grows as more input kinds and eval profiles are added.

### Eval profiles

The eval data model already supports multiple profiles in principle (the rubric schema
is versioned and the `EvalReport` carries the rubric version it was scored against).
Anticipated profiles:

- **Standard.** The current full rubric: 20 dimensions across 6 groups, rule findings,
  quant metrics. This is what Phase 1 renders.
- **Basic.** A stripped-down variant (subset of dimensions or a simpler scoring pass).
  Rendered with the same Visual 9B card scaffolding but with empty/hidden group columns
  where dimensions are missing.
- **Advanced.** A future variant that may carry per-passage annotations on an embedded
  copy of the source document — the eval report optionally embeds the document body so
  the renderer can show annotations inline.
  Rendered with an additional section (annotated document) layered on top of the
  standard rollup.

The renderer selects which sections to emit based on what data the `EvalReport` actually
contains, not on a profile-name switch.
A missing block (e.g., no quant metrics) skips its section silently rather than
rendering a blank page.

### Visual 9B extraction

The card markup and CSS are lifted from the explorations file (sections currently
labeled “Visual 9A + 9B: Bidirectional Bars” and `.bi-ltr`). The extraction is careful
but mechanical:

- All CSS scoped under `.bi-`, `.bi-ltr`, `.doc-kicker`, `.doc-name` is moved to
  `styles/card.css`.
- The JavaScript-built DOM (in `biCard()` / `biDim9B()` in the explorations file)
  becomes Jinja markup in `templates/page_card.html.jinja`. No JS at view time.
- The hover-driven tip panels are *removed*; their content moves into the per-dim detail
  page (page 2).
- Per-dim hues from the design-system YAML are emitted as inline CSS custom properties
  on each row (`style="--dim-hue: 72"` style) — same pattern the explorations file
  already uses.

### Resolved design choices

- **CLI shape**: new top-level `pprose render` subcommand (peer of `pprose report`,
  `pprose compare`).
- **Default output mode**: single self-contained HTML file.
  `--format folder` is available for development inspection.
- **MVP scope**: all four sections ship from day one — Visual 9B card, per-dim detail,
  quant metrics, provenance footer.
- **Templating library**: Jinja2. Adds one dependency to `pprose`; matches the
  established kash/textpress pattern and makes future enhancements (new sections,
  alternate cards, compare variant) cheap.
- **Default page size**: Letter.
  `--page-size a4` is supported for international sharing.

## Implementation Plan

### Phase 1: End-to-end single-file render

- [ ] Add `pprose render` subcommand to
  [cli.py](../../../../tools/pprose/src/pprose/cli.py) `COMMANDS` table.
- [ ] Implement the input-kind detection + dispatch table in `renderer.py`. Phase 1
  registers one kind (`eval_report`); unknown kinds raise a clear error naming the
  detected kind and the kinds the renderer supports.
- [ ] Add `--render-html` (plus the forwarded render flags) to `pprose score`’s argparse
  setup; on success, call `render_html.renderer.render_eval_report` on the freshly
  written report. No new logic — pure composition of the two primitives.
- [ ] Create `tools/pprose/src/pprose/render_html/` package with the file layout above;
  wire `importlib.resources` so bundled templates load from the installed wheel.
- [ ] Extract the Visual 9B card markup + CSS from the explorations file into
  `templates/page_card.html.jinja` + `styles/card.css`. Resolve the JS-built DOM to
  static Jinja markup driven by an `EvalReport`.
- [ ] Pull palette + scale tokens from
  [tools/design-system/_generated/design_system.css](../../../../tools/design-system/_generated/design_system.css)
  into `styles/tokens.css` (or `{% include %}` the generated file directly).
- [ ] Implement `renderer.py::render_eval_report(report: EvalReport, opts) -> str`.
- [ ] Implement `inliner.py` for single-file mode (CSS + SVG icon embedding).
- [ ] Add `--page-size letter|a4` and matching `@page` CSS rules with
  `break-inside: avoid` on the card.
- [ ] Add per-dim detail page (page 2), quant metrics page (page 3), and provenance
  footer page (page 4). Each gated by `--sections` so a one-page card is achievable.
- [ ] Add a fixture-driven golden test: `tests/test_render_html.py` renders
  `tests/fixtures/<some-eval>.eval.md` and diffs against a checked-in `<some-eval>.html`
  golden.
- [ ] Verify in browser: open rendered HTML, confirm print preview paginates cleanly on
  both Letter and A4, and that “Save as PDF” yields a sensible PDF. This is manual UI
  verification, not an automated test.

## Testing Strategy

- **Golden HTML tests.** Render fixtures from `tools/pprose/tests/fixtures/*.eval.md` to
  HTML, diff against a checked-in golden file.
  Follows the project’s existing golden-test pattern.
- **Schema-coverage test.** Confirm an in-memory `EvalReport` with every legal
  combination of `Score` (1-5, “NA”, “ERR”) renders without crashing and produces the
  expected per-row CSS classes.
- **Manual print verification.** Run `pprose render --open <fixture>.eval.md`, inspect
  on screen, then use the browser print dialog at Letter and A4. Sign-off is visual.
- **No headless-browser PDF test.** We deliberately do not add Playwright / Puppeteer
  just for this; the user’s print dialog is the source of truth.

## Rollout Plan

- Phase 1 lands as a single PR.
- Once merged, `pprose render <eval.md>` becomes the canonical “share my eval” workflow,
  documented in [AGENTS.md](../../../../AGENTS.md) under Tooling.
- The Visual 9B exploration file is *not* removed — it stays as the design playground.
  The HTML template is the production surface.

## Open Questions

- Should we adopt `frontmatter_format` here as well (matching kash/textpress) or keep
  the existing `pprose`-internal frontmatter parser?
  Decision can be deferred to implementation; the renderer takes an `EvalReport`, so the
  parsing layer is a local concern.
- For the per-dim detail page, do we want to include rule-level descriptions from
  [rubric_schema.yaml](../../../../tools/pprose/src/pprose/rubric_schema.yaml) inline
  (rich) or just rule ids + verdicts (compact)?
  Lean rich for the first cut; revisit if the page count climbs.
- Long-term: should `pprose compare` also emit an HTML variant using this same template
  scaffolding? Likely yes, but explicitly deferred from this spec.
- What’s the right kind-detection signal beyond Phase 1? File extension plus frontmatter
  shape is enough for `.eval.md` vs.
  plain `.md`, but the “advanced” eval with embedded source document may want a distinct
  extension or a frontmatter `kind:` field to make detection unambiguous.
  Decide when the second kind is added.
- When the advanced profile lands, where does the embedded document live in the
  `EvalReport` schema — a separate `source.body` block, an attached file path, or inline
  annotations on the rendered Markdown rollup?
  Schema decision, not a render decision, but the renderer’s section list will need a
  corresponding entry.

## References

- [Visual 9B mockup (explorations)](../../../../tools/explorations/visual-design/dimension-visualizations.html)
- [Practical Prose Design System](../../../../tools/design-system/design-system.md)
- [eval_report.py — EvalReport schema](../../../../tools/pprose/src/pprose/eval_report.py)
- [eval_render.py — Markdown rollup renderer](../../../../tools/pprose/src/pprose/eval_render.py)
- [pprose CLI dispatch](../../../../tools/pprose/src/pprose/cli.py)
- kash template-render harness:
  `/Users/levy/wrk/kmd/kash/src/kash/web_gen/template_render.py`
- textpress print CSS:
  `/Users/levy/wrk/kmd/textpress/src/textpress/docs/templates/textpress_webpage.html.jinja`

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
