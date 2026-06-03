---
type: is
id: is-01kt5nffhr65vxdgmmt59cwj7y
title: Document metrics to eval-report lint-signal asymmetry
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
created_at: 2026-06-03T02:37:23.896Z
updated_at: 2026-06-03T02:49:13.762Z
closed_at: 2026-06-03T02:49:13.761Z
close_reason: null
---
Risk #12. 'pprose metrics' emits richer lint signals (replacement_history, pedantic_marker, generic_heading, em-dash density, bracket-tag examples) that are intentionally dropped at the eval-report QuantMetrics boundary, so report/compare never surface them. Add a one-line note at the command boundary / in the metrics doc so users are not surprised. RAPID FIX.
