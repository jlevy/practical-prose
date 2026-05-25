---
type: is
id: is-01ksey55erarj3za2eqdcn9bwq
title: Update hand-ordered Python code in pprose package
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01ksey5yp32kt19vj1m19vjtye
parent_id: is-01ksey4hc3txw0a3f13445ahrm
created_at: 2026-05-25T06:46:31.126Z
updated_at: 2026-05-25T06:55:31.193Z
closed_at: 2026-05-25T06:55:31.189Z
close_reason: Reordered Pydantic class defs (GroundingScores/Reasons swapped with ReasoningScores/Reasons), QualScores/QualReasons field order, RubricRollup field order, group_means dict in summary builder, and _SCORES_CLS/_REASONS_CLS dicts in eval_score.py. Also updated docstring in eval_compare.py.
---
These files have group order declared by hand (not iterated from rs.GROUPS), so they must be reordered manually. Pydantic field order affects serialized output, so getting this right is required for fixtures to match.

- tools/pprose/src/pprose/eval_report.py:157-194 — class definition order: PurposeScores, ExpressionScores, FormScores, GroundingScores, ReasoningScores, JudgmentScores (and same for *Reasons classes at 217-258)
- tools/pprose/src/pprose/eval_report.py:203-208 — QualScores field order
- tools/pprose/src/pprose/eval_report.py:263-268 — QualReasons field order
- tools/pprose/src/pprose/eval_report.py:683-688 — group_means dict in summary builder
- tools/pprose/src/pprose/eval_score.py:188-201 — two class-mapping dicts (SCORES_BY_GROUP and REASONS_BY_GROUP, or whatever they're named)
- tools/pprose/src/pprose/eval_compare.py:9 — docstring comment listing group order
