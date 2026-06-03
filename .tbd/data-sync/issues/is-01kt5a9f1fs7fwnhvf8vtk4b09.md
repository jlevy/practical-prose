---
type: is
id: is-01kt5a9f1fs7fwnhvf8vtk4b09
title: "Tests: round-trip stability, show formats, key-order assertion"
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-06-02-eval-output-improvements.md
labels: []
dependencies: []
parent_id: is-01kt58cf6h6hne026ebzgkmh1j
created_at: 2026-06-02T23:21:52.430Z
updated_at: 2026-06-03T19:15:13.899Z
closed_at: 2026-06-03T19:15:13.897Z
close_reason: Superseded by reporting CLI redesign epic pp-d2j3 (spec plan-2026-06-03-reporting-cli-redesign.md); work folded into its phases.
---
Unit tests: from_eval_md(to_eval_md(r))==r; pprose show mdyaml/yaml/json each parse back to same EvalReport; assert EVAL_REPORT_KEY_ORDER on a fully-populated fixture so the order stays pinned.
