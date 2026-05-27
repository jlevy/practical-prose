---
type: is
id: is-01kskbsxyw2mnmd6byddwy1kge
title: Update tests for new schema (test_metrics, test_eval_report, test_eval_compare, test_cli)
kind: task
status: open
priority: 1
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kskbsy6cmb5dxs9mdh75we1z
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:02:00.794Z
updated_at: 2026-05-27T00:02:15.536Z
---
Rewrite tools/pprose/tests/test_metrics.py to assert on the new *_count fields. Add coverage for: prose-only vs all_* distinction, heading_outline + section rollups, distribution percentiles on a fixture with known sentence-length spread, link classification (external vs internal × inline vs autolink vs reference-use), list_info counts, table_info counts, and the lint regex sections running against extracted prose text. Update test_eval_report.py (currently references .sentences=50 / .paragraphs=25 in fixtures) and test_eval_compare.py similarly. Update test_cli.py for output-format assertions. Where a fixture's expected number changes (e.g. a doc with 5 headings + 10 prose paragraphs now reports paragraph_count=10), add a one-line test comment explaining why.
