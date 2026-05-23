---
type: is
id: is-01ks97pmpnytq5mjeg6becv852
title: Update LLM scoring prompt (eval-rubric-score.md) to include Parsimony
kind: chore
status: closed
priority: 2
version: 3
labels:
  - rubric-rollout
  - parsimony
  - code
dependencies:
  - type: blocks
    target: is-01ks97q4vvxq99hpdhpt396gvy
parent_id: is-01ks97m4tenhgn7w974et1nrnk
created_at: 2026-05-23T01:37:54.388Z
updated_at: 2026-05-23T02:12:36.356Z
closed_at: 2026-05-23T02:12:36.356Z
close_reason: Implemented as part of the combined 20-dim-v1 rollout (commit on claude/vibrant-goldberg-828VB)
---
Update tools/prose-eval/src/prose_eval/prompts/eval-rubric-score.md — the prompt sent to Claude for model-scoring.

## Changes

1. **Canonical dimension name list (around lines 27-29):** Insert `Parsimony` between `Precision` and `Calibration`.

2. **JSON example block (around lines 53-73):** Insert `"parsimony": {"score": 0, "reason": "..."}` between the `precision` and `calibration` entries.

3. **Key count (around line 83):** Update 'all 18 keys present' → 'all 19 keys present' (or 20 if Relevance is concurrent).

4. **Parsimony scoring guidance:** Include a short description of Parsimony in the prompt body so the LLM knows what to score against. Pull from P1 rules summary.

## Files touched

- tools/prose-eval/src/prose_eval/prompts/eval-rubric-score.md (only)

## Depends on

pp-v2q7 (P1: content), pp-jw8w (P2: schema)
