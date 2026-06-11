---
type: is
id: is-01kshmsqeapneg35whw8589qq8
title: "pprose.distributions: percentile helpers"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshmtgfac9gte43d945jgt0z
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:00:42.441Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-05-27T00:00:52.608Z
close_reason: "Superseded by spec rewrite 2026-05-26 (v3). New architecture: chopdiff v0.4.x parses each block once and exposes typed accessors (heading_level, code_language, list_info, table_info, inlines, section_tree). Pprose becomes a thin serializer with no marko import and no per-block re-parse. Replaced by a fresh bead set."
---
New module tools/pprose/src/pprose/distributions.py with percentiles(values: list[int], pcts: tuple[int, ...]) -> dict[int, int] using simple sorted-index percentiles (no numpy dependency). Empty input rule: return {p: 0 for p in pcts}. Used to compute sentence_length_p50_words / p95 / max and the paragraph variants in Metrics.from_block_doc.
