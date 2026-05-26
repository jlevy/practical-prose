---
type: is
id: is-01kshh744sg1n3wdx5wsxa6dqg
title: "Implement build_structure: marko walk to typed Block tree"
kind: task
status: open
priority: 1
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshh79hc3pnsfg4m0x4xht9r
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T06:58:07.128Z
updated_at: 2026-05-26T06:59:10.479Z
---
Implement build_structure(raw_md, *, sentence_splitter=None) -> DocStructure in pprose/structure.py. Parses via flowmark_markdown().parse(); walks the marko AST and translates each node to the corresponding pprose Block. For prose-bearing blocks (Paragraph, ListItem, BlockQuote, FootnoteDef), constructs a chopdiff.TextDoc from the block's plain text using the provided splitter (default flowmark.split_sentences_regex). For each block extracts a list[Inline] from marko inlines. Strip YAML frontmatter via the parser, not regex. Preserve original char ranges on Block.char_range. See spec Approach step 2 and the Prose inclusion rules table for what's prose-bearing.
