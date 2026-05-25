---
type: is
id: is-01ksey5yp32kt19vj1m19vjtye
title: Regenerate test fixtures (expected-comparison + 9 eval.md goldens)
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01ksey4hc3txw0a3f13445ahrm
created_at: 2026-05-25T06:46:56.962Z
updated_at: 2026-05-25T07:06:31.960Z
closed_at: 2026-05-25T07:06:31.954Z
close_reason: Regenerated tools/pprose/tests/fixtures/expected-comparison.md from the figma-*.eval.md fixtures using 'pprose compare ... --format unified --pairs ...'. The 9 .eval.md input fixtures did not need regeneration (their YAML qual keys are alphabetical, parsed by Pydantic into the new declared field order). All 178 tests pass.
---
Once the YAML schema, Pydantic class order, and rendering code reflect the new group order, the golden test fixtures will no longer match. Regenerate:

- tools/pprose/tests/fixtures/expected-comparison.md — comparison table rows currently grouped Purpose, Expression, Form, Grounding, Reasoning, Judgment (lines 3-28)
- tools/pprose/tests/fixtures/*.eval.md (9 files): figma-ddog-r1/r2/r4.eval.md, figma-net-r1/r2/r4.eval.md, rev1-net.eval.md, rev2-net.eval.md, guidelines-self.eval.md — each contains rendered comparison tables and dimension listings in OLD order

Use the project's standard fixture regeneration mechanism (likely a pytest --update-goldens or a make target) rather than editing by hand. Diff the regenerated files to confirm the change is exclusively the G/R swap, not unintended drift.
