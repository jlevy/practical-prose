---
type: is
id: is-01ksyh4wwkae62epfxjv1c5z3z
title: "Restructure docs: extract authoring-principles, move development.md and AGENTS.md content"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-05-30-pprose-install-scopes-and-surfaces.md
labels: []
dependencies:
  - type: blocks
    target: is-01ksyh4x4x091pzmepdrnhf3r5
  - type: blocks
    target: is-01ksyh4xvmnt9q1xzqxzjm1yh9
parent_id: is-01ksyh41ve1a731ww85kxnh54k
created_at: 2026-05-31T08:07:01.773Z
updated_at: 2026-05-31T08:08:55.311Z
closed_at: 2026-05-31T08:08:55.305Z
close_reason: extracted /docs/practical-prose-authoring-principles.md; moved /docs/development.md → /docs/project/development.md; created /docs/project/agents-internal-guide.md with workflows table + tooling + visual design sections
---
(a) Extract 8 authoring principles from /AGENTS.md into NEW /docs/practical-prose-authoring-principles.md (full content, no abbreviation). (b) Move /docs/development.md to /docs/project/development.md so sync_resources non-recursive glob stops bundling it; update any internal links. (c) Move workflows table + Tooling + Visual Design sections from /AGENTS.md into NEW /docs/project/agents-internal-guide.md. After this bead /AGENTS.md is just title + brief desc + (will reference the moved docs).
