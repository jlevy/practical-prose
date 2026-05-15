---
type: is
id: is-01krfgdgghp4x3rtpyk0kd4r1n
title: "Spec: Eval scoring re-architecture (package + SDK + batch concurrency)"
kind: epic
status: closed
priority: 2
version: 16
spec_path: docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md
labels: []
dependencies: []
child_order_hints:
  - is-01krfgecww7vy81sw8v6s9sfm5
  - is-01krfged1j49wg72vycsarvw28
  - is-01krfged5mfsa2ne692nr1c218
  - is-01krfgeda76zvvdk9zbftcm2vf
  - is-01krfgewnekztnde568r3p6hcn
  - is-01krfgewsntaqw05e29s24shky
  - is-01krfgewxxdgq2t74njv50vn7f
  - is-01krfgex27av7wzazhyn8hkj6v
  - is-01krfgex6jj10h1qtwsx8x16ft
  - is-01krfgexb0348x9s50y4y51pev
  - is-01krfgf9p9px0c3c6qz8t4vc36
  - is-01krfgkdgxz45gt3bb24856s81
  - is-01krfgkk1zc1jcqw28jwf1x0nw
  - is-01krfgkr6rtn0sj8e5r82ct367
created_at: 2026-05-13T01:49:57.130Z
updated_at: 2026-05-13T02:28:22.971Z
closed_at: 2026-05-13T02:28:22.970Z
close_reason: "All 14 child beads closed. Phase 0 (package scaffold), Phase 1 (Anthropic SDK + prompt caching + dotenv), and Phase 2 (gather_limited + score_batch + --batch flag) all delivered. Verified: 155/155 tests pass, make lint clean, end-to-end 12-doc batch in 1m33s (vs ~4h serial in round 1, ~160x speedup), cache mechanism confirmed via read_input_tokens hits, 8/12 docs in self-eval-v0.2 completed cleanly with the rest preserving raw responses for F3a recovery. Runbooks + root README updated for the new entry points and batch flow. Two follow-on candidates surfaced (not in this spec): (a) model-self-correction retry to eliminate F3 residue, (b) cache pre-warming to lift cache-hit rate above the observed 2/8 on the first concurrent wave."
---
Tracks the full work in docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md. Phase 0 (scaffold tools/prose-eval/) is implemented; this epic groups the remaining Phase 0 cleanup, Phase 1 (Anthropic SDK migration with prompt caching), and Phase 2 (bounded async batch concurrency). See spec for goals, non-goals, and design rationale.
