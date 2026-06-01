---
type: is
id: is-01ksxek73f3pyh1vbq59d0g1sr
title: "Refactor pprose install: scopes + surfaces vocabulary"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-05-30-pprose-install-scopes-and-surfaces.md
labels: []
dependencies: []
created_at: 2026-05-30T22:03:10.825Z
updated_at: 2026-05-30T22:03:42.235Z
closed_at: 2026-05-30T22:03:42.234Z
close_reason: implemented on branch pprose-skill-install-improvements
---
Drop --print/--all/--claude/--codex/--skip-*/--no-agents-md flags. Add --project/--global/--surfaces/--no-repo-check. Drop in-file surface= namespace; keep only format=fNN. Add git-repo + $HOME guard rails with pre-write target message. flowmark-style --surfaces=portable,claude,agents-md with 'all' alias. SurfaceSpec parser tracks explicit agents-md so --global --surfaces=agents-md can error while --surfaces=all silently drops it.
