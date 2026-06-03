---
type: is
id: is-01kt5ng18emf36s2q9q985vvxd
title: "Golden test: compare --format by-doc"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/release-readiness-2026-06.md
labels:
  - release
  - test
dependencies: []
parent_id: is-01kt5nebv6vqtrx17dfy0hy04m
created_at: 2026-06-03T02:37:42.029Z
updated_at: 2026-06-03T02:37:42.029Z
---
Risk #9 / automation candidate. Only compare's unified+pairs output is byte-locked (test_eval_compare golden); by-doc (render_per_doc_rollup: per-doc header line, group/overall means, numbered Violations, Quant/Derived tables) has no shape/golden test and can drift silently. Add a byte-golden against a committed expected fixture, the way unified+pairs is locked.
