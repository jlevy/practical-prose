---
type: is
id: is-01kxbzc6he9bcjqqsrn3pp92pk
title: Upgrade pprose to flexdoc 0.3.0 for v0.2.0
kind: task
status: closed
priority: 1
version: 4
labels: []
dependencies: []
created_at: 2026-07-12T20:12:54.189Z
updated_at: 2026-07-12T20:29:09.786Z
closed_at: 2026-07-12T20:29:09.786Z
close_reason: Released pprose v0.2.0 from merged commit 2fc2b85 after green PR/main CI; upgraded tbd integration to 0.4.0 and flexdoc to 0.3.0, hardened the release process, and verified the published PyPI/uvx/scratch-install path.
---
Pin first-party flexdoc 0.3.0, review its breaking pre-1.0 API changes, adapt pprose if needed, refresh uv.lock with the repository two-pass procedure, and run the full release gates. User confirmed the standing first-party cool-off exemption.

## Notes

Reviewed flexdoc v0.3.0 tag 74dff0c and PyPI sdist/wheel hashes; downloaded sdist source matches the tag. Pinned 0.3.0, refreshed uv.lock with a one-package first-party override followed by a neutral second lock, and confirmed no unrelated lock changes. Focused tests and the full 338-test suite pass; constrained build and clean-wheel install require flexdoc==0.3.0.
