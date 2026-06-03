---
type: is
id: is-01kt5neza3nhpv6ts8875q1nwb
title: Clarify dual-license in package metadata
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
created_at: 2026-06-03T02:37:07.266Z
updated_at: 2026-06-03T02:49:13.429Z
closed_at: 2026-06-03T02:49:13.427Z
close_reason: null
---
Risk #10. pyproject.toml declares license = MIT only, but the wheel bundles substantial CC-BY prose (resources/*.md). Add a note (README/pyproject/long-description) clarifying code is MIT and bundled prose remains CC BY 4.0, consistent with the repo LICENSE. RAPID FIX.
