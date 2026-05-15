---
type: is
id: is-01krfgecww7vy81sw8v6s9sfm5
title: Delete scripts/ now that tools/prose-eval/ is the canonical location
kind: chore
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md
labels: []
dependencies:
  - type: blocks
    target: is-01krfged1j49wg72vycsarvw28
parent_id: is-01krfgdgghp4x3rtpyk0kd4r1n
created_at: 2026-05-13T01:50:26.202Z
updated_at: 2026-05-13T02:08:01.491Z
closed_at: 2026-05-13T02:08:01.490Z
close_reason: scripts/ deleted. tools/prose-eval/ is now the sole location for eval tooling.
---
Round-1 scorer has finished (11/12 OK). The legacy scripts/*.py files in the repo root are duplicates of what now lives in tools/prose-eval/src/prose_eval/. Verify no running process references them, then 'rm -rf scripts/' (or leave a one-line scripts/README.md pointer to tools/prose-eval/).
