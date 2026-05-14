---
type: is
id: is-01krfgewsntaqw05e29s24shky
title: "Phase 1: Add anthropic SDK dep + call_anthropic() with cache_control"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md
labels: []
dependencies:
  - type: blocks
    target: is-01krfgewxxdgq2t74njv50vn7f
parent_id: is-01krfgdgghp4x3rtpyk0kd4r1n
created_at: 2026-05-13T01:50:42.484Z
updated_at: 2026-05-13T02:17:04.016Z
closed_at: 2026-05-13T02:17:04.012Z
close_reason: Added anthropic>=0.39 and python-dotenv>=1.0 deps. Added call_anthropic() using client.messages.create with timeout=600s. Added _load_env_files() (walks cwd + $HOME for .env / .env.local). Added _resolve_model() for sonnet/opus/haiku aliases plus DEFAULT_MODEL=claude-sonnet-4-5.
---
In tools/prose-eval/pyproject.toml, add 'anthropic>=0.39' (and 'aiolimiter>=1.2' if decided in Q7) to dependencies. In src/prose_eval/eval_score.py, add call_anthropic(messages, model) using AsyncAnthropic().messages.create() with cache_control={'type': 'ephemeral'} on the invariant rubric+guidelines+instructions block. Keep call_claude() reachable behind --use-cli per Q6 decision.
