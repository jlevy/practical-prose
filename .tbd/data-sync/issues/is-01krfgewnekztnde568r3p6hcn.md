---
type: is
id: is-01krfgewnekztnde568r3p6hcn
title: Resolve Phase 1/2 open questions (5 decisions)
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md
labels: []
dependencies:
  - type: blocks
    target: is-01krfgewsntaqw05e29s24shky
parent_id: is-01krfgdgghp4x3rtpyk0kd4r1n
created_at: 2026-05-13T01:50:42.348Z
updated_at: 2026-05-13T02:07:39.861Z
closed_at: 2026-05-13T02:07:39.858Z
close_reason: "Decisions captured in plan spec §Open Questions: drop CLI path entirely (SDK-only), use aiolimiter, --batch as flag, concurrent=8 rps=4, timeout=10min. Plus load .env/.env.local via python-dotenv per leximetry pattern."
---
Per docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md §Open Questions, resolve before starting Phase 1: (6) Drop the 'claude' CLI path entirely or keep '--use-cli' as fallback? (7) Use aiolimiter dep or inline a leaky-bucket? (8) Should 'batch' be a subcommand or a flag? (9) Default --max-concurrent and --max-rps values (proposed 4 and 2). (10) Per-call timeout — 5 min, 10 min, or SDK default? Decisions inform Phase 1 implementation; record resolutions back in the spec.
