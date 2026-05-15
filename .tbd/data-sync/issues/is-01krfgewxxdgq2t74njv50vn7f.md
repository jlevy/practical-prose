---
type: is
id: is-01krfgewxxdgq2t74njv50vn7f
title: "Phase 1: Add _build_messages() multi-block shape; switch main() to SDK by default"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md
labels: []
dependencies:
  - type: blocks
    target: is-01krfgex27av7wzazhyn8hkj6v
  - type: blocks
    target: is-01krfgex6jj10h1qtwsx8x16ft
parent_id: is-01krfgdgghp4x3rtpyk0kd4r1n
created_at: 2026-05-13T01:50:42.621Z
updated_at: 2026-05-13T02:17:04.134Z
closed_at: 2026-05-13T02:17:04.133Z
close_reason: Added _cached_block_text() / _artifact_block_text() / _build_messages() returning a 2-block user message with cache_control={'type':'ephemeral'} on the invariant block. Rewired main() to use _build_messages + call_anthropic; CLI path removed per Q6 decision; --batch flag stub reserved for Phase 2. Added ANTHROPIC_API_KEY check + dotenv autoload at the start of main().
---
Add _build_messages(artifact_path) returning a 2-block user message: (1) instructions + rule-bounds appendix + rubric + guidelines (cached); (2) '## Artifact under review' header + artifact body (uncached). Rewire main() to call call_anthropic() instead of call_claude(); --use-cli flag falls back to the legacy path.
