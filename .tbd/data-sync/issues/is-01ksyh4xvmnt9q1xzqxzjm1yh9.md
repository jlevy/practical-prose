---
type: is
id: is-01ksyh4xvmnt9q1xzqxzjm1yh9
title: Slim agents_md_block and regenerate discovery copies
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-05-30-pprose-install-scopes-and-surfaces.md
labels: []
dependencies:
  - type: blocks
    target: is-01ksyh4y5d5zpdp8rv6tk5g5k4
  - type: blocks
    target: is-01ksyh4ympybqjqjnfb0rz3bxs
parent_id: is-01ksyh41ve1a731ww85kxnh54k
created_at: 2026-05-31T08:07:02.771Z
updated_at: 2026-05-31T08:11:04.539Z
closed_at: 2026-05-31T08:11:04.534Z
close_reason: "agents_md_block trimmed: removed per-skill bullet list and 'Installed workflow skills:' label. End shape is ~15 lines: trigger description + 4 list-command pointers + pprose <pin> line. Discovery copies regenerated (no change since bootstrap line stays same)."
---
TDD: update existing agents-md tests for slimmer block. Drop per-skill bullet list from agents_md_block; end shape: header + trigger desc + routing pointers (~10 lines). Regenerate /skills/pprose-*/SKILL.md discovery copies (the bootstrap line referenced from the block changed? actually the SKILL.md bootstrap line is unchanged — but sync may pick up bundled additions, re-run for completeness). Drift test stays green.
