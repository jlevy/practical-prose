---
type: is
id: is-01ks97pd2e5h9h8rgzyraxja9f
title: Add parsimony field to Pydantic models in eval_report.py
kind: chore
status: closed
priority: 2
version: 4
labels:
  - rubric-rollout
  - parsimony
  - code
dependencies:
  - type: blocks
    target: is-01ks97q4vvxq99hpdhpt396gvy
  - type: blocks
    target: is-01ks97qev6jz44nkqjs438dwen
parent_id: is-01ks97m4tenhgn7w974et1nrnk
created_at: 2026-05-23T01:37:46.574Z
updated_at: 2026-05-23T02:12:36.057Z
closed_at: 2026-05-23T02:12:36.057Z
close_reason: Implemented as part of the combined 20-dim-v1 rollout (commit on claude/vibrant-goldberg-828VB)
---
Pydantic models in tools/prose-eval/src/prose_eval/eval_report.py have explicit per-dimension field names; these must match the YAML schema keys.

## Changes

1. **`JudgmentScores` (around line 187):** Add `parsimony: Score` field. Position before `calibration` to match section order.

2. **`JudgmentReasons` (around line 253):** Add `parsimony: str | None = None`.

3. **`stub_qual()` (around line 728):** Add `parsimony=0` to the `JudgmentScores(...)` constructor call.

(If Relevance epic lands first/concurrently, `relevance` field goes in `GroundingScores` and `GroundingReasons` — separate epic.)

## Files touched

- tools/prose-eval/src/prose_eval/eval_report.py (only)

## Depends on

pp-v2q7 (P1: content), pp-<P2-id> (P2: schema)
