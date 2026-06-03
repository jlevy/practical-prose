---
type: is
id: is-01krhz27s9axj15pcwy0ccpt2d
title: Prepare first pprose PyPI release
kind: task
status: open
priority: 1
version: 5
spec_path: tools/docs/project/specs/active/plan-2026-05-13-cross-agent-skills.md
labels:
  - cross-agent-skills
  - release
dependencies:
  - type: blocks
    target: is-01krhz2f5wsv5rwkvzz2c6mbaq
parent_id: is-01krhz0ckjzn0s26wggjjfays1
created_at: 2026-05-14T00:44:25.257Z
updated_at: 2026-06-03T02:38:56.030Z
---
Cut the first prose-eval package release after the unified CLI entry point is tested, so uvx prose-eval ... resolves without --from. If the PyPI package name changes, keep the package and console script names aligned so uvx <name> ... remains self-documenting.

## Notes

Package renamed from prose-eval → practical-prose → pprose (commits 9e243b0, 0384e6b, 05718e6).  Local release prep was completed.  Remaining external step: create/push a GitHub release tag and publish to PyPI via trusted publishing — needs explicit user approval.
