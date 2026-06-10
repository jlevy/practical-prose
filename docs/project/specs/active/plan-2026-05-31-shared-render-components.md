---
title: Shared render components — single source of truth for visual surfaces
description: Pull CSS + JS + Jinja partials for the eval visualizations into upstream component files that both the explorations playground and the `pprose render` static HTML output ingest unchanged, so visual changes only need to happen in one place
author: Joshua Levy (github.com/jlevy) with LLM assistance
---
# Feature: Shared Render Components

**Date:** 2026-05-31

**Author:** Joshua Levy

**Status:** Implemented in substance (tools/render-components/ + sync into
`_generated/`, variant architecture, workbench-consumes-shared tests).
The Phase 1 checklist below was never ticked; treat the shipped artifacts as
authoritative. Epic pp-ict2 closed 2026-06-10.

## Overview

Replace the current ad-hoc selective-copy approach for keeping `pprose render` aligned
with the explorations playground with a **shared-components** model: the CSS,
JavaScript, and HTML partials that draw the Practical Prose visual surfaces live in one
canonical set of files, and both the explorations playground (the design workbench) and
the `pprose render` static-HTML pipeline ingest those same files unchanged.

The renderer’s job shrinks to: (1) compute a small data payload from an `EvalReport`,
(2) assemble a thin outer HTML page that includes the shared components plus a tiny
bootstrap script that hands the data to them.

The result: any visual or interaction change made in the workbench automatically lands
in `pprose render`’s output the next time the sync script runs.

## Goals

- One canonical set of CSS, JavaScript, and HTML partials drives every Practical Prose
  visual surface (the explorations playground today; future surfaces like a comparison
  page tomorrow). No selector-by-selector porting, no drift.
- A single sync script `tools/pprose/devtools/sync_render_html_styles.py` is the only
  path that writes into `tools/pprose/src/pprose/render_html/styles/` and
  `tools/pprose/src/pprose/render_html/js/`. The outputs carry a clear auto-generated
  header.
- `pprose render <eval.md>` continues to produce a single self-contained HTML file (CSS,
  JS, icons, eval data all inlined).
  The print dialog still works cleanly (light tokens forced, theme toggle hidden).
- The shared components encapsulate one cohesive piece each (card renderer, tip-panel
  pair, theme toggle) with documented entry points and data contracts, so they’re
  reusable from any HTML page (not only the explorations workbench and `pprose render`).
- The renderer supports a small, named set of **variant templates** built from the same
  shared components but with different page layouts.
  Phase 1 ships only the `interactive` variant; the design leaves room for
  `static-cards` (all panels rendered statically below the card, no hover needed for
  print) and `annotated-doc` (card + embedded source document with inline annotations)
  as future additions.
- A drift-check command (`uv run python devtools/sync_render_html_styles.py --check`)
  fails CI when the synced outputs are out of date.

## Non-Goals

- **A general-purpose component framework.** This is specifically about the Practical
  Prose visual surfaces.
  We are not adopting Web Components, Lit, React, or any framework.
  Plain CSS, plain JavaScript IIFEs, plain Jinja partials.
- **Server-side rendering of the card DOM.** The card and tip panels are built by the
  same JavaScript functions in every surface (explorations, static report, future
  comparison page). Python’s only DOM responsibility is the outer HTML shell.
- **Bundling a build pipeline.** No Vite, no esbuild, no rollup.
  The sync script is plain Python; assets are read from disk and inlined into the output
  HTML.
- **Refactoring the explorations workbench beyond what’s needed.** We will extract the
  canonical pieces from where they currently live in the workbench, but we will not
  redesign the workbench’s UI or its non-shared parts (the controls panel, the slider
  grid, the other visualization variants).
- **Lifting CSS/JS for visuals 1–8 and 10.** Out of scope; only the Visual 9B card, the
  tip-panel pair, and the theme toggle are shared by `pprose render` today.
- **Web fonts as a hard requirement.** The shared design-system tokens declare a font
  stack with `@font-face` links to a CDN; the rendered HTML works offline (system fonts
  fall back), and the printed PDF is acceptable with system fonts.
  We do not vendor the woff2 files into the wheel.

## Background

### What’s broken today

`pprose render` mirrors the explorations playground’s visual output by **selectively
extracting** CSS rules (via a sync script that routes selectors to `card.css` /
`detail.css` / `surface_white.css`) and **manually replicating** the JS-built DOM in
Python Jinja templates (`page_card.html.jinja`, `page_detail.html.jinja`).

Every time the workbench’s CSS or DOM shape changes, the manual replication drifts.
Concrete drift incidents seen in the last day:

- Added `bi-stack` centering rule missed entirely.
- New design tokens (`--font-sans-weight-medium`, `--font-serif-weight-bold`,
  `--line-height`, `--font-serif-size`) introduced upstream; the renderer’s CSS file
  used old hand-tuned values.
- Per-dim hue, score color, segment alpha logic in `_biDimPrep` reinterpreted in Python;
  values diverged.
- `.bi-layout .bi-card, .bi-layout .bi-tip-panel { box-sizing: border-box; }` added
  upstream; missed in the route table because the selector spans both card and detail
  targets.
- Group icon SVG sizing rules (`.grp-icon`, `.grp-icon svg`) were not in the router; the
  sync’s first cut shipped without them.
- Theme toggle markup, CSS, and JavaScript not in `pprose render` at all yet.

The user has now flagged this pattern explicitly: selective copying is the problem;
pieces must be copied **whole cloth** with only a few thin outer template tweaks
specific to each surface.

### What “shared components” means concretely

A component, for this project, is a tuple of:

- One or more **CSS files** — the styles the component owns (selectors are expected to
  be uniquely-namespaced so they don’t collide between components).
- Zero or more **JavaScript files** — the public entry points and the DOM they build.
- An optional **Jinja partial** — the static HTML scaffold the JS hydrates, for surfaces
  that prefer static-first markup over fully JS-built DOM.
- A documented **data contract** — the JS public entry point’s parameter shape, written
  in the JS file’s leading comment.

Components live under `tools/render-components/<name>/` (a new top-level sibling of
`tools/design-system/`). Each surface that wants to use a component lists it in a
manifest and the sync tooling concatenates and inlines accordingly.

### Why now

- The drift pattern is biting on every iteration of the static HTML report.
- The user has settled on the Visual 9B card + the two tip panels + the theme toggle as
  the canonical single-doc presentation.
  These are the first set of pieces to share, and there is no incentive to keep two
  copies.
- The design system already lives upstream
  ([tools/design-system/](../../../../tools/design-system/)) and is mirrored to the
  renderer via a generated file.
  Shared components are the natural next layer of that pattern.

## Design

### Architecture overview

```
tools/
  design-system/                       (existing; tokens, palette, schema)
    _generated/design_system.css
    assets/icons.svg

  render-components/                   (NEW; the shared components)
    bi-card/                           — Visual 9B card renderer
      card.css                         (CSS rules with `.bi-*` selectors)
      card.js                          (renderBiCard(), biDim9B(), groupIcon(), helpers)
      README.md                        (data contract + usage example)
    tip-panels/                        — Detail + Assessment hover panels
      tip-panels.css                   (`.bi-tip-panel` styles + content typography)
      tip-panels.js                    (mountTipPanels(), renderDim(), renderGroup())
      README.md
    theme-toggle/                      — Three-button Auto/Light/Dark
      theme-toggle.css                 (`.theme-toggle` styles)
      theme-toggle.js                  (mountThemeToggle())
      theme-toggle.html.jinja          (markup partial)
      README.md
    vendor/                            — Third-party libraries the components need
      marked.min.js                    (the markdown library tip-panels uses)

  explorations/visual-design/
    dimension-visualizations.html      (the workbench; ingests components via
                                        plain <link>/<script> for now, no
                                        bundling)

  pprose/
    devtools/sync_render_html_styles.py
                                       — mirrors render-components/ + design-system/
                                       — into src/pprose/render_html/{styles,js}/
    src/pprose/render_html/
      styles/_generated/design_system.css   (mirrored from design-system)
      styles/_generated/bi-card.css         (mirrored from render-components)
      styles/_generated/tip-panels.css      (mirrored)
      styles/_generated/theme-toggle.css    (mirrored)
      styles/print.css                      (renderer-owned, hand-edited)
      js/_generated/bi-card.js              (mirrored)
      js/_generated/tip-panels.js           (mirrored)
      js/_generated/theme-toggle.js         (mirrored)
      js/_generated/marked.min.js           (mirrored)
      templates/base.html.jinja             (renderer-owned, hand-edited)
      templates/theme-toggle.html.jinja     (mirrored from render-components, via {% include %})
      renderer.py                           (renderer-owned)
      inliner.py                            (renderer-owned)
```

The `_generated/` subdirectories under `pprose/render_html/styles/` and
`pprose/render_html/js/` carry a clear “AUTO-GENERATED; run the sync script” header at
the top of every file.
The sync script is the only path that writes to those folders; hand-editing is a
contract violation and the drift-check command catches it.

### Data flow for `pprose render <eval.md>`

```
.eval.md
  │
  ▼  EvalReport.from_eval_md
EvalReport (Pydantic model — existing schema)
  │
  ▼  renderer.py builds JSON payload matching bi-card's contract:
  │     { groups, dimensions, rubric, doc }
  │
  ▼  Jinja renders base.html.jinja, which:
  │     - inlines styles/_generated/{design_system,bi-card,tip-panels,theme-toggle}.css
  │     - inlines js/_generated/{marked.min,bi-card,tip-panels,theme-toggle}.js
  │     - inlines design-system/assets/icons.svg (via mirrored copy)
  │     - {% include 'theme-toggle.html.jinja' %} for the markup partial
  │     - emits the empty card container and tip-panel asides
  │     - emits a bootstrap <script> that hands the data payload to the JS
  │
  ▼  inliner.py concatenates assets into the final HTML string
  │
  ▼  --format single (default)   →  one self-contained .html file
  │  --format folder             →  HTML + sidecar assets/ for dev
  │
  ▼  written to disk; --open launches the default browser
```

The bootstrap script is a few lines:

```html
<script>
  (function () {
    const data = JSON.parse(document.getElementById("pp-eval-data").textContent);
    PracticalProseBiCard.mount(".bi-stack", data);
    PracticalProseTipPanels.mount(".bi-tip-panel-detail", ".bi-tip-panel-assess", data);
    PracticalProseDesignColorControls.mountThemeToggle(".theme-toggle");
  })();
</script>
```

Each component exposes a single `mount()`-shaped public function.
The JSON payload’s shape is documented in each component’s `README.md` and validated by
a tiny check in each component’s `mount()` so a malformed payload fails loudly.

### Per-surface variation: the only delta lives in the outer page

Surfaces differ in:

- **HTML shell** — the explorations workbench has a full chrome (controls panel, legend,
  notes grid, the other 8 visuals).
  `pprose render`’s shell has only the toggle + card + tip panels.
  The components don’t care; they attach to whatever container selectors the caller
  passes.
- **Print rules** — only `pprose render`’s shell carries `print.css`; the workbench
  doesn’t print.
- **Data source** — the workbench loads fixtures asynchronously from on-disk `.eval.md`
  files; `pprose render` injects pre-computed JSON.
- **Theme / surface defaults** — `pprose render` defaults to `data-surface="white"` and
  `data-theme-mode="auto"` on `<html>`; the workbench has the surface toggle UI that
  lets the designer pick.

These are 5–10 lines of HTML per surface.
Everything else is shared.

### Sync script responsibilities

`tools/pprose/devtools/sync_render_html_styles.py` is the single mirror path.
On every run it:

1. Copies `tools/design-system/_generated/design_system.css` →
   `styles/_generated/design_system.css`.
2. For each component listed in a small manifest
   (`COMPONENTS = ("bi-card", "tip-panels", "theme-toggle")`):
   - Copies `tools/render-components/<name>/<name>.css` →
     `styles/_generated/<name>.css`.
   - Copies `tools/render-components/<name>/<name>.js` → `js/_generated/<name>.js`.
   - Copies `<name>.html.jinja` (if present) → `templates/<name>.html.jinja`.
3. Copies `tools/render-components/vendor/marked.min.js` →
   `js/_generated/marked.min.js`.
4. Copies `tools/design-system/assets/icons.svg` →
   `src/pprose/render_html/assets/icons.svg`.
5. Stamps a provenance header at the top of each output ("AUTO-GENERATED by
   sync_render_html_styles.py from <source>; do not edit").
6. With `--check`: exits non-zero on any drift; CI runs this.

The script is plain Python (`uv run python devtools/sync_render_html_styles.py`). No
build step, no transpilation.

### Bootstrapping the work — what gets pulled where

Some of the canonical files don’t exist yet at the new locations; they live inside the
explorations HTML or the existing `lib/` directory.
Phase 1 also **creates** `tools/render-components/` and **moves** the canonical pieces
in.

Specifically, the following moves happen as part of this work:

- Extract from `tools/explorations/visual-design/dimension-visualizations.html`:
  - The CSS rules for `.bi-*` (card) → `tools/render-components/bi-card/card.css`.
  - The CSS rules for `.bi-tip-panel*` →
    `tools/render-components/tip-panels/tip-panels.css`.
  - The JS functions `biCard`, `biDim9B`, `_biDimPrep`, `groupIcon`, `groupAvgChip`,
    `dimColorMix`, `scoreColor`, `_readScoreAlphaStep`, `segmentAlpha`, `el` →
    `tools/render-components/bi-card/card.js`.
  - The JS functions `setupTipPanel`, `renderDim`, `renderGroup` →
    `tools/render-components/tip-panels/tip-panels.js`.
- Move only the `mountThemeToggle` half of
  `tools/explorations/visual-design/lib/design-color-controls.js` →
  `tools/render-components/theme-toggle/theme-toggle.js`. `mountSurfaceToggle` stays in
  the workbench’s local `lib/`.
- Lift the `.theme-toggle` + `.surface-toggle` CSS from the explorations HTML’s
  `<style>` block → `tools/render-components/theme-toggle/theme-toggle.css`.
- The explorations HTML is then edited to `<link rel="stylesheet">` and `<script src>`
  from the new shared locations (relative paths) so the workbench keeps working
  unchanged from the user’s perspective.

This is structural-only refactoring inside the explorations file (pure extract + import)
— no visual or behavioral change there.

### Components

**`bi-card`** — The Visual 9B bidirectional-bars card.

- `mount(containerSelector, data)` — clears the container and renders one `.bi-card` per
  `data.doc` (today: one doc; future: an array for compare).
- Data contract:
  `{ groups, dimensions, rubric, doc: { id, name, scores, reasons, findings, meta? } }`.
  Documented in `tools/render-components/bi-card/README.md`.

**`tip-panels`** — The Detail + Assessment side panels with hover-driven content.

- `mount(detailSelector, assessSelector, data)` — wires hover handlers onto every
  `[data-tip-kind]` element on the page (which the bi-card emits).
- Data contract includes `rubric` (questions + rules per dim) and `doc` (per-doc scores
  \+ reasons + findings).

**`theme-toggle`** — Three-button Auto / Light / Dark toggle.

- `mountThemeToggle(containerSelector, opts?)` — verbatim from the existing
  `design-color-controls.js`.
- HTML partial provided so callers can `{% include 'theme-toggle.html.jinja' %}` instead
  of hand-writing the buttons.

### Variant templates

The renderer is designed for a small, named set of **variant templates** that share the
same shared components but assemble them into different page layouts.
Phase 1 ships exactly one variant — `interactive` — and the design holds room for more.

Anticipated variants (named, not all implemented today):

| Variant | What it shows | Status |
| --- | --- | --- |
| `interactive` | One `.bi-card` centered; two hover-driven `.bi-tip-panel` asides update on hover (Detail + Assessment); theme toggle in the corner. Mirrors the explorations workbench’s 9B section. | **Phase 1** |
| `static-cards` | The card at the top, then a static “cards-below” stack rendering each dim’s Detail + Assessment side-by-side as printed blocks. Each block reuses the same `tip-panels` markup; the JS just renders them all at once instead of swapping on hover. Good for printing the entire eval to PDF without needing to hover anything. | Future |
| `annotated-doc` | The card at the top, then the full source document body with inline annotations (highlights, marginalia) linking quotes to dim findings. Requires the future “advanced” eval profile that embeds the source body in the report. | Future |

Each variant is one Jinja template file under
`tools/pprose/src/pprose/render_html/templates/variants/<name>.html.jinja` that
**extends** `base.html.jinja` (Jinja inheritance: `{% extends 'base.html.jinja' %}`).
The base provides the head + theme toggle + body shell; each variant overrides one or
two `{% block %}` sections to lay out the card and the panels its own way.

The CLI grows one flag — `--variant <name>` — defaulting to `interactive`. The renderer
looks up `variants/<name>.html.jinja`, errors with a clear “unknown variant; available:
…” message if it’s not present, and renders through that file.
The bootstrap script and the data payload are identical across variants; only the DOM
scaffolding the variant emits (and the JS calls in its bootstrap section) differ.

Adding a new variant later is a self-contained piece of work: add the template file,
document it here, no changes to the shared components or the sync script.

### Print + theme behavior

`styles/print.css` (renderer-owned, not auto-generated) carries:

- `@media print { .theme-toggle { display: none !important; } }`.
- `@media print { :root, :root[data-theme="dark"] { /* force light tokens */ } }` —
  overrides every surface and dim token to its light-mode value, so a user whose OS is
  in dark mode still prints a clean light-mode PDF. Light token values mirror the design
  system’s `:root` defaults.
- Existing `@page { size: letter; margin: 0.6in }` rules and `break-inside: avoid` on
  cards / panels.

`pprose render --page-size a4` rewrites `size: letter` to `size: A4` at inline-time,
same as today.

### CLI surface

`pprose render <eval.md> [options]` — primitive surface as defined in
[plan-2026-05-29-static-html-eval-report.md](../done/plan-2026-05-29-static-html-eval-report.md).
`pprose score --render-html` — composition flag, unchanged.

This spec adds one CLI flag and otherwise leaves the surface intact:

```
--variant <name>          Page-layout variant to render. Default: interactive.
                          Phase 1 ships only `interactive`. Future variants
                          (e.g. `static-cards`, `annotated-doc`) plug in as
                          new templates under variants/.
```

The earlier `--sections` flag becomes redundant (variants own their own section
composition) and is removed; `--page-size`, `--format`, `-o`, and `--open` stay.

The internal mirroring strategy changes substantially; the user-facing shape only grows
by one flag.

## Implementation Plan

### Phase 1: Extract, share, and wire

This phase touches three trees in lockstep so the cutover lands atomically: the
explorations workbench, the new shared-components tree, and the renderer.

- [ ] Create `tools/render-components/` with the subdirectory layout above (`bi-card/`,
  `tip-panels/`, `theme-toggle/`, `vendor/`).
- [ ] Extract from
  [tools/explorations/visual-design/dimension-visualizations.html](../../../../tools/explorations/visual-design/dimension-visualizations.html):
  the CSS rules for `.bi-*` (excluding `.bi-tip-panel`) and `.grp-icon` →
  `tools/render-components/bi-card/card.css`.
- [ ] Extract the `.bi-tip-panel*` CSS rules and `@keyframes bi-tip-fade-in` →
  `tools/render-components/tip-panels/tip-panels.css`.
- [ ] Extract `.theme-toggle` and `.surface-toggle` CSS rules →
  `tools/render-components/theme-toggle/theme-toggle.css`.
- [ ] Extract the JS functions listed in **Bootstrapping** above into `bi-card/card.js`
  and `tip-panels/tip-panels.js`. Wrap each in an IIFE that exposes one global
  (`window.PracticalProseBiCard` / `window.PracticalProseTipPanels`) with a `mount()`
  entry point matching the documented data contract.
  Helpers stay private.
- [ ] Move only `mountThemeToggle` from
  [tools/explorations/visual-design/lib/design-color-controls.js](../../../../tools/explorations/visual-design/lib/design-color-controls.js)
  → `tools/render-components/theme-toggle/theme-toggle.js`. `mountSurfaceToggle` stays
  in the workbench’s local file.
- [ ] Write the `theme-toggle/theme-toggle.html.jinja` partial with the three buttons.
- [ ] Vendor `marked.min.js` (download once, commit) →
  `tools/render-components/vendor/marked.min.js`.
- [ ] Edit
  [tools/explorations/visual-design/dimension-visualizations.html](../../../../tools/explorations/visual-design/dimension-visualizations.html)
  to `<link rel="stylesheet">` and `<script src>` from the new shared locations
  (relative paths). Verify the workbench renders identically before and after.
- [ ] Add per-component `README.md` files (data contract + `mount()` signature
  + usage example) under each `tools/render-components/<name>/`.
- [ ] Rewrite `tools/pprose/devtools/sync_render_html_styles.py` to operate on the
  manifest model described under **Sync script responsibilities**. Stamp provenance
  headers; support `--check` for drift.
- [ ] Update
  [tools/pprose/src/pprose/render_html/inliner.py](../../../../tools/pprose/src/pprose/render_html/inliner.py)
  to load from `styles/_generated/*.css` and `js/_generated/*.js` instead of the
  per-section hand-edited files.
- [ ] Rewrite
  [tools/pprose/src/pprose/render_html/renderer.py](../../../../tools/pprose/src/pprose/render_html/renderer.py)
  to build the JSON payload (matching each component’s data contract) and drop the
  per-dim/metrics/footer Python-built DOM. The card and tip panels become JS-built; the
  renderer’s job is data + shell.
- [ ] Rewrite
  [base.html.jinja](../../../../tools/pprose/src/pprose/render_html/templates/base.html.jinja)
  to be the thin outer shell: `<head>` with inlined CSS + JS, `<body>` with the icon
  sprite, the theme-toggle partial, and Jinja `{% block %}` placeholders the variant
  fills in (`{% block layout %}`, `{% block bootstrap %}`). The base is
  variant-agnostic; it knows nothing about cards or panels — it just establishes the
  page chrome.
- [ ] Add the `interactive` variant under
  `tools/pprose/src/pprose/render_html/templates/variants/interactive.html.jinja`.
  Extends `base.html.jinja`. Its `layout` block emits the empty `.bi-stack` container +
  the two tip-panel asides; its `bootstrap` block calls `PracticalProseBiCard.mount`,
  `PracticalProseTipPanels.mount`, and
  `PracticalProseDesignColorControls.mountThemeToggle`.
- [ ] Wire `--variant <name>` (default `interactive`) into `pprose render`. Unknown
  variants raise with a clear “available: …” message.
  Drop `--sections` (subsumed by variants).
- [ ] Delete the now-unused per-section Jinja templates (`page_card.html.jinja`,
  `page_detail.html.jinja`, `page_metrics.html.jinja`, `page_footer.html.jinja`) and the
  hand-edited per-section CSS (`card.css`, `detail.css`, `surface_white.css`,
  `static_adaptations.css`, `base.css`, `metrics.css`). The `print.css` stays.
- [ ] Update [tools/pprose/pyproject.toml](../../../../tools/pprose/pyproject.toml)
  `[tool.hatch.build.targets.wheel] include = [...]` to ship the new
  `styles/_generated/*`, `js/_generated/*`, and `templates/*.jinja` paths.
- [ ] Update / rewrite
  [tests/test_render_html.py](../../../../tools/pprose/tests/test_render_html.py) to
  assert the new structure: the JSON payload embeds the right keys, the
  `<script src>`-equivalent inlines are present, the card container is empty (rendered
  at view time), the theme-toggle markup is present.
  The detection + fixture-rendering tests stay.
- [ ] Add a drift-check test: `tests/test_render_html_sync.py` runs the sync script in
  `--check` mode and fails on drift.
- [ ] Verify in browser: `uv run pprose render tests/fixtures/rev2-net.eval.md --open`,
  confirm card renders, hover panels work, theme toggle works, `Cmd-P` shows light-mode
  preview with toggle hidden.
  Manual sign-off.

## Testing Strategy

- **Golden HTML test (existing pattern)**: render a fixture `.eval.md` to HTML; diff the
  **structural shell** (everything outside the inlined data payload) against a
  checked-in golden. The inlined JSON payload is asserted separately field-by-field so a
  token-level reformatting doesn’t break the structural diff.
- **Data-payload test**: construct an in-memory `EvalReport` with every legal `Score`
  value (`1..5`, `NA`, `ERR`) and assert the JSON payload’s shape matches each
  component’s contract.
- **Drift-check test**: `tests/test_render_html_sync.py` runs the sync script with
  `--check`; CI fails on any unsynced output.
- **Schema-coverage test (existing)**: passes once the payload-builder handles every
  Score variant.
- **Manual browser sign-off**: same checklist as before — card renders, hover panels
  populate, theme toggle works, `Cmd-P` shows clean light preview with toggle hidden,
  both Letter and A4 paginate sensibly.
- **No headless-browser PDF test**: explicitly out of scope, same as earlier spec.

## Rollout Plan

- Phase 1 lands as a single PR. The PR’s `git diff` will be large because multiple files
  move; reviewing is easier by viewing the PR with whitespace ignored and reading
  per-component, not per-file.
- After merge: regenerate
  [tools/design-system/_generated/design_system.css](../../../../tools/design-system/_generated/design_system.css)
  if anything in `design-system.yaml` changed; re-run the sync script; re-render the
  bundled fixture goldens.
- The earlier static-HTML-eval-report spec
  ([plan-2026-05-29-static-html-eval-report.md](../done/plan-2026-05-29-static-html-eval-report.md))
  remains the source of truth for the CLI surface and the user-facing workflow.
  This spec amends only the internal architecture.

## Resolved design choices

- **Component tree location**: `tools/render-components/` as a top-level peer of
  `tools/design-system/`. The design system owns tokens + schemas
  + generator; render-components own the visual surfaces that consume those tokens.
    Two distinct concerns, sibling directories.
- **`marked.min.js` vendoring**: committed under
  `tools/render-components/vendor/marked.min.js`. No npm step, no node toolchain in CI.
  The sync script reads from there and inlines.
- **Theme-toggle scope**: only `mountThemeToggle` (Auto / Light / Dark).
  `mountSurfaceToggle` stays in the explorations workbench’s local
  `lib/design-color-controls.js` (or moves with it as a separate workbench-only file),
  not in the shared component.
  Cleaner shared component, and `pprose render` ships less inert JS.
- **Component public API surface**: a single `mount()` entry point per component.
  `PracticalProseBiCard.mount(containerSelector, data)`,
  `PracticalProseTipPanels.mount(detailSelector, assessSelector, data)`,
  `PracticalProseDesignColorControls.mountThemeToggle(containerSelector, opts?)`.
  Helpers stay private inside each component’s IIFE.

## Open Questions

- **Should each render-component carry its own version stamp** (so the workbench and the
  renderer can detect mismatched copies)?
  Likely not in Phase 1; the sync-on-CI check covers the same ground.
  Revisit if a third surface joins.

## References

- [plan-2026-05-29-static-html-eval-report.md](../done/plan-2026-05-29-static-html-eval-report.md)
  — the CLI surface and user-facing workflow this spec implements
- [tools/design-system/design-system.md](../../../../tools/design-system/design-system.md)
  — the token system the components consume
- [tools/explorations/visual-design/dimension-visualizations.html](../../../../tools/explorations/visual-design/dimension-visualizations.html)
  — the canonical source for the Visual 9B card, tip-panel CSS, and JS functions that
  get extracted into the shared components
- [tools/explorations/visual-design/lib/design-color-controls.js](../../../../tools/explorations/visual-design/lib/design-color-controls.js)
  — the existing theme-toggle / surface-toggle implementation, moves into
  `render-components/theme-toggle/`

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
