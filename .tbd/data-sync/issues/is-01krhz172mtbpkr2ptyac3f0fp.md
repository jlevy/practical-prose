---
type: is
id: is-01krhz172mtbpkr2ptyac3f0fp
title: Test prose-eval subcommand CLI surface
kind: task
status: open
priority: 2
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-13-cross-agent-skills.md
labels:
  - cross-agent-skills
  - testing
dependencies:
  - type: blocks
    target: is-01krhz27s9axj15pcwy0ccpt2d
parent_id: is-01krhz0ckjzn0s26wggjjfays1
created_at: 2026-05-14T00:43:51.763Z
updated_at: 2026-05-14T00:45:29.207Z
---
Add focused tests for the unified CLI: prose-eval --help lists metrics/score/report/compare, each subcommand help exits 0 and describes the workflow, uv run prose-eval <subcommand> dispatches like the compatibility scripts on a small fixture, and stdout/stderr/progress behavior remains agent-friendly in non-TTY or CI contexts.
