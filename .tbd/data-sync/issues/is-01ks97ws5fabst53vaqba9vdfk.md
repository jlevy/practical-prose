---
type: is
id: is-01ks97ws5fabst53vaqba9vdfk
title: Update LLM scoring prompt (eval-rubric-score.md) to include Relevance
kind: chore
status: open
priority: 2
version: 2
labels:
  - rubric-rollout
  - relevance
  - code
dependencies:
  - type: blocks
    target: is-01ks97wyqfkqcx7w5mzkwhs893
parent_id: is-01ks97vjxrmnzmxk6ke3hmt505
created_at: 2026-05-23T01:41:15.567Z
updated_at: 2026-05-23T01:42:25.074Z
---
Update tools/prose-eval/src/prose_eval/prompts/eval-rubric-score.md.

## Changes

1. **Canonical dimension name list:** Insert `Relevance` between `Factuality` and `Inference Discipline`.

2. **JSON example block:** Insert `"relevance": {"score": 0, "reason": "..."}` between the `factuality` and `inference_discipline` entries.

3. **Key count:** Update 'all 18 keys present' → 'all 19 keys present' (or 20 if Parsimony concurrent).

4. **Relevance scoring guidance:** Include short description of Relevance in the prompt body. Pull from R1 rules summary.

## Files touched

- tools/prose-eval/src/prose_eval/prompts/eval-rubric-score.md (only)

## Depends on

pp-xt1p (R1: content), pp-gqa8 (R2: schema)
