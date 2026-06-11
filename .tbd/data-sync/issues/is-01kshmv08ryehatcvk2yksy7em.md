---
type: is
id: is-01kshmv08ryehatcvk2yksy7em
title: "[chopdiff tracking] Expose Table sub-structure (rows, cells, alignment) on BlockDoc"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:01:24.246Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-05-27T00:00:53.895Z
close_reason: "Superseded by spec rewrite 2026-05-26 (v3). New architecture: chopdiff v0.4.x parses each block once and exposes typed accessors (heading_level, code_language, list_info, table_info, inlines, section_tree). Pprose becomes a thin serializer with no marko import and no per-block re-parse. Replaced by a fresh bead set."
---
Tracked here for visibility; the work itself happens in jlevy/chopdiff. The chopdiff PR #8 BlockDoc spec treats a table as a single Block. pprose needs: rows: list[Row], each row with cells: list[Cell] and header: bool; per-column alignment: left|right|center|None. Enables pprose metrics: table_row_count, table_cell_count, max_table_row_count, max_table_column_count. Additive and small; should land as a follow-on to the chopdiff BlockDoc epic chopdiff-d6js. When this lands upstream, bump the chopdiff pin in pprose and fill in the zero-defaulted fields in a small follow-up.
