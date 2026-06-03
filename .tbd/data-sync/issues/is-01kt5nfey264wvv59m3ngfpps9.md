---
type: is
id: is-01kt5nfey264wvv59m3ngfpps9
title: Add pprose --version and a CHANGELOG
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/release-readiness-2026-06.md
labels:
  - release
  - docs
dependencies: []
parent_id: is-01kt5nebv6vqtrx17dfy0hy04m
created_at: 2026-06-03T02:37:23.251Z
updated_at: 2026-06-03T02:49:14.414Z
closed_at: 2026-06-03T02:49:14.412Z
close_reason: null
---
Risk #13. No 'pprose --version' command exists (it errors as unknown), and there is no CHANGELOG, for a tool that bakes version pins into generated artifacts and tells users to pin pprose@<version>. Add a top-level --version flag in cli.py (report the installed pprose version) and a CHANGELOG.md stub. RAPID FIX (version flag is small; mind the dev-version display).
