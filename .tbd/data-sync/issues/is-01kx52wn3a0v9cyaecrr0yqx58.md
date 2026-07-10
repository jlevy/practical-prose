---
type: is
id: is-01kx52wn3a0v9cyaecrr0yqx58
title: Lock isolated Python build dependencies and publish from a current lock
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:59:38.089Z
updated_at: 2026-07-10T04:48:05.277Z
closed_at: 2026-07-10T04:48:05.276Z
close_reason: Build requirements are exact-pinned and hash-constrained; publish checks the current neutral lock and uses the constrained build.
---
PR #31: UV_FROZEN does not constrain uv build; publish currently resolved hatchling 1.31.0 one day after release, violating the 14-day rule. Add hashed build constraints with reviewed pins, exact-pin build-system requirements, use constraints for sync/build, and make publish verify lock freshness.
