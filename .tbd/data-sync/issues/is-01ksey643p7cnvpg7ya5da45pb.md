---
type: is
id: is-01ksey643p7cnvpg7ya5da45pb
title: Update visualization explorations for new canonical order
kind: task
status: closed
priority: 3
version: 3
labels: []
dependencies: []
parent_id: is-01ksey4hc3txw0a3f13445ahrm
created_at: 2026-05-25T06:47:02.517Z
updated_at: 2026-05-25T07:07:39.914Z
closed_at: 2026-05-25T07:07:39.908Z
close_reason: Updated dimension-icons-chooser.html DIM_LABELS/DIM_ORDER to PEFRGJ order; dimension-visualizations.html updated header-comment hue listing and Visual 9 narrative description for new canonical order; Visual 9 R-G-J right-column layout (lines 1714, 3081 area) preserved since it now matches canonical order. Hex-layout row comment at line 2319 updated to reflect new boundary.
---
The visualization explorations contain ordering references that should match the new canonical order. Visual 9 in dimension-visualizations.html already uses R-G-J on its right column (was deliberate for layout balance pre-change) — that layout stays as-is and will now align with the canonical order automatically.

Changes needed:
- tools/explorations/visual-design/dimension-icons-chooser.html:862 — const DIM_ORDER = ["p", "e", "f", "g", "r", "j"] → ["p", "e", "f", "r", "g", "j"]
- tools/explorations/visual-design/dimension-visualizations.html:33 — header comment listing hues 'Form=30, Grounding=162, Reasoning=329, Judgment=278' should swap G and R entries
- tools/explorations/visual-design/dimension-visualizations.html:3092 — narrative description text 'Grounding 158–166, Reasoning 323–332' should swap to match (but keep the Visual 9 layout descriptions intact — they're already R-G-J)
- Sweep both files for any other ordered listings (e.g. line 2319 'Grounding (3) + first Reasoning slot')

Lower priority (P3) since these are explorations, not production rendering.
