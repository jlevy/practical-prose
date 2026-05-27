---
type: is
id: is-01kskbsx1f7fm5cmj1j6hca4qb
title: Rewrite Metrics + Metrics.from_text_doc (single walk; no marko in pprose)
kind: task
status: open
priority: 1
version: 3
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kskbsxbhfccjwmeh5sxmg8qm
  - type: blocks
    target: is-01kskbsxp15rfdps3qynmb3pft
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:01:59.850Z
updated_at: 2026-05-27T00:02:14.954Z
---
Rewrite tools/pprose/src/pprose/metrics.py to the *_count schema in the spec API Changes section. Implement Metrics.from_text_doc(text_doc, file, *, words_per_page, banned_re) as a single walk over the TextDoc, reading typed accessors from chopdiff: Paragraph.heading_level / heading_text, Paragraph.code_language / code_line_count, Paragraph.list_info, Paragraph.table_info, Paragraph.inlines, TextDoc.section_tree(). Build the heading_outline by walking section_tree and aggregating per-section rollups. Compute sentence-length and paragraph-length distributions (P50/P95/max in words) inline from sentence/paragraph .size(TextUnit.words). Run lint regexes (banned register, em-dash, replacement history, pedantic markers, generic headings, bracket tags, bare urls) against text_doc.filtered(include=PROSE_KINDS).reassemble(). Delete the regex-based structural counters and strip_code_and_frontmatter. Replace measure() to build TextDoc once and call Metrics.from_text_doc. NO 'import marko' in pprose anywhere.
