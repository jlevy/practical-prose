---
type: is
id: is-01kskbrg8zxz91ccbjtpmffnct
title: "[chopdiff v0.4.x] Add Paragraph.list_info (ListInfo dataclass)"
kind: task
status: open
priority: 1
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
dependencies:
  - type: blocks
    target: is-01kskbs2ymzshjbfvnsg1wp8n9
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:01:14.014Z
updated_at: 2026-05-27T00:02:13.466Z
---
Tracked here; work in jlevy/chopdiff. Add a cached Paragraph.list_info: ListInfo | None property that walks the cached parse result's List node (when present) and returns ListInfo(ordered: bool, start: int | None, items: list[ListItemInfo], nesting_depth: int, total_item_count: int). ListItemInfo(text: str, children: list[ListInfo]) recursively describes nested lists. Enables pprose metrics: list_item_count, max_list_nesting_depth, ordered_list_count, unordered_list_count, max_list_item_count.
