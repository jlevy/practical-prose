---
type: is
id: is-01ksey4r4mf12d0g2vp9cnzqpf
title: Reorder groups in source-of-truth YAMLs (rubric_schema, design-system)
kind: task
status: closed
priority: 2
version: 8
labels: []
dependencies:
  - type: blocks
    target: is-01ksey4wb77fjq0scc71zr7bva
  - type: blocks
    target: is-01ksey5009z243dqjkb7mnq8vg
  - type: blocks
    target: is-01ksey55erarj3za2eqdcn9bwq
  - type: blocks
    target: is-01ksey5yp32kt19vj1m19vjtye
  - type: blocks
    target: is-01ksey643p7cnvpg7ya5da45pb
parent_id: is-01ksey4hc3txw0a3f13445ahrm
created_at: 2026-05-25T06:46:17.491Z
updated_at: 2026-05-25T06:53:37.238Z
closed_at: 2026-05-25T06:53:37.237Z
close_reason: Swapped grounding/reasoning groups in rubric_schema.yaml and design-system.yaml; section numbers in rubric YAML shifted to match new position (Reasoning 11-14, Grounding 15-17); schema loader verifies new order.
---
Swap the order of the grounding and reasoning entries in:
- tools/pprose/src/pprose/rubric_schema.yaml (group definitions starting at line 134 grounding, 179 reasoning)
- tools/design-system/design-system.yaml (groups array, ids G/R)

These two files are the canonical sources for everything downstream. After this bead, the order across all derived assets will flow from these changes. Verify rubric_schema.py's GROUPS tuple picks up the new order automatically (no code change needed there).
