---
type: is
id: is-01krhz1wf1bsx960qc78frs7sx
title: Wire Claude skill discovery
kind: task
status: open
priority: 2
version: 3
spec_path: tools/docs/project/specs/active/plan-2026-05-13-cross-agent-skills.md
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
updated_at: 2026-05-14T00:45:29.571Z
---
Add .claude/skills symlinks for all five canonical skills so Claude Code can discover them natively without duplicating skill files. Verify symlink targets are relative and portable.
