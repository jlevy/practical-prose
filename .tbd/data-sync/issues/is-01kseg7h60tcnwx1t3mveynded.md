---
type: is
id: is-01kseg7h60tcnwx1t3mveynded
title: "Design-system: audit dimensionsByGroup export usage"
kind: chore
status: open
priority: 4
version: 1
labels:
  - design-system
  - cleanup
dependencies: []
created_at: 2026-05-25T02:43:08.607Z
updated_at: 2026-05-25T02:43:08.607Z
---
tools/design-system/lib/design-system.js exports `dimensionsByGroup` (a precomputed lookup) but no caller has been wired to use it yet.  Either:
- Document the intended consumer (e.g. future renderer code), or
- Remove the export until a real caller appears (YAGNI).
