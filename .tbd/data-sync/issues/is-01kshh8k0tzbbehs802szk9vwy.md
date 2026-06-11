---
type: is
id: is-01kshh8k0tzbbehs802szk9vwy
title: Update test_metrics, test_eval_report, test_eval_compare, test_cli for new schema
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshh8rsdpaxy249veyqk52tr
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T06:58:55.125Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-05-26T08:00:23.512Z
close_reason: "Superseded by spec rewrite 2026-05-26: pprose now depends on chopdiff BlockDoc (jlevy/chopdiff#8). Replaced by a slimmer pprose-only bead set under the same epic pp-3hg4."
---
Rewrite tools/pprose/tests/test_metrics.py to assert on the new *_count fields; add coverage for prose-only vs all_* distinction, for heading_outline + section rollups, and for distribution percentiles on a representative fixture. Update test_eval_report.py (currently references .sentences=50 / .paragraphs=25 in fixtures) and test_eval_compare.py similarly. Update test_cli.py for any output-format assertions. Where a fixture's expected number changes (e.g. a doc with 5 headings + 10 prose paragraphs now reports paragraph_count=10 instead of paragraphs=15), add a one-line comment in the test explaining why.
