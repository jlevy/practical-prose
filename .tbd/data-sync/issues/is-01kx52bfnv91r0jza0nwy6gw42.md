---
type: is
id: is-01kx52bfnv91r0jza0nwy6gw42
title: Validate render variants before paid scoring
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:50:15.482Z
updated_at: 2026-07-10T04:48:04.780Z
closed_at: 2026-07-10T04:48:04.779Z
close_reason: Render variants are validated before environment loading or any paid scoring call, with a regression test.
---
PR #31, eval_score.py: --render-variant is not validated until after model calls, so a typo can incur paid scoring before the requested render fails. Preflight variants before API-key/model execution, return a usage error, and add CLI regression coverage.
