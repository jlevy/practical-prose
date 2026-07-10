---
type: is
id: is-01kx5a5qhyyj7rh0156yjc5h01
title: Move batch rendering outside async scoring slots
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01kx599fjed9w5y77xswj8ab2t
created_at: 2026-07-10T06:06:55.549Z
updated_at: 2026-07-10T06:10:37.400Z
closed_at: 2026-07-10T06:10:37.399Z
close_reason: Moved post-score rendering outside all async scoring tasks and added a regression proving all scores finish before rendering begins.
---
Address unresolved PR #31 thread PRRT_kwDOSbwK686PyQch: do not run synchronous HTML rendering while an async scoring task still owns the concurrency semaphore or event loop.
