---
type: is
id: is-01kt5ng10p5hxh0mf04krmj6wy
title: "CI: add uv build + install-from-wheel smoke job"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/release-readiness-2026-06.md
labels:
  - release
  - ci
  - test
dependencies: []
parent_id: is-01kt5nebv6vqtrx17dfy0hy04m
created_at: 2026-06-03T02:37:41.781Z
updated_at: 2026-06-03T06:11:22.730Z
closed_at: 2026-06-03T06:11:22.729Z
close_reason: "Added the wheel-smoke CI job: uv build into a clean out-dir, install into a fresh venv, run the CLI (--help/guidelines --list/about). Green on the run for 1e45e00."
---
Risk #2. The zero-install/publish path has zero automated coverage; a wheel data-file packaging regression (the pyproject include= list is long) would only surface for the first real user. Add a CI job that runs 'uv build', installs the wheel into a fresh venv, and runs 'pprose guidelines --list' + 'pprose about' to catch packaging regressions before a release.
