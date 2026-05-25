---
type: is
id: is-01ksey4wb77fjq0scc71zr7bva
title: Regenerate design-system outputs from updated YAML
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01ksey5yp32kt19vj1m19vjtye
parent_id: is-01ksey4hc3txw0a3f13445ahrm
created_at: 2026-05-25T06:46:21.798Z
updated_at: 2026-05-25T06:57:11.925Z
closed_at: 2026-05-25T06:57:11.921Z
close_reason: Ran tools/design-system/generate.py; regenerated design_system.css, design_system.js, design_system.global.js, and _generated/design_system.py — all six groups now follow P/E/F/R/G/J order in the generated outputs.
---
Run tools/design-system/generate.py (uv run --script tools/design-system/generate.py) and verify the regenerated files have the new group order:
- tools/design-system/_generated/design_system.css (--accent-g, --text-g, --surface-g, --dim-G* should now follow --*-r/R*)
- tools/design-system/_generated/design_system.js
- tools/design-system/_generated/design_system.global.js
- tools/pprose/src/pprose/_generated/design_system.py

These are auto-generated — never hand-edit. The regeneration command is documented in the file headers.
