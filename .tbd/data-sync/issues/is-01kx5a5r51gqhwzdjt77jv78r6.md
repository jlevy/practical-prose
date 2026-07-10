---
type: is
id: is-01kx5a5r51gqhwzdjt77jv78r6
title: Skip render variant validation for score dry runs
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01kx599fjed9w5y77xswj8ab2t
created_at: 2026-07-10T06:06:56.160Z
updated_at: 2026-07-10T06:10:37.807Z
closed_at: 2026-07-10T06:10:37.806Z
close_reason: Dry-run now returns before render-variant validation while invalid variants still fail before any paid scorer call.
---
Address unresolved PR #31 thread PRRT_kwDOSbwK686PyXJT: a score dry run performs no render, so render-only option validation must not block prompt inspection.
