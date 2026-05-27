---
type: is
id: is-01kshmsq2vfk7ws48rt8vcm1hn
title: "pprose.outline: HeadingOutline + section rollups"
kind: task
status: closed
priority: 1
version: 3
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshmtgfac9gte43d945jgt0z
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:00:42.072Z
updated_at: 2026-05-27T00:00:52.392Z
closed_at: 2026-05-27T00:00:52.391Z
close_reason: "Superseded by spec rewrite 2026-05-26 (v3). New architecture: chopdiff v0.4.x parses each block once and exposes typed accessors (heading_level, code_language, list_info, table_info, inlines, section_tree). Pprose becomes a thin serializer with no marko import and no per-block re-parse. Replaced by a fresh bead set."
---
New module tools/pprose/src/pprose/outline.py. Define frozen dataclass HeadingEntry (level, text, char_offset, word_count, section_word_count, section_sentence_count, section_paragraph_count, section_list_item_count, section_table_count, section_fenced_code_count). Implement build_outline(block_doc: BlockDoc) -> list[HeadingEntry]: for each heading block, find the span until the next equal-or-shallower heading (or end of doc), then aggregate counts via block_doc.iter_blocks filtered to relevant kinds. Render-ready: consumers should be able to display an indented outline with sizes per the example in the spec.
