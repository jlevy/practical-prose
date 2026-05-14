---
type: is
id: is-01krhz12n33ecbdyrwb0c07ght
title: Add unified prose-eval CLI entry point
kind: task
status: open
priority: 2
version: 3
spec_path: tools/docs/project/specs/active/plan-2026-05-13-cross-agent-skills.md
labels:
  - cross-agent-skills
  - cli
dependencies:
  - type: blocks
    target: is-01krhz172mtbpkr2ptyac3f0fp
  - type: blocks
    target: is-01krhz1m2ae7n8ghbjnjjeqcsz
parent_id: is-01krhz0ckjzn0s26wggjjfays1
created_at: 2026-05-14T00:43:47.234Z
updated_at: 2026-05-14T00:45:28.464Z
---
Implement the spec's single public CLI surface in tools/prose-eval: add src/prose_eval/cli.py, expose prose-eval = prose_eval.cli:main, route metrics/score/report/compare subcommands to existing implementations, preserve compatibility aliases unless a concrete maintenance issue appears, and keep help/output automation-friendly.
