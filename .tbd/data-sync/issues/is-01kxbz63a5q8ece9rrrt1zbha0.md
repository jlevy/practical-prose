---
type: is
id: is-01kxbz63a5q8ece9rrrt1zbha0
title: Harden the release checklist for target-commit and uv isolation
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-07-12T20:09:34.276Z
updated_at: 2026-07-12T20:09:34.276Z
---
tools/pprose/docs/publishing.md does not prove HEAD equals current origin/main, generates the candidate log and diff from HEAD, and creates the GitHub release without an explicit --target. In the current checkout HEAD is divergent from origin/main, so this can describe or tag the wrong candidate. Its local check_release_version.py command also omits UV_NO_CONFIG and UV_LOCKED; under the maintainer global uv config it rewrote uv.lock with an [options] block during this audit. Require a fetched, exact origin/main target (or explicit release commit), run all uv commands with repository isolation, use the real release date in CHANGELOG, and align the release-notes structure with shipped guideline/content changes.
