---
type: is
id: is-01krfgex27av7wzazhyn8hkj6v
title: "Phase 1: Extend ReproContext with cache_stats + sdk_version"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md
labels: []
dependencies:
  - type: blocks
    target: is-01krfgexb0348x9s50y4y51pev
parent_id: is-01krfgdgghp4x3rtpyk0kd4r1n
created_at: 2026-05-13T01:50:42.758Z
updated_at: 2026-05-13T02:17:04.249Z
closed_at: 2026-05-13T02:17:04.248Z
close_reason: ReproContext gained model_id, sdk_version, cache_stats fields. EvalMetadata schema extended with the same fields (model_id, sdk_version, cache_stats). merge_into_report persists them under metadata.repro. method string updated to 'model (anthropic SDK)'.
---
Persist anthropic response's usage.cache_creation_input_tokens and usage.cache_read_input_tokens into metadata.repro.cache_stats. Add metadata.repro.sdk_version = anthropic.__version__. Keep prompt_sha256 computed over the rendered prompt text so it stays comparable to historical YAMLs.
