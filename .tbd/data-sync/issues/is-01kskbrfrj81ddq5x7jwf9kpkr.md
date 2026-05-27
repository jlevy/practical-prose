---
type: is
id: is-01kskbrfrj81ddq5x7jwf9kpkr
title: "[chopdiff v0.4.x] Add Paragraph.heading_level + heading_text"
kind: task
status: open
priority: 1
version: 3
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
dependencies:
  - type: blocks
    target: is-01kskbs2bmqjrb8884yn6yb5q7
  - type: blocks
    target: is-01kskbs2ymzshjbfvnsg1wp8n9
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:01:13.489Z
updated_at: 2026-05-27T00:02:12.962Z
---
Tracked here; work in jlevy/chopdiff. Add two cached properties on Paragraph: heading_level: int | None (1..6 for ATX/setext headings, None otherwise) and heading_text: str | None (heading content without the # prefix or underline). Both read from the cached parse result. Enables pprose metrics: heading_counts_by_level, max_heading_depth, heading_level_skip_count, and the heading_outline text/level fields.
