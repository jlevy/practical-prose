---
type: is
id: is-01kx3zj3ymn0122yadkwvhy8gd
title: Re-lock uv.lock from a clean env; add lockfile staleness check to CI
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-07-09T17:42:12.692Z
updated_at: 2026-07-09T17:42:12.692Z
---
The committed uv.lock [options] block embeds the maintainer's personal global uv settings (exclude-newer-span P7D, per-package 2100-dated sentinels). Any clean environment treats the lock as stale, so plain 'uv sync' silently re-resolved on every CI run until UV_FROZEN was added on the 2026-07-09 review branch. Follow-up: re-lock from a clean environment, or commit a repo-scoped uv.toml carrying the intended exclude-newer policy so all environments resolve identically; then a 'uv lock --check' CI step becomes possible.
