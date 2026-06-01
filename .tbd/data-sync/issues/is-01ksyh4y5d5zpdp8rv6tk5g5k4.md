---
type: is
id: is-01ksyh4y5d5zpdp8rv6tk5g5k4
title: Dogfood pprose install on this repo; slim /AGENTS.md
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-30-pprose-install-scopes-and-surfaces.md
labels: []
dependencies:
  - type: blocks
    target: is-01ksyh4ympybqjqjnfb0rz3bxs
parent_id: is-01ksyh41ve1a731ww85kxnh54k
created_at: 2026-05-31T08:07:03.084Z
updated_at: 2026-05-31T08:16:47.400Z
closed_at: 2026-05-31T08:16:47.394Z
close_reason: "ran pprose install --project on this repo: wrote 5 .agents/skills/pprose-* dirs and added the pprose block to /AGENTS.md (reordered manually so pprose block precedes the tbd block). Idempotent re-run shows all unchanged. AGENTS.md slimmed to 44 lines: header + 2 pointers + pprose block + tbd block."
---
Run pprose install --project on the practical-prose repo to write the pprose marker block into /AGENTS.md. Then slim the hand-authored content surrounding the block: replace Authoring Principles section with one-line pointer at 'pprose guidelines practical-prose-authoring-principles'; replace Workflows + Tooling + Visual Design sections with one-line pointer at 'docs/project/agents-internal-guide.md'. End state: ~15 lines: title + brief desc + 2 pointers + pprose block + tbd block.
