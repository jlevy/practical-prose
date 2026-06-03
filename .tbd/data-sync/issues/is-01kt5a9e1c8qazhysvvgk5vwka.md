---
type: is
id: is-01kt5a9e1c8qazhysvvgk5vwka
title: Define EVAL_REPORT_KEY_ORDER + migrate EvalReport.to_yaml() to frontmatter-format
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-06-02-eval-output-improvements.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt5a9ecp8t9evj7h09scbzac
  - type: blocks
    target: is-01kt5a9eq9h2cyxtnczrx3p6n7
parent_id: is-01kt58cf6h6hne026ebzgkmh1j
created_at: 2026-06-02T23:21:51.402Z
updated_at: 2026-06-03T19:15:12.931Z
closed_at: 2026-06-03T19:15:12.928Z
close_reason: Superseded by reporting CLI redesign epic pp-d2j3 (spec plan-2026-06-03-reporting-cli-redesign.md); work folded into its phases.
---
Add the flat EVAL_REPORT_KEY_ORDER constant (depth-first schema order; 'total' placed after h6/before links leaves). Replace pyyaml.safe_dump in to_yaml() with to_yaml_string(key_sort=custom_key_sort(EVAL_REPORT_KEY_ORDER)). Keep include_table_styles. Confirm to_eval_md/from_eval_md/from_yaml round-trip + derived recompute stable.
