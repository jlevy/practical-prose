---
type: is
id: is-01kskbrggva8sp3ssqraq86a4t
title: "[chopdiff v0.4.x] Add Paragraph.table_info (TableInfo dataclass)"
kind: task
status: open
priority: 3
version: 6
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
  - upstream-chopdiff
dependencies:
  - type: blocks
    target: is-01kskbs2ymzshjbfvnsg1wp8n9
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:01:14.262Z
updated_at: 2026-06-11T16:21:46.496Z
---
Tracked here; work in jlevy/chopdiff. Add a cached Paragraph.table_info: TableInfo | None property that walks the cached parse result's Table node (GFM) when present and returns TableInfo(header_cells: list[str], body_rows: list[list[str]], alignments: list[str | None], row_count: int, column_count: int). alignments is per-column ('left' / 'right' / 'center' / None). Enables pprose metrics: table_row_count, table_cell_count, max_table_row_count, max_table_column_count.

## Notes

chopdiff 0.3.1 audit: not exposed in 0.3.1. pprose has a clean source-text workaround, so this is an OPTIONAL upstream follow-up, not blocking. Filed as jlevy/chopdiff#19 on 2026-06-10 — see docs/project/chopdiff-upstream-requests.md.
