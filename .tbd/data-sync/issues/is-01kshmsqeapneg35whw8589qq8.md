---
type: is
id: is-01kshmsqeapneg35whw8589qq8
title: "pprose.distributions: percentile helpers"
kind: task
status: open
priority: 2
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshmtgfac9gte43d945jgt0z
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:00:42.441Z
updated_at: 2026-05-26T08:01:38.573Z
---
New module tools/pprose/src/pprose/distributions.py with percentiles(values: list[int], pcts: tuple[int, ...]) -> dict[int, int] using simple sorted-index percentiles (no numpy dependency). Empty input rule: return {p: 0 for p in pcts}. Used to compute sentence_length_p50_words / p95 / max and the paragraph variants in Metrics.from_block_doc.
