---
type: is
id: is-01kshmspqewmm0rw0c9f0grq4s
title: "pprose.inlines: typed Inline extraction via marko per-block walk"
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
created_at: 2026-05-26T08:00:41.707Z
updated_at: 2026-05-26T08:01:38.170Z
---
New module tools/pprose/src/pprose/inlines.py. Define frozen dataclasses Inline (base) + Text, Link (url, text, ref_id), Image (url, alt), AutoLink (url), CodeSpan (text), FootnoteRef (ref_id), LineBreak. Implement parse_inlines(block_text: str) -> list[Inline] by parsing the block's text with flowmark_markdown() and walking the inline tree of the resulting single Paragraph. Distinguish inline links / autolinks / reference-use links / images. See spec API Changes section for exact signatures.
