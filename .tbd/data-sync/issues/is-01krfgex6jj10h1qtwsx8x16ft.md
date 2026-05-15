---
type: is
id: is-01krfgex6jj10h1qtwsx8x16ft
title: "Phase 1: Update test_eval_score.py with SDK-client mock"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md
labels: []
dependencies:
  - type: blocks
    target: is-01krfgexb0348x9s50y4y51pev
parent_id: is-01krfgdgghp4x3rtpyk0kd4r1n
created_at: 2026-05-13T01:50:42.897Z
updated_at: 2026-05-13T02:18:33.720Z
closed_at: 2026-05-13T02:18:33.716Z
close_reason: "Added 5 new tests covering SDK code paths: _build_messages cache-control shape, _resolve_model aliases, ReproContext SDK-field persistence, call_anthropic returning text + usage via FakeAnthropic mock, and end-to-end main() round-trip persisting cache_stats. 155/155 tests pass + lint clean."
---
Today test_eval_score.py has no subprocess mock (call_claude wasn't covered). Add a fixture mocking anthropic.AsyncAnthropic so call_anthropic returns a fixed JSON-fence-shaped response. All 24 existing tests should pass with the new mock. Add 1-2 tests asserting cache_control markers are present in the messages.create payload and that cache_stats are persisted.
