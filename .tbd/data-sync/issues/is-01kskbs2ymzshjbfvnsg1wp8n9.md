---
type: is
id: is-01kskbs2ymzshjbfvnsg1wp8n9
title: "[chopdiff v0.4.x] Cut v0.4.0 release with all additions"
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
dependencies:
  - type: blocks
    target: is-01kskbswph34xyby79hz0adr8v
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:01:33.138Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-06-03T05:04:26.123Z
close_reason: "Done: chopdiff 0.3.1 is published (PRs #12/#14/#15) and adopted. The remaining optional accessors are tracked as upstream follow-ups, not a release blocker."
---
Tracked here; work in jlevy/chopdiff. After the per-block parse cache + heading + code + list_info + table_info + inlines + section_tree all land, cut a v0.4.0 tagged release. This is what unblocks the pprose-side work. Update chopdiff CHANGELOG.md with the additions. Honor the 14-day cool-off policy.
