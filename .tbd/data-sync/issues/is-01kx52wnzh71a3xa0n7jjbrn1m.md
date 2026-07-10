---
type: is
id: is-01kx52wnzh71a3xa0n7jjbrn1m
title: Deduplicate Codex session hooks
kind: chore
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:59:38.992Z
updated_at: 2026-07-10T03:59:38.992Z
---
.codex/hooks.json runs both Claude and Codex tbd-session/ensure-gh scripts on SessionStart and PreCompact, potentially priming twice. Confirm intended hook ownership and remove duplicates.
