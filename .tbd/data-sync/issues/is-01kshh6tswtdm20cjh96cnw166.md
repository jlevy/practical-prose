---
type: is
id: is-01kshh6tswtdm20cjh96cnw166
title: Build pprose.structure Block & Inline type hierarchies
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshh744sg1n3wdx5wsxa6dqg
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T06:57:57.538Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-05-26T08:00:22.078Z
close_reason: "Superseded by spec rewrite 2026-05-26: pprose now depends on chopdiff BlockDoc (jlevy/chopdiff#8). Replaced by a slimmer pprose-only bead set under the same epic pp-3hg4."
---
New module tools/pprose/src/pprose/structure.py. Define dataclasses ONLY (no parsing yet): the Inline base + Text, Link, Image, AutoLink, CodeSpan, FootnoteRef, LineBreak; the Block base + ProseBlock mixin (holds chopdiff TextDoc); concrete blocks Document, Heading (level), Paragraph, List (ordered, loose, start, items), ListItem (nesting_depth, children), BlockQuote (children), Table (header_row, rows, alignments), TableRow (cells), TableCell (header, alignment), FencedCode (language, code), IndentedCode (code), HTMLBlock (raw), ThematicBreak, FootnoteDef (ref_id), LinkRefDef (ref_id, url). Plus SectionStats and HeadingOutline frozen dataclasses. See spec API Changes section for full signatures.
