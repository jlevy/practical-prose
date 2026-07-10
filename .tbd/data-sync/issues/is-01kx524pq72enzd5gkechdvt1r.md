---
type: is
id: is-01kx524pq72enzd5gkechdvt1r
title: Report the configured words-per-page value in metrics output
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:46:33.318Z
updated_at: 2026-07-10T04:48:03.771Z
closed_at: 2026-07-10T04:48:03.771Z
close_reason: Human metrics output now labels pages with the configured words-per-page value, with exact tests.
---
PR #31, tools/pprose/src/pprose/metrics.py:390: the touched label is hardcoded to 275 wpp even when --words-per-page changes the calculation. Thread the configured value into human output and test it.
