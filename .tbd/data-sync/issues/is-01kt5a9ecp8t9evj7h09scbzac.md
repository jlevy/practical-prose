---
type: is
id: is-01kt5a9ecp8t9evj7h09scbzac
title: Add top-level 'pprose show' command (mdyaml/yaml/json, --output)
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-06-02-eval-output-improvements.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt5a9f1fs7fwnhvf8vtk4b09
parent_id: is-01kt58cf6h6hne026ebzgkmh1j
created_at: 2026-06-02T23:21:51.765Z
updated_at: 2026-06-03T19:15:13.215Z
closed_at: 2026-06-03T19:15:13.214Z
close_reason: Superseded by reporting CLI redesign epic pp-d2j3 (spec plan-2026-06-03-reporting-cli-redesign.md); work folded into its phases.
---
New pprose/show.py registered in cli.py COMMANDS under Evaluate (sibling of render). --format mdyaml|yaml|json (default mdyaml via to_eval_md; yaml via to_yaml; json via model_dump) and --output <path>; long flags only; infer format from --output extension when --format omitted; data->stdout, errors->stderr; read-only.
