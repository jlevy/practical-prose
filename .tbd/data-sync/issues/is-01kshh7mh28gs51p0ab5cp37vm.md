---
type: is
id: is-01kshh7mh28gs51p0ab5cp37vm
title: Unit tests for pprose.structure
kind: task
status: closed
priority: 1
version: 3
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshh7sfsr9n4v149kn43xsr3
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T06:58:23.897Z
updated_at: 2026-05-26T08:00:22.719Z
closed_at: 2026-05-26T08:00:22.716Z
close_reason: "Superseded by spec rewrite 2026-05-26: pprose now depends on chopdiff BlockDoc (jlevy/chopdiff#8). Replaced by a slimmer pprose-only bead set under the same epic pp-3hg4."
---
Hand-built Markdown fixtures covering: nested ordered/unordered lists (any depth), GFM tables (with left/right/center alignment), fenced code (with and without language), indented code, footnote defs / refs, blockquotes containing lists, headings with inline code/links/images, setext headings, thematic breaks that DON'T false-trigger as setext, HTML blocks, YAML frontmatter, link reference definitions, autolinks vs inline links vs reference-use links, deeply nested ListItem with nested List + sibling Paragraph (verifies prose attribution rules). Assert: block kinds, per-kind fields, prose-only sentence/paragraph counts, all_* counts, heading_outline order and section rollups, distribution percentiles on a doc with known sentence-length spread. See spec Prose inclusion rules table for what each fixture should resolve to.
