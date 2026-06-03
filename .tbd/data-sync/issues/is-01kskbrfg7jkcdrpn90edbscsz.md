---
type: is
id: is-01kskbrfg7jkcdrpn90edbscsz
title: "[chopdiff v0.4.x] Cache per-block marko parse result on Paragraph"
kind: task
status: closed
priority: 1
version: 7
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
dependencies:
  - type: blocks
    target: is-01kskbrfrj81ddq5x7jwf9kpkr
  - type: blocks
    target: is-01kskbrg0px9w2baeeeryg896a
  - type: blocks
    target: is-01kskbrg8zxz91ccbjtpmffnct
  - type: blocks
    target: is-01kskbrggva8sp3ssqraq86a4t
  - type: blocks
    target: is-01kskbs23rrda0270vpc2wxn7j
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:01:13.219Z
updated_at: 2026-06-03T05:04:26.363Z
closed_at: 2026-06-03T05:04:26.362Z
close_reason: "Shipped in 0.3.1: Paragraph.block_type is a @cached_property and TextDoc.blocks() memoizes the parse on source_text."
---
Tracked here for visibility; work happens in jlevy/chopdiff. Today Paragraph.block_type calls _markdown_parser().parse(text) via _classify_block and discards the parsed tree. Refactor to cache the parsed element (e.g. Paragraph._parsed_element as a @cached_property) so every other typed accessor (heading_level, code_language, list_info, table_info, inlines) can read from the same parse. Pure internal refactor; no public API change. Foundation for the other v0.4.x additions.
