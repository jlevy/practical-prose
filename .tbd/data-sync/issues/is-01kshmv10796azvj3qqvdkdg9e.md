---
type: is
id: is-01kshmv10796azvj3qqvdkdg9e
title: "[chopdiff tracking] Expose Code fence info string (language) on BlockDoc"
kind: task
status: open
priority: 3
version: 1
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:01:24.997Z
updated_at: 2026-05-26T08:01:24.997Z
---
Tracked here for visibility; the work itself happens in jlevy/chopdiff. Expose language: str | None (the fenced-code info string) on Code blocks. Enables pprose metric: fenced_code_counts_by_language. Smallest of the three follow-ons; one extra string field. When this lands upstream, bump the chopdiff pin and fill in the empty-dict-defaulted field.
