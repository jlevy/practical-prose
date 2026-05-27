---
type: is
id: is-01kshmv0mbpraakcdy7yy6qdh7
title: "[chopdiff tracking] Expose List metadata (ordered, start, nesting depth) on BlockDoc"
kind: task
status: open
priority: 2
version: 1
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:01:24.619Z
updated_at: 2026-05-26T08:01:24.619Z
---
Tracked here for visibility; the work itself happens in jlevy/chopdiff. Expose ordered: bool, start: int | None on List blocks; nesting_depth: int on ListItem blocks. Enables pprose metrics: ordered_list_count, unordered_list_count, max_list_nesting_depth, max_list_item_count. Additive; landing as a follow-on to chopdiff BlockDoc epic chopdiff-d6js. When this lands upstream, bump the chopdiff pin and fill in the zero-defaulted fields.
