---
type: is
id: is-01kx3zk4jspvc0y1dgdz9b7w8x
title: Add rule-number stability policy to rubric versioning
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-07-09T17:42:46.105Z
updated_at: 2026-07-09T17:42:46.105Z
---
Eval reports cite findings by dimension + rule_number, so rule numbers are load-bearing identifiers. Inserting a rule mid-list would renumber later rules and silently re-target every archived eval report. Add to practical-prose-rubric.md's Versioning section: rule additions are append-only; renumbering requires a rubric version bump. (G1.7 'Links serve readers' was correctly appended, and rubric_schema.yaml now carries it.)
