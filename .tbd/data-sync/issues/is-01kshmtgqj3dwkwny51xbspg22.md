---
type: is
id: is-01kshmtgqj3dwkwny51xbspg22
title: Rewrite format_human and format_summary_table for new schema
kind: task
status: open
priority: 1
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshmth7p8t647kk3y1qp3agx
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:01:08.336Z
updated_at: 2026-05-26T08:01:39.218Z
---
In tools/pprose/src/pprose/metrics.py: rewrite format_human to render the heading outline as an indented tree with section sizes (per the example in the spec Heading outline section); render the new list / table / code / distribution sections cleanly; render the existing lint sections (renamed). Rewrite format_summary_table column names to match the new *_count fields. Verify 'pprose metrics path/to/doc.md' and '--format yaml' / '--format json' produce sensible output on a representative fixture.
