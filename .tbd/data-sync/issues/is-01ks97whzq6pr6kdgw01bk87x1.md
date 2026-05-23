---
type: is
id: is-01ks97whzq6pr6kdgw01bk87x1
title: Add relevance field to GroundingScores/GroundingReasons in eval_report.py
kind: chore
status: open
priority: 2
version: 3
labels:
  - rubric-rollout
  - relevance
  - code
dependencies:
  - type: blocks
    target: is-01ks97wyqfkqcx7w5mzkwhs893
  - type: blocks
    target: is-01ks97xacz7gyeyycb8ggn697e
parent_id: is-01ks97vjxrmnzmxk6ke3hmt505
created_at: 2026-05-23T01:41:08.215Z
updated_at: 2026-05-23T01:42:25.357Z
---
Pydantic models in tools/prose-eval/src/prose_eval/eval_report.py — add the new `relevance` field to the Grounding models. Note: this is a different group than the Parsimony epic (which touches JudgmentScores).

## Changes

1. **`GroundingScores`:** Add `relevance: Score` field. Position between `factuality` and the end of the class to match section order.

2. **`GroundingReasons`:** Add `relevance: str | None = None`.

3. **`stub_qual()`:** Add `relevance=0` to the `GroundingScores(...)` constructor call.

## Files touched

- tools/prose-eval/src/prose_eval/eval_report.py (only)

## Depends on

pp-xt1p (R1: content), pp-<R2-id> (R2: schema)
