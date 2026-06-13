---
type: is
id: is-01kskbrg8zxz91ccbjtpmffnct
title: "[chopdiff v0.4.x] Add Paragraph.list_info (ListInfo dataclass)"
kind: task
status: closed
priority: 3
version: 7
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
  - upstream-chopdiff
dependencies:
  - type: blocks
    target: is-01kskbs2ymzshjbfvnsg1wp8n9
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:01:14.014Z
updated_at: 2026-06-13T08:35:29.527Z
closed_at: 2026-06-13T08:35:29.526Z
close_reason: "Superseded by the chopdiff->flexdoc 0.1.0 migration: flexdoc ships all five typed APIs (code_info/table_info/list_info, frontmatter, NodeKind.footnote_ref), so these upstream-chopdiff requests are moot. pprose-side workaround removal tracked in pp-bcrw."
---
Tracked here; work in jlevy/chopdiff. Add a cached Paragraph.list_info: ListInfo | None property that walks the cached parse result's List node (when present) and returns ListInfo(ordered: bool, start: int | None, items: list[ListItemInfo], nesting_depth: int, total_item_count: int). ListItemInfo(text: str, children: list[ListInfo]) recursively describes nested lists. Enables pprose metrics: list_item_count, max_list_nesting_depth, ordered_list_count, unordered_list_count, max_list_item_count.

## Notes

chopdiff 0.3.1 audit: not exposed in 0.3.1. pprose has a clean source-text workaround, so this is an OPTIONAL upstream follow-up, not blocking. Filed as jlevy/chopdiff#20 on 2026-06-10 — see docs/project/chopdiff-upstream-requests.md.
