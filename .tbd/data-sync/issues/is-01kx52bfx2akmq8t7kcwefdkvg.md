---
type: is
id: is-01kx52bfx2akmq8t7kcwefdkvg
title: Remove undocumented bracket-tag detail length cap
kind: bug
status: closed
priority: 3
version: 3
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:50:15.713Z
updated_at: 2026-07-10T04:48:04.944Z
closed_at: 2026-07-10T04:48:04.943Z
close_reason: The undocumented 200-character tag-detail cap was removed and boundary coverage added.
---
PR #31, metrics.py: new regex silently accepts 200 colon-detail characters and rejects 201 although docs specify no limit; magic cap is unexplained. Remove the line-bounded cap and test a long observable tag.
