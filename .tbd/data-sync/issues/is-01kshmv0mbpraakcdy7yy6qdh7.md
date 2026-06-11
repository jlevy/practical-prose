---
type: is
id: is-01kshmv0mbpraakcdy7yy6qdh7
title: "[chopdiff tracking] Expose List metadata (ordered, start, nesting depth) on BlockDoc"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:01:24.619Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-05-27T00:00:54.125Z
close_reason: "Superseded by spec rewrite 2026-05-26 (v3). New architecture: chopdiff v0.4.x parses each block once and exposes typed accessors (heading_level, code_language, list_info, table_info, inlines, section_tree). Pprose becomes a thin serializer with no marko import and no per-block re-parse. Replaced by a fresh bead set."
---
Tracked here for visibility; the work itself happens in jlevy/chopdiff. Expose ordered: bool, start: int | None on List blocks; nesting_depth: int on ListItem blocks. Enables pprose metrics: ordered_list_count, unordered_list_count, max_list_nesting_depth, max_list_item_count. Additive; landing as a follow-on to chopdiff BlockDoc epic chopdiff-d6js. When this lands upstream, bump the chopdiff pin and fill in the zero-defaulted fields.
