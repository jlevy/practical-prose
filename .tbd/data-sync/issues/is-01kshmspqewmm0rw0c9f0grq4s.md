---
type: is
id: is-01kshmspqewmm0rw0c9f0grq4s
title: "pprose.inlines: typed Inline extraction via marko per-block walk"
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshmtgfac9gte43d945jgt0z
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:00:41.707Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-05-27T00:00:52.188Z
close_reason: "Superseded by spec rewrite 2026-05-26 (v3). New architecture: chopdiff v0.4.x parses each block once and exposes typed accessors (heading_level, code_language, list_info, table_info, inlines, section_tree). Pprose becomes a thin serializer with no marko import and no per-block re-parse. Replaced by a fresh bead set."
---
New module tools/pprose/src/pprose/inlines.py. Define frozen dataclasses Inline (base) + Text, Link (url, text, ref_id), Image (url, alt), AutoLink (url), CodeSpan (text), FootnoteRef (ref_id), LineBreak. Implement parse_inlines(block_text: str) -> list[Inline] by parsing the block's text with flowmark_markdown() and walking the inline tree of the resulting single Paragraph. Distinguish inline links / autolinks / reference-use links / images. See spec API Changes section for exact signatures.
