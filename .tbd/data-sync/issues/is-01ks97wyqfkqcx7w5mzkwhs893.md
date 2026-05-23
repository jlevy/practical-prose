---
type: is
id: is-01ks97wyqfkqcx7w5mzkwhs893
title: Update Python tests for relevance field (test_eval_report.py, test_eval_score.py, test_eval_compare.py)
kind: chore
status: closed
priority: 2
version: 3
labels:
  - rubric-rollout
  - relevance
  - tests
dependencies:
  - type: blocks
    target: is-01ks97yme61jy7g3wwczpt9fy0
parent_id: is-01ks97vjxrmnzmxk6ke3hmt505
created_at: 2026-05-23T01:41:21.263Z
updated_at: 2026-05-23T02:12:40.184Z
closed_at: 2026-05-23T02:12:40.184Z
close_reason: Implemented as part of the combined 20-dim-v1 rollout (commit on claude/vibrant-goldberg-828VB)
---
Three test files have hardcoded dimension dicts for GroundingScores; update to include the new `relevance` field.

## Changes

### test_eval_report.py

- `_minimal_qual()`: add `'relevance': 5` to the `'grounding'` dict.
- `test_validate_complete_accepts_filled_report`: add `'relevance': 'clean'` to qual_reasons.grounding.
- Update dim-count comments and `sub5_dims` lists.

### test_eval_score.py

All `GroundingScores(verifiability=5, factuality=5)` constructor calls: add `relevance=5`.

### test_eval_compare.py

- `_make_report()` and `_make_report_with_scope()`: add `'relevance'` to grounding dict.
- `test_collect_density_concerns_returns_only_flagged`: same.
- Update literal `'18-dim-v1'` strings to `'19-dim-v1'`.

## Files touched

- tools/prose-eval/tests/test_eval_report.py
- tools/prose-eval/tests/test_eval_score.py
- tools/prose-eval/tests/test_eval_compare.py

## Depends on

pp-6lh8 (R3: Pydantic models), pp-(R4-id) (R4: prompt)
