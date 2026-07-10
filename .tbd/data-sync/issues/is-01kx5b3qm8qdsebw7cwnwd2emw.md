---
type: is
id: is-01kx5b3qm8qdsebw7cwnwd2emw
title: Report failed local tbd accurately when npx is unavailable
kind: bug
status: closed
priority: 3
version: 3
labels: []
dependencies: []
parent_id: is-01kx599fjed9w5y77xswj8ab2t
created_at: 2026-07-10T06:23:18.663Z
updated_at: 2026-07-10T06:24:30.168Z
closed_at: 2026-07-10T06:24:30.167Z
close_reason: Both session hooks now distinguish a failed local tbd from a missing CLI when npx is unavailable; manual branch simulations cover failed-local, missing-local, and successful-fallback paths, and both scripts pass bash -n.
---
Address PR #31 thread PRRT_kwDOSbwK686Pyj7s in both generated session hooks: distinguish a broken local tbd from a missing CLI when the pinned npx fallback cannot run.
