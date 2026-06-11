---
type: is
id: is-01kshh79hc3pnsfg4m0x4xht9r
title: Add derived counts, section rollups, and distribution helpers to DocStructure
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshh7mh28gs51p0ab5cp37vm
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T06:58:12.624Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-05-26T08:00:22.514Z
close_reason: "Superseded by spec rewrite 2026-05-26: pprose now depends on chopdiff BlockDoc (jlevy/chopdiff#8). Replaced by a slimmer pprose-only bead set under the same epic pp-3hg4."
---
On DocStructure: implement walk(), blocks_of(*kinds), and all derived count @property fields per spec API Changes section (heading_count, heading_counts_by_level, paragraph_count, sentence_count, word_count, list_item_count, blockquote_count, table_count, table_row_count, table_cell_count, fenced_code_count, html_block_count, all_sentence_count, all_paragraph_count). On Heading: implement .section -> SectionStats by walking forward from heading position until the next equal-or-shallower heading. Implement HeadingOutline construction over the full document. Implement percentile helpers (P50/P95/max in words) for sentence-length and paragraph-length distributions; use simple sorted-index percentiles (no numpy). Document the empty-doc rule (return 0).
