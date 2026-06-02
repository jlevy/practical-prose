---
type: is
id: is-01kt5a9ecp8t9evj7h09scbzac
title: Add top-level 'pprose show' command (mdyaml/yaml/json, --output)
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-06-02-eval-output-improvements.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt5a9f1fs7fwnhvf8vtk4b09
parent_id: is-01kt58cf6h6hne026ebzgkmh1j
created_at: 2026-06-02T23:21:51.765Z
updated_at: 2026-06-02T23:22:12.666Z
---
New pprose/show.py registered in cli.py COMMANDS under Evaluate (sibling of render). --format mdyaml|yaml|json (default mdyaml via to_eval_md; yaml via to_yaml; json via model_dump) and --output <path>; long flags only; infer format from --output extension when --format omitted; data->stdout, errors->stderr; read-only.
