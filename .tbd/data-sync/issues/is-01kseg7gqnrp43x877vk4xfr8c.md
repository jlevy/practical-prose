---
type: is
id: is-01kseg7gqnrp43x877vk4xfr8c
title: "Design-system: add tests for the generator"
kind: task
status: open
priority: 2
version: 1
labels:
  - design-system
  - test
dependencies: []
created_at: 2026-05-25T02:43:08.148Z
updated_at: 2026-05-25T02:43:08.148Z
---
Add tools/design-system/tests/ (or under tools/pprose/tests/) covering:
- Pydantic schema validates the canonical YAML (no regression in shape)
- generate.py is idempotent: run twice, --check exits 0
- Emitter outputs are well-formed: JS parses (node --check), CSS has expected --accent-*/--surface-*/--dim-* tokens, Python module imports + DESIGN_SYSTEM has expected keys
- Round-trip: per-dim colors are computed correctly from group H/S + h_offset + L

Currently the generator has zero test coverage; a schema or emitter regression would only surface when downstream consumers break.
