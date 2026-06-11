---
type: is
id: is-01kskbsxp15rfdps3qynmb3pft
title: Update eval_report.py and eval_compare.py for renamed fields
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kskbsxyw2mnmd6byddwy1kge
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:02:00.509Z
updated_at: 2026-06-11T16:21:46.496Z
---
In tools/pprose/src/pprose/eval_report.py: the SizeBlock pydantic model (~line 86-87) has 'sentences' / 'paragraphs' fields; rename to sentence_count / paragraph_count. Density math (~line 635-642) reads metrics.sentences / .paragraphs / .words; switch to .sentence_count / .paragraph_count / .word_count. In tools/pprose/src/pprose/eval_compare.py: column lambdas at ~line 120-274 reference r.quant.size.sentences / .paragraphs and the derived density block — update field accesses to the new names. Run 'pprose report' and 'pprose compare' on a fixture to verify output renders correctly.
