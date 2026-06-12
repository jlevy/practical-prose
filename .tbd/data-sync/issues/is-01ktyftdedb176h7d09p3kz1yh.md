---
type: is
id: is-01ktyftdedb176h7d09p3kz1yh
title: pprose compare scope-class warning renders spaced em dashes
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-06-12T17:59:31.532Z
updated_at: 2026-06-12T17:59:31.532Z
---
Generated comparison Markdown (e.g. evals/baselines/comparison-all.md) opens with 'Scope-class warning: comparing across scope classes — brief: ...' using spaced em dashes, which F2.7 bans; the renderer should use a colon or unspaced em dash. Also note: the tbd AGENTS.md integration block (format=f04) contains a spaced em dash ('user's behalf — translate'), generated upstream by tbd and worth an upstream template fix.
