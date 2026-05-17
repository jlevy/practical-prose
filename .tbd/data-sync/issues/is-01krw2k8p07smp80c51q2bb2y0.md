---
type: is
id: is-01krw2k8p07smp80c51q2bb2y0
title: Add score target/config primitives
kind: task
status: open
priority: 2
version: 4
spec_path: tools/docs/project/specs/active/plan-2026-05-17-eval-tool-and-model-configuration.md
labels: []
dependencies:
  - type: blocks
    target: is-01krw2kecm7z05st1fswn2jx8x
  - type: blocks
    target: is-01krw2kjr88g3q2m6gdvsxwd0h
  - type: blocks
    target: is-01krw2kwyemv5gswppedwfpqn4
parent_id: is-01krvxewx2bjm707fh941e3dvk
created_at: 2026-05-17T22:58:33.279Z
updated_at: 2026-05-17T22:59:17.634Z
---
Implement the thin target/config layer from the spec: parse provider/model target ids, load default_target/default_concurrency/comparison_targets from config, merge CLI overrides, preserve the existing --model compatibility path, and focus built-in examples on openai/gpt-5.5 plus anthropic/claude-opus-4-7.
