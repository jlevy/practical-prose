---
type: is
id: is-01krfgkdgxz45gt3bb24856s81
title: "Phase 2: Add score_batch() and 'batch' subcommand to eval_score.py"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md
labels: []
dependencies:
  - type: blocks
    target: is-01krfgkk1zc1jcqw28jwf1x0nw
parent_id: is-01krfgdgghp4x3rtpyk0kd4r1n
created_at: 2026-05-13T01:53:10.682Z
updated_at: 2026-05-13T02:24:01.585Z
closed_at: 2026-05-13T02:24:01.581Z
close_reason: Added call_anthropic_async() using AsyncAnthropic. Factored _score_one body into _prepare_score() + _apply_score() helpers shared by sync and async paths. Added _score_one_async() and score_batch(yaml_paths, *, model, evaluator, allow_misaligned, argv, max_concurrent=8, max_rps=4.0) fanning N coroutines through gather_limited with return_exceptions=True. Wired --batch / --max-concurrent / --max-rps argparse flags; main() routes to score_batch when --batch+len>1, else falls back to sequential _score_one. Per-doc OK/FAIL printed in batch mode. 155/155 tests pass + lint clean.
---
Add score_batch(yaml_paths, *, model, max_concurrent, max_rps) that schedules N single-doc scorings through gather_limited(). Add 'batch' subcommand to argparse (per Q8 decision) with --max-concurrent (default 4 per Q9) and --max-rps (default 2 per Q9). Per-call timeout from Q10.
