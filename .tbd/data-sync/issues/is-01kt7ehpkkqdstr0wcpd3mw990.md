---
type: is
id: is-01kt7ehpkkqdstr0wcpd3mw990
title: "Phase 1: shared report-view + frontmatter-format YAML writer"
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-06-03-reporting-cli-redesign.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt7ehpz8mfmpb8byqdf68wdw
parent_id: is-01kt7eh75j40zhgrbbkrrv6kc9
created_at: 2026-06-03T19:14:45.490Z
updated_at: 2026-06-03T19:15:10.982Z
---
Add pinned frontmatter-format dep (+ supply-chain record); add EVAL_REPORT_KEY_ORDER and migrate EvalReport.to_yaml to frontmatter-format with custom_key_sort; build the shared report-view model (groups/dims, scores, reasons, findings+formatted locations, violations, quant rows, derived ratios, rollup, metadata) and move _format_locations onto it; re-express render_single_doc_rollup (md body) and the HTML build_payload to render from that one view so locations + quant tables reach every format.
