---
type: is
id: is-01kshmsq2vfk7ws48rt8vcm1hn
title: "pprose.outline: HeadingOutline + section rollups"
kind: task
status: open
priority: 1
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshmtgfac9gte43d945jgt0z
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:00:42.072Z
updated_at: 2026-05-26T08:01:38.354Z
---
New module tools/pprose/src/pprose/outline.py. Define frozen dataclass HeadingEntry (level, text, char_offset, word_count, section_word_count, section_sentence_count, section_paragraph_count, section_list_item_count, section_table_count, section_fenced_code_count). Implement build_outline(block_doc: BlockDoc) -> list[HeadingEntry]: for each heading block, find the span until the next equal-or-shallower heading (or end of doc), then aggregate counts via block_doc.iter_blocks filtered to relevant kinds. Render-ready: consumers should be able to display an indented outline with sizes per the example in the spec.
