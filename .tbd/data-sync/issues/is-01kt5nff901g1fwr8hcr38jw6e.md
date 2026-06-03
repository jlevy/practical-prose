---
type: is
id: is-01kt5nff901g1fwr8hcr38jw6e
title: Document dotenv autoload + default-model cost behavior
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/release-readiness-2026-06.md
labels:
  - release
  - docs
dependencies: []
parent_id: is-01kt5nebv6vqtrx17dfy0hy04m
created_at: 2026-06-03T02:37:23.615Z
updated_at: 2026-06-03T02:49:14.107Z
closed_at: 2026-06-03T02:49:14.106Z
close_reason: null
---
Risk #4. .env and .env.local auto-load from the cwd hierarchy AND $HOME with override, so 'pprose score' can make a real, billable call as soon as any reachable dotenv defines the key (env -u VAR does NOT prevent it). The default model is the flagship Opus. Document this prominently in the score help/runbook; consider a cheaper default or a cost confirmation. RAPID FIX (doc part).
