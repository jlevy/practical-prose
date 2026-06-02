---
title: tip-panels render component
description: Detail + Assessment side panels that update on hover
---
# tip-panels

The two side panels that mirror the rubric (Detail) and the per-doc evaluation
(Assessment) for whatever element the cursor is over.
The card component emits `[data-tip-kind="dim|group|score"]` triggers and these panels
listen on the document; hovering a dim updates both panels, hovering a group updates
just the Detail panel.

## Public API

```javascript
PracticalProseTipPanels.mount(detailSelector, assessSelector, data, biCardApi?);
```

| Argument | Description |
| --- | --- |
| `detailSelector` | CSS selector for the “Evaluation Detail” panel container. |
| `assessSelector` | CSS selector for the “Assessment” panel container. |
| `data` | Same shape as the bi-card data contract; see [bi-card/README.md](../bi-card/README.md). |
| `biCardApi` | Optional return value from `PracticalProseBiCard.mount(...)`. When provided, the Assessment panel mirrors the same `.bi-dim` widget for the hovered dimension; otherwise the mirror is omitted. |

## Dependencies

- `window.marked` — markdown library used for content rendering.
  Vendored at [../vendor/marked.min.js](../vendor/marked.min.js).

## DOM markup contract

```html
<aside class="bi-tip-panel"></aside>
<aside class="bi-tip-panel bi-tip-panel-assess"></aside>
```

The component appends a `.tip-panel-heading` and a `.tip-content` div to each; CSS keys
off `.is-empty` to hide chrome when there’s nothing to show.

## Source

CSS + JS extracted verbatim from
[tools/explorations/visual-design/dimension-visualizations.html](../../explorations/visual-design/dimension-visualizations.html).
