---
type: is
id: is-01kx3zj3ymn0122yadkwvhy8gd
title: Re-lock uv.lock from a clean env; add lockfile staleness check to CI
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-07-09T17:42:12.692Z
updated_at: 2026-07-09T19:29:16.279Z
closed_at: 2026-07-09T19:29:16.279Z
close_reason: "Resolved on review branch: [options] block stripped from uv.lock (resolved versions unchanged, verified byte-identical installs + tests), CI gates on 'env -u UV_FROZEN uv lock --check' plus an [options]-reappearance grep, and SUPPLY-CHAIN-SECURITY.md documents the environment-neutral-lock invariant and the 'uv lock --no-config' re-lock guidance."
---
The committed uv.lock [options] block embeds the maintainer's personal global uv settings (exclude-newer-span P7D, per-package 2100-dated sentinels). Any clean environment treats the lock as stale, so plain 'uv sync' silently re-resolved on every CI run until UV_FROZEN was added on the 2026-07-09 review branch. Follow-up: re-lock from a clean environment, or commit a repo-scoped uv.toml carrying the intended exclude-newer policy so all environments resolve identically; then a 'uv lock --check' CI step becomes possible.
