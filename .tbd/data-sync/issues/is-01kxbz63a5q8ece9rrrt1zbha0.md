---
type: is
id: is-01kxbz63a5q8ece9rrrt1zbha0
title: Harden the release checklist for target-commit and uv isolation
kind: bug
status: closed
priority: 1
version: 4
labels: []
dependencies: []
created_at: 2026-07-12T20:09:34.276Z
updated_at: 2026-07-12T20:29:09.779Z
closed_at: 2026-07-12T20:29:09.779Z
close_reason: Released pprose v0.2.0 from merged commit 2fc2b85 after green PR/main CI; upgraded tbd integration to 0.4.0 and flexdoc to 0.3.0, hardened the release process, and verified the published PyPI/uvx/scratch-install path.
---
tools/pprose/docs/publishing.md does not prove HEAD equals current origin/main, generates the candidate log and diff from HEAD, and creates the GitHub release without an explicit --target. In the current checkout HEAD is divergent from origin/main, so this can describe or tag the wrong candidate. Its local check_release_version.py command also omits UV_NO_CONFIG and UV_LOCKED; under the maintainer global uv config it rewrote uv.lock with an [options] block during this audit. Require a fetched, exact origin/main target (or explicit release commit), run all uv commands with repository isolation, use the real release date in CHANGELOG, and align the release-notes structure with shipped guideline/content changes.

## Notes

Release guide now requires the exact up-to-date main commit, read-only lint gates, isolated locked uv commands, exact commit-based notes, explicit gh release --target, CI watch, and post-publish exact-version uvx smoke. Release notes format now separates shipped guidelines/content. The e2e runbook distinguishes pre-publish, post-publish, and non-shipping quality evidence.
