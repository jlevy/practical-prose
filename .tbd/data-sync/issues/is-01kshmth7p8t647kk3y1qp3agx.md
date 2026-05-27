---
type: is
id: is-01kshmth7p8t647kk3y1qp3agx
title: Update test_metrics, test_eval_report, test_eval_compare, test_cli for new schema
kind: task
status: open
priority: 1
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshmthfgw30hr3ptx88y4ze9
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:01:08.852Z
updated_at: 2026-05-26T08:01:39.718Z
---
Rewrite tools/pprose/tests/test_metrics.py to assert on the new *_count fields. Add coverage for: prose-only vs all_* distinction, heading_outline + section rollups, distribution percentiles on a fixture with known sentence-length spread, inline link classification (external vs internal × inline vs autolink vs reference-use), and the lint regex sections running against extracted prose text. Update test_eval_report.py (currently references .sentences=50 / .paragraphs=25 in fixtures) and test_eval_compare.py similarly. Update test_cli.py for any output-format assertions. Where a fixture's expected number changes (e.g. a doc with 5 headings + 10 prose paragraphs now reports paragraph_count=10 instead of paragraphs=15), add a one-line comment in the test explaining why.
