---
title: bi-card render component
description: The Visual 9B bidirectional-bars eval card
---
# bi-card

Renders the Practical Prose Visual 9B card: one bidirectional-bars chart per document,
with 10 dimensions on each side (Purpose/Expression/Form left;
Reasoning/Grounding/Judgment right), per-dim hue, unit-tick segments, score chips, and
group icons.

## Public API

```javascript
const api = PracticalProseBiCard.mount(containerSelector, data);
```

`mount` clears `containerSelector` and appends a `.bi-stack.bi-ltr` containing one
`.bi-card` per `data.doc` (today: a single doc; future comparison variants will accept
`data.docs[]`).

The return value `api` exposes the per-row builder so other components (the tip-panels)
can mirror the same widget client-side:

```javascript
{ biDim9B, _biDimPrep, el, groups, dims }
```

## Data contract

```javascript
{
  groups: [{ id: "P", label: "Purpose" }, ...],
  dimensions: [{ id: "P1", label: "Suitability", g: "P" }, ...],
  rubric: { "P1": { question: "...", rules: [...], group: "Purpose" }, ... },
  doc: {
    id: "rev2-net",
    name: "rev2-net",
    scores:   { P1: 4, P2: 3, ..., E1: "NA", J3: "ERR" },
    reasons:  { P1: "...", ... },        // optional, used by tip-panels
    findings: { P1: [{ rule_number, verdict, description }, ...], ... }
  }
}
```

## DOM markup contract

The mount target should be a single empty container:

```html
<div class="bi-stack"></div>
```

The component adds `.bi-ltr` to the stack and emits one `.bi-card` inside.
Group icons reference an inline `<svg>` sprite at the top of `<body>` via
`<use href="#icon-purpose"/>` etc.
The sprite source lives at
[tools/design-system/assets/icons.svg](../../design-system/assets/icons.svg).

## Usage example

```html
<svg style="display:none"><!-- inline icon sprite --></svg>
<div class="bi-stack"></div>
<script src="card.js"></script>
<script>
  PracticalProseBiCard.mount(".bi-stack", payload);
</script>
```

## Source

The CSS and JS in this directory are extracted verbatim from
[tools/explorations/visual-design/dimension-visualizations.html](../../explorations/visual-design/dimension-visualizations.html).
The workbench links to these files via `<link>` and `<script src>`; the `pprose render`
pipeline mirrors them into its wheel via the sync script.
Edit the workbench file, then re-run
`uv run python tools/pprose/devtools/sync_render_html_styles.py`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
