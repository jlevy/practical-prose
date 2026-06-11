---
type: is
id: is-01krhz1wf1bsx960qc78frs7sx
title: Wire Claude skill discovery
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/done/plan-2026-05-13-cross-agent-skills.md
labels:
  - cross-agent-skills
  - docs
dependencies:
  - type: blocks
    target: is-01krhz20668axryc1y423xcs5h
  - type: blocks
    target: is-01krhz2f5wsv5rwkvzz2c6mbaq
parent_id: is-01krhz0ckjzn0s26wggjjfays1
created_at: 2026-05-14T00:44:13.664Z
updated_at: 2026-06-11T16:21:45.875Z
closed_at: 2026-05-14T01:06:10.032Z
close_reason: Added relative .claude/skills symlinks for all five canonical skills and verified targets resolve.
---
Add .claude/skills symlinks for all five canonical skills so Claude Code can discover them natively without duplicating skill files. Verify symlink targets are relative and portable.
