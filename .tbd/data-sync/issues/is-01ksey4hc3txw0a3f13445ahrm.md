---
type: is
id: is-01ksey4hc3txw0a3f13445ahrm
title: "Reorder dimension groups: Reasoning before Grounding"
kind: epic
status: closed
priority: 2
version: 12
labels: []
dependencies: []
child_order_hints:
  - is-01ksey4r4mf12d0g2vp9cnzqpf
  - is-01ksey4wb77fjq0scc71zr7bva
  - is-01ksey5009z243dqjkb7mnq8vg
  - is-01ksey55erarj3za2eqdcn9bwq
  - is-01ksey5dp301w6ez2712znmhnf
  - is-01ksey5h5vvsz6q4f42ne4emn6
  - is-01ksey5mryjv4zzgyz7kememkn
  - is-01ksey5rcgvrbvy9r5m08pqkrr
  - is-01ksey5yp32kt19vj1m19vjtye
  - is-01ksey643p7cnvpg7ya5da45pb
created_at: 2026-05-25T06:46:10.557Z
updated_at: 2026-05-25T07:09:06.926Z
closed_at: 2026-05-25T07:09:06.921Z
close_reason: "All 10 child beads completed: source YAMLs swapped, hand-ordered Python reordered, design-system schema/enums updated and outputs regenerated, all root docs/shortcuts/skills/AGENTS.md/agent-policy updated, packaged resources synced, expected-comparison.md golden regenerated, visualization explorations updated. All 178 tests pass; design-system --check passes; rubric_schema.GROUPS returns Purpose, Expression, Form, Reasoning, Grounding, Judgment."
---
Swap the canonical order of the Reasoning and Grounding groups so the six groups read: Purpose, Expression, Form, Reasoning, Grounding, Judgment. The change must propagate consistently across the source-of-truth YAMLs, generated design-system assets, hand-ordered Python code, all documentation, packaged resources, test fixtures, and visualization explorations. Visual 9 in dimension-visualizations.html already uses R-G-J on its right column; that layout will simply align with the new canonical order and does not need to change.
