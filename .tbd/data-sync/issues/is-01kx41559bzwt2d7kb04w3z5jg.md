---
type: is
id: is-01kx41559bzwt2d7kb04w3z5jg
title: pprose install clobbers a symlinked AGENTS.md
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-07-09T18:10:05.225Z
updated_at: 2026-07-09T18:10:05.225Z
---
Repro: in a repo where AGENTS.md is a symlink (e.g. AGENTS.md -> agents-overview.md, the shared-entry-file pattern finterm uses for CLAUDE.md/AGENTS.md), `pprose install --auto --project` replaces the symlink with a regular file containing only the pprose block. The symlink target is orphaned and the repo's entry files silently fork. The installer should write the block through the symlink (resolve and edit the target), or refuse with a clear message. Found 2026-07-09 while installing pprose@0.1.1 into finterm-main; worked around with --surfaces=portable,claude plus a hand edit of the target file.
