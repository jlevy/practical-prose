---
type: is
id: is-01kt5ng1ggpa2h99wssc4w4gf1
title: "Golden tests: metrics CLI argv path + --banned-words-file"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/release-readiness-2026-06.md
labels:
  - release
  - test
dependencies: []
parent_id: is-01kt5nebv6vqtrx17dfy0hy04m
created_at: 2026-06-03T02:37:42.287Z
updated_at: 2026-06-03T02:37:42.287Z
---
Automation candidates. Unit tests call the formatter functions directly but never drive metrics.main(argv) through --format yaml|json (assert single file still emits a one-element list), the multi-file summary-table branch, or nonexistent-file (stderr + exit 1). Also no CLI-level test for --banned-words-file (file with # comments + blank lines replacing the default list). Add golden/CLI tests. Bonus: lock the flag-only lint signals (replacement_history, pedantic_marker, generic_heading, em-dash density) and assert their intended absence from the report QuantMetrics surface (ties to #12).
