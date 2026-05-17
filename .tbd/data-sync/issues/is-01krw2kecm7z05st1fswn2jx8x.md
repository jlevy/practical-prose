---
type: is
id: is-01krw2kecm7z05st1fswn2jx8x
title: Add provider adapter interface and Anthropic Opus path
kind: task
status: open
priority: 2
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-17-eval-tool-and-model-configuration.md
labels: []
dependencies:
  - type: blocks
    target: is-01krw2kq1dqn3gd49waqcfccag
parent_id: is-01krvxewx2bjm707fh941e3dvk
created_at: 2026-05-17T22:58:39.123Z
updated_at: 2026-05-17T22:59:22.374Z
---
Introduce the provider adapter boundary for scoring calls. Move the current Anthropic Messages behavior behind an adapter without changing default behavior, and add explicit coverage/config for anthropic/claude-opus-4-7 while leaving generic anthropic/<model> parsing available.
