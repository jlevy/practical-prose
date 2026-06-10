---
type: is
id: is-01krw2k8p07smp80c51q2bb2y0
title: Refresh pprose score targets and current model aliases
kind: task
status: closed
priority: 2
version: 8
spec_path: tools/docs/project/specs/active/plan-2026-05-23-pprose-score-loose-ends.md
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
updated_at: 2026-06-10T22:17:24.615Z
closed_at: 2026-06-10T22:17:24.614Z
close_reason: "Already done in commit b9e53f7 (2026-06-06): SUGGESTED_MODELS lists anthropic:claude-opus-4-8 as the opus flagship/default; aliases refreshed. Verified in eval_score.py during the 2026-06-10 bead audit."
---
Implement the current-code target/config cleanup in tools/pprose: refresh Anthropic aliases so Opus maps to claude-opus-4-7, decide/document the default model behavior, add a thin target parser for anthropic/<model> and openai/<model>, preserve --model as an Anthropic compatibility path, and keep examples focused on anthropic/claude-opus-4-7 plus openai/gpt-5.5.
