---
type: is
id: is-01ks97q4vvxq99hpdhpt396gvy
title: Update Python tests for parsimony field (test_eval_report.py, test_eval_score.py, test_eval_compare.py)
kind: chore
status: open
priority: 2
version: 2
labels:
  - rubric-rollout
  - parsimony
  - tests
dependencies:
  - type: blocks
    target: is-01ks97s25n1s058wk2nfqbtvx3
parent_id: is-01ks97m4tenhgn7w974et1nrnk
created_at: 2026-05-23T01:38:10.939Z
updated_at: 2026-05-23T01:39:39.574Z
---
Three test files have hardcoded dimension dicts for the JudgmentScores model.

## Changes

### test_eval_report.py

- `_minimal_qual()` (~line 90): add `'parsimony': 5` to the `'judgment'` dict.
- `test_validate_complete_accepts_filled_report` (~lines 810-814): add `'parsimony': 'clean'` to qual_reasons.judgment.
- Update comment '17 of 18 dimensions' → '18 of 19' (~line 173).
- `test_score_below_5_with_matching_violation_is_aligned` and `test_canonical_dimension_names_validate` (~lines 619-689): include Parsimony where relevant.

### test_eval_score.py

Around 7 `JudgmentScores(calibration=5, fairness=5, robustness=5)` constructor calls (lines 207, 237, 254, 272, 349, 397, 466). Add `parsimony=5` to each.

### test_eval_compare.py

- `_make_report()` (~line 284) and `_make_report_with_scope()` (~line 411): add `'parsimony'` to judgment dict.
- `test_collect_density_concerns_returns_only_flagged` (~line 494): same.
- Update literal `'18-dim-v1'` strings to `'19-dim-v1'` (or accept as test data for that version).

## Files touched

- tools/prose-eval/tests/test_eval_report.py
- tools/prose-eval/tests/test_eval_score.py
- tools/prose-eval/tests/test_eval_compare.py

## Depends on

pp-or98 (P3: Pydantic models), pp-t8uz (P4: prompt), pp-8wp0 (P5: dim count)
