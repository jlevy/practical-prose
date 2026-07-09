---
type: is
id: is-01krw2kecm7z05st1fswn2jx8x
title: Add provider adapter interface and Anthropic Opus path
kind: task
status: open
priority: 2
version: 6
spec_path: null
labels: []
dependencies:
  - type: blocks
    target: is-01krw2kq1dqn3gd49waqcfccag
parent_id: is-01krvxewx2bjm707fh941e3dvk
created_at: 2026-05-17T22:58:39.123Z
updated_at: 2026-06-13T18:39:16.140Z
---
Wrap the current Anthropic Messages SDK scoring path in a small provider adapter without changing default single-report or --batch behavior. Add explicit coverage for anthropic/claude-opus-4-7 while leaving generic anthropic/<model> pass-through available.
