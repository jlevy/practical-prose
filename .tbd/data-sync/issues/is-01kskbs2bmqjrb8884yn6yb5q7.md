---
type: is
id: is-01kskbs2bmqjrb8884yn6yb5q7
title: "[chopdiff v0.4.x] Add TextDoc.section_tree()"
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
dependencies:
  - type: blocks
    target: is-01kskbs2ymzshjbfvnsg1wp8n9
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:01:32.531Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-06-03T05:04:26.871Z
close_reason: "Shipped in 0.3.1: TextDoc.sections() + toc() + section_size_tree() (the section tree this asked for, under different names)."
---
Tracked here; work in jlevy/chopdiff. Add TextDoc.section_tree() -> list[Section] returning the document's heading hierarchy. Section(heading: Paragraph | None, level: int, children: list[Paragraph]) covers every block; sibling sections at the same level are flat in the list; deeper levels nest under their parent. Blocks before the first heading go under a synthetic Section(heading=None, level=0). Setext-safe and #-in-code-safe (uses heading_level from cached parse result). Enables pprose heading_outline with per-section rollups.
