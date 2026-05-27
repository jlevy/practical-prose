---
type: is
id: is-01kshmv08ryehatcvk2yksy7em
title: "[chopdiff tracking] Expose Table sub-structure (rows, cells, alignment) on BlockDoc"
kind: task
status: open
priority: 2
version: 1
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:01:24.246Z
updated_at: 2026-05-26T08:01:24.246Z
---
Tracked here for visibility; the work itself happens in jlevy/chopdiff. The chopdiff PR #8 BlockDoc spec treats a table as a single Block. pprose needs: rows: list[Row], each row with cells: list[Cell] and header: bool; per-column alignment: left|right|center|None. Enables pprose metrics: table_row_count, table_cell_count, max_table_row_count, max_table_column_count. Additive and small; should land as a follow-on to the chopdiff BlockDoc epic chopdiff-d6js. When this lands upstream, bump the chopdiff pin in pprose and fill in the zero-defaulted fields in a small follow-up.
