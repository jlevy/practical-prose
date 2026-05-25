---
type: is
id: is-01kseyakm51q8bq3shx3xweptn
title: "P1: Out-of-range rule_number recovery path unreachable; ScoringResponse validates RuleFinding strictly so Pydantic AI rejects hallucinated rule_numbers before _to_scored_result sees them (eval_score.py:318, eval_report.py:367) (PR #12)"
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01kseya645astqx3kpgr6fh4w6
created_at: 2026-05-25T06:49:29.476Z
updated_at: 2026-05-25T06:51:28.554Z
closed_at: 2026-05-25T06:51:28.553Z
close_reason: Introduced RawRuleFinding as permissive scorer output; _to_scored_result now filters bad dimension labels + rule_numbers and re-validates survivors through strict RuleFinding. Added regression tests at the ScoringResponse boundary.
---
