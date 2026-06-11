---
type: is
id: is-01kshmtgfac9gte43d945jgt0z
title: Rewrite Metrics dataclass + Metrics.from_block_doc + wire measure()
kind: task
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshmtgqj3dwkwny51xbspg22
  - type: blocks
    target: is-01kshmtgzfyr2ngrg267zgd9p8
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:01:08.069Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-05-27T00:00:52.794Z
close_reason: "Superseded by spec rewrite 2026-05-26 (v3). New architecture: chopdiff v0.4.x parses each block once and exposes typed accessors (heading_level, code_language, list_info, table_info, inlines, section_tree). Pprose becomes a thin serializer with no marko import and no per-block re-parse. Replaced by a fresh bead set."
---
Rewrite tools/pprose/src/pprose/metrics.py: replace Metrics dataclass with the new *_count schema (full field list in spec API Changes section — sizes, heading structure incl. heading_outline + max_heading_depth + heading_level_skip_count + mean_heading_word_count, list shape, table shape, code by language + total_code_line_count + inline_code_span_count, html, distributions, link/footnote counts derived from typed Inlines, bracket tags, bare urls, em-dash discipline, all lint *_count fields with _examples lists). Implement Metrics.from_block_doc(block_doc, file, *, words_per_page, banned_re) deriving every field via block_doc.filtered/iter_blocks/size + pprose.inlines + pprose.outline + pprose.distributions. Replace measure() to build BlockDoc once via chopdiff and call Metrics.from_block_doc. Delete strip_code_and_frontmatter and all regex-based structural counters (HEADING_RE, SETEXT_*, INLINE_LINK_RE, IMAGE_RE, AUTOLINK_RE, REF_LINK_*_RE, FOOTNOTE_*_RE, TABLE_SEP_RE, CODE_FENCE_RE, CODE_INLINE_RE, FRONTMATTER_RE). Keep lint regex constants and run them against text extracted from BlockDoc. Fields that depend on chopdiff follow-ons (table sub-structure, list metadata, code language) default to 0 / empty dict until those land.
