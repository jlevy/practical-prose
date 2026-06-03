---
type: is
id: is-01kt5nghzhr1ktfvx2kr1b2p5s
title: Note SUGGESTED_MODELS version drift + maintenance
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/release-readiness-2026-06.md
labels:
  - release
  - docs
dependencies: []
parent_id: is-01kt5nebv6vqtrx17dfy0hy04m
created_at: 2026-06-03T02:37:59.152Z
updated_at: 2026-06-03T02:37:59.152Z
---
Risk #11. eval_score.py SUGGESTED_MODELS hard-codes specific model IDs (claude-opus-4-7, gpt-5.5, gemini-3.5-flash, ...) that drift as providers ship/retire models; aliases fail only at the live agent boundary. Add a maintenance note tying the table to the pricing data source and a release-checklist re-verify. Likely folds into pp-gq0o (Refresh score targets and model aliases).
