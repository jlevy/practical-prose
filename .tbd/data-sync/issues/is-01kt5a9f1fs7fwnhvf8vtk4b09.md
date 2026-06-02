---
type: is
id: is-01kt5a9f1fs7fwnhvf8vtk4b09
title: "Tests: round-trip stability, show formats, key-order assertion"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-06-02-eval-output-improvements.md
labels: []
dependencies: []
parent_id: is-01kt58cf6h6hne026ebzgkmh1j
created_at: 2026-06-02T23:21:52.430Z
updated_at: 2026-06-02T23:21:52.430Z
---
Unit tests: from_eval_md(to_eval_md(r))==r; pprose show mdyaml/yaml/json each parse back to same EvalReport; assert EVAL_REPORT_KEY_ORDER on a fully-populated fixture so the order stays pinned.
