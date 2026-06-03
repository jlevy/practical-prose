---
type: is
id: is-01kt5nezjv7nt82eg1a78nmcr1
title: "detect_kind(): narrow exception handling and emit a clear error"
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/release-readiness-2026-06.md
labels:
  - release
  - bug
dependencies: []
parent_id: is-01kt5nebv6vqtrx17dfy0hy04m
created_at: 2026-06-03T02:37:07.546Z
updated_at: 2026-06-03T02:49:15.093Z
closed_at: 2026-06-03T02:49:15.091Z
close_reason: null
---
Risk #14. render_html detect_kind() swallows ALL exceptions, so an almost-valid .md whose frontmatter happens to parse renders a confusing/empty page instead of erroring clearly. Narrow the except to the expected validation errors and emit an actionable message. Add a test for a malformed-but-close .eval.md.
