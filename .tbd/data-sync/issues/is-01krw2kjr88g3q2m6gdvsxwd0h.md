---
type: is
id: is-01krw2kjr88g3q2m6gdvsxwd0h
title: Add OpenAI Responses adapter for GPT-5.5
kind: task
status: open
priority: 2
version: 5
spec_path: null
labels: []
dependencies:
  - type: blocks
    target: is-01krw2kq1dqn3gd49waqcfccag
parent_id: is-01krvxewx2bjm707fh941e3dvk
created_at: 2026-05-17T22:58:43.591Z
updated_at: 2026-06-13T18:39:16.317Z
---
Add an OpenAI Responses provider adapter for openai/gpt-5.5, including request construction, structured output handling, usage metadata, provider-specific model args such as reasoning.effort and max_output_tokens, and fake-client unit tests. Gate real network smoke coverage behind OPENAI_API_KEY and PROSE_EVAL_RUN_NETWORK_TESTS=1.
