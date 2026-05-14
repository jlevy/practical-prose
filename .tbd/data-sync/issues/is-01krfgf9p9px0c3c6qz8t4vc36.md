---
type: is
id: is-01krfgf9p9px0c3c6qz8t4vc36
title: "Phase 2: Add gather_limited(coros, *, max_concurrent, max_rps) helper"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md
labels: []
dependencies:
  - type: blocks
    target: is-01krfgkdgxz45gt3bb24856s81
parent_id: is-01krfgdgghp4x3rtpyk0kd4r1n
created_at: 2026-05-13T01:50:55.688Z
updated_at: 2026-05-13T02:21:57.114Z
closed_at: 2026-05-13T02:21:57.108Z
close_reason: Added src/prose_eval/_concurrency.py with gather_limited(*coros, max_concurrent=8, max_rps=4.0, return_exceptions=False) — asyncio.Semaphore + aiolimiter.AsyncLimiter wrapping each awaitable, patterned on leximetry's aio_limited.py. Smoke-tested with 10-coro fan-out and exception passing. aiolimiter>=1.2 added to pyproject deps.
---
Add src/prose_eval/_concurrency.py with gather_limited() patterned on /Users/levy/wrk/aisw/trading/attic/leximetry/src/leximetry/utils/aio_limited.py: asyncio.Semaphore + aiolimiter.AsyncLimiter wrapping each coroutine via nested async with. ~30 LOC. Or inline if aiolimiter dep was rejected in Q7 (~10 more LOC to inline the leaky bucket).
