---
type: is
id: is-01kt5ng1rdp5k3st5tvcg7189t
title: "Integration tests: compute-derived --in-place idempotency + compare draft rejection"
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
created_at: 2026-06-03T02:37:42.539Z
updated_at: 2026-06-03T02:37:42.539Z
---
Automation candidates. (a) compute-derived --in-place: run twice on a fixture, assert byte-stable second run and body matches frontmatter. (b) compare draft/misalignment rejection: all committed fixtures are status=complete+aligned, so the default-reject UX is only tested via temp files; commit a draft/misaligned fixture and assert exit 1 + message, then --allow-draft --allow-misalignment passes with warning blocks.
