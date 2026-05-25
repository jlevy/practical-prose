---
type: is
id: is-01kseyakx300b76wphpapmf7fw
title: "P1: CI does not run new design-system or JS checks; CI runs only tools/pprose lint+tests, missing make lint-check, ruff on tools/design-system/, biome ci, generate.py --check (.github/workflows/ci.yml) (PR #12)"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01kseya645astqx3kpgr6fh4w6
created_at: 2026-05-25T06:49:29.762Z
updated_at: 2026-05-25T07:05:25.579Z
closed_at: 2026-05-25T07:05:25.578Z
close_reason: Added lint-root job to CI workflow that runs npm ci, design-system generator --check, top-level ruff on tools/design-system/, and biome ci. Also migrated biome.json from v1 to v2 schema (includes + assist.actions.organizeImports) and fixed pre-existing lint errors in exploration JS/HTML (useIterableCallbackReturn, noEmptyBlock).
---
