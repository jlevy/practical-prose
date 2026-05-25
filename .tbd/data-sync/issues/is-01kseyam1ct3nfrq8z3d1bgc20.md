---
type: is
id: is-01kseyam1ct3nfrq8z3d1bgc20
title: "P2: Default metadata.method still 'model (anthropic SDK)' in merge_into_report (eval_score.py:519); should be 'model (pydantic-ai)' or include resolved provider (PR #12)"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01kseya645astqx3kpgr6fh4w6
created_at: 2026-05-25T06:49:29.900Z
updated_at: 2026-05-25T07:06:09.152Z
closed_at: 2026-05-25T07:06:09.145Z
close_reason: merge_into_report now defaults metadata.method to f'model ({provider} via pydantic-ai)' when ReproContext.model is set, else 'model (pydantic-ai)'. Explicit method values still take precedence.
---
