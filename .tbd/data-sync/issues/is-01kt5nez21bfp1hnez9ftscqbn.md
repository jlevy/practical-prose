---
type: is
id: is-01kt5nez21bfp1hnez9ftscqbn
title: Substitute OWNER/PROJECT placeholders in publishing.md + installation.md
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/release-readiness-2026-06.md
labels:
  - release
  - docs
dependencies: []
parent_id: is-01kt5nebv6vqtrx17dfy0hy04m
created_at: 2026-06-03T02:37:07.009Z
updated_at: 2026-06-03T02:49:13.057Z
closed_at: 2026-06-03T02:49:13.056Z
close_reason: null
---
Risk #7. tools/pprose/docs/publishing.md and installation.md are unedited simple-modern-uv template stubs with OWNER/PROJECT placeholders in the PyPI URL and trusted-publisher steps. Substitute jlevy/practical-prose and package name 'pprose' so a first releaser does not misconfigure trusted publishing. RAPID FIX.
