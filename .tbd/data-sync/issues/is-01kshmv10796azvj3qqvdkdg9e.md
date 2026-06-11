---
type: is
id: is-01kshmv10796azvj3qqvdkdg9e
title: "[chopdiff tracking] Expose Code fence info string (language) on BlockDoc"
kind: task
status: closed
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:01:24.997Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-05-27T00:00:54.342Z
close_reason: "Superseded by spec rewrite 2026-05-26 (v3). New architecture: chopdiff v0.4.x parses each block once and exposes typed accessors (heading_level, code_language, list_info, table_info, inlines, section_tree). Pprose becomes a thin serializer with no marko import and no per-block re-parse. Replaced by a fresh bead set."
---
Tracked here for visibility; the work itself happens in jlevy/chopdiff. Expose language: str | None (the fenced-code info string) on Code blocks. Enables pprose metric: fenced_code_counts_by_language. Smallest of the three follow-ons; one extra string field. When this lands upstream, bump the chopdiff pin and fill in the empty-dict-defaulted field.
