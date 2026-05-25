---
type: is
id: is-01kseg7hf7c3jk7sqbyp07r3qp
title: "table_styles: use per-dimension colors for table cell backgrounds"
kind: feature
status: open
priority: 3
version: 1
labels:
  - design-system
  - pprose
dependencies: []
created_at: 2026-05-25T02:43:08.902Z
updated_at: 2026-05-25T02:43:08.902Z
---
Currently _dimension_styles() in tools/pprose/src/pprose/table_styles.py expands each dim to inherit its parent group's uniform surface/ink.  The generated DESIGN_SYSTEM dict now ships per-dimension colors (rotated H around the group hue), which would give each dim row a distinguishable sub-hue within its group.

The current comment notes the choice is 'reserved for visualizations that draw the dim mark directly; for cell backgrounds in tables the uniform group color reads as a clearer block.'  Worth revisiting once a renderer is using the design system end-to-end — small per-row hue variation may help differentiate adjacent dims without sacrificing the block-reading effect.
