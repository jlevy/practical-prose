---
type: is
id: is-01kt5neygdcg4sh05nah2x9d34
title: "Fix Gemini key-name mismatch: accept GEMINI_API_KEY"
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/release-readiness-2026-06.md
labels:
  - release
  - bug
dependencies: []
parent_id: is-01kt5nebv6vqtrx17dfy0hy04m
created_at: 2026-06-03T02:37:06.443Z
updated_at: 2026-06-03T02:49:14.713Z
closed_at: 2026-06-03T02:49:14.712Z
close_reason: null
---
Risk #3. eval_score.py main() hard-requires GOOGLE_API_KEY for provider 'google', but environments (incl. this repo's ~/.env.local) commonly set GEMINI_API_KEY, so 'pprose score --model gemini' is blocked despite a valid key. Fix: accept GEMINI_API_KEY as an alias for the google provider (or, at minimum, name it in the error message). Add a unit test locking the accepted env-var names per provider.
