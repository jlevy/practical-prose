---
type: is
id: is-01kt5neysah5wcpp1fpb7efvk5
title: "Update root README: remove stale install flags"
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/release-readiness-2026-06.md
labels:
  - release
  - docs
dependencies: []
parent_id: is-01kt5nebv6vqtrx17dfy0hy04m
created_at: 2026-06-03T02:37:06.729Z
updated_at: 2026-06-03T02:49:12.727Z
closed_at: 2026-06-03T02:49:12.720Z
close_reason: null
---
Risk #5. Root README.md (~lines 234-235) still documents removed install flags --claude/--codex/--skip-claude/--skip-codex; the shipped CLI is --project/--global/--surfaces/--pin (tools/pprose/README.md is already correct). Fix the root README to match. RAPID FIX.
