---
type: is
id: is-01kshh7sfsr9n4v149kn43xsr3
title: Refactor Metrics dataclass and implement Metrics.from_structure
kind: task
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshh860nz3ttj6b5qe1p3wdf
  - type: blocks
    target: is-01kshh8aayzyqp4cxmgvamzsq6
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T06:58:28.955Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-05-26T08:00:22.902Z
close_reason: "Superseded by spec rewrite 2026-05-26: pprose now depends on chopdiff BlockDoc (jlevy/chopdiff#8). Replaced by a slimmer pprose-only bead set under the same epic pp-3hg4."
---
Rewrite Metrics in pprose/metrics.py to the new *_count schema (full field list in spec API Changes section: sizes, structure incl. heading_outline + max_heading_depth + heading_level_skip_count + mean_heading_word_count, list shape, table shape, code by language + total_code_line_count + inline_code_span_count, html, distributions, link/footnote counts derived from typed Inlines, bracket tags, bare urls, em-dash discipline, all lint *_count fields with _examples lists). Implement Metrics.from_structure(structure, file, *, words_per_page, banned_re). Link classification (external vs internal vs inline vs autolink vs reference-use vs image) comes from walking Inline objects, NOT regex. Keep existing lint regex constants and run them against concatenated prose text from DocStructure. See spec rename table for every field rename.
