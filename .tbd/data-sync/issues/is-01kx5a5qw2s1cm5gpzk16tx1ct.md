---
type: is
id: is-01kx5a5qw2s1cm5gpzk16tx1ct
title: Report batch render failures as partial successes
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01kx599fjed9w5y77xswj8ab2t
created_at: 2026-07-10T06:06:55.873Z
updated_at: 2026-07-10T06:10:37.604Z
closed_at: 2026-07-10T06:10:37.603Z
close_reason: Batch render failures now preserve the scored report, identify partial scoring success, and contribute to the nonzero batch result.
---
Address unresolved PR #31 thread PRRT_kwDOSbwK686PyXJV: preserve scoring success and identify the written eval report when post-score rendering fails.
