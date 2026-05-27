---
type: is
id: is-01kshmtgfac9gte43d945jgt0z
title: Rewrite Metrics dataclass + Metrics.from_block_doc + wire measure()
kind: task
status: open
priority: 1
version: 3
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshmtgqj3dwkwny51xbspg22
  - type: blocks
    target: is-01kshmtgzfyr2ngrg267zgd9p8
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:01:08.069Z
updated_at: 2026-05-26T08:01:39.018Z
---
Rewrite tools/pprose/src/pprose/metrics.py: replace Metrics dataclass with the new *_count schema (full field list in spec API Changes section — sizes, heading structure incl. heading_outline + max_heading_depth + heading_level_skip_count + mean_heading_word_count, list shape, table shape, code by language + total_code_line_count + inline_code_span_count, html, distributions, link/footnote counts derived from typed Inlines, bracket tags, bare urls, em-dash discipline, all lint *_count fields with _examples lists). Implement Metrics.from_block_doc(block_doc, file, *, words_per_page, banned_re) deriving every field via block_doc.filtered/iter_blocks/size + pprose.inlines + pprose.outline + pprose.distributions. Replace measure() to build BlockDoc once via chopdiff and call Metrics.from_block_doc. Delete strip_code_and_frontmatter and all regex-based structural counters (HEADING_RE, SETEXT_*, INLINE_LINK_RE, IMAGE_RE, AUTOLINK_RE, REF_LINK_*_RE, FOOTNOTE_*_RE, TABLE_SEP_RE, CODE_FENCE_RE, CODE_INLINE_RE, FRONTMATTER_RE). Keep lint regex constants and run them against text extracted from BlockDoc. Fields that depend on chopdiff follow-ons (table sub-structure, list metadata, code language) default to 0 / empty dict until those land.
