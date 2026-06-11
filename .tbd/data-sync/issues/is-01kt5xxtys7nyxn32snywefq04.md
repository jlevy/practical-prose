---
type: is
id: is-01kt5xxtys7nyxn32snywefq04
title: "[chopdiff] Add NodeKind.footnote_ref (typed inline footnote reference)"
kind: task
status: open
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - upstream-chopdiff
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-06-03T05:05:02.936Z
updated_at: 2026-06-11T16:21:46.496Z
---
chopdiff 0.3.1 has no typed inline node kind for footnote references ([^1]); pprose keeps a regex. Optional upstream follow-up: add footnote_ref to NodeKind, surfaced via collect(kinds={footnote_ref}, inline=True). Not blocking. See docs/project/chopdiff-upstream-requests.md (request #4).

## Notes

chopdiff 0.3.1 audit: not exposed in 0.3.1. pprose keeps a footnote-reference regex workaround, so this is an OPTIONAL upstream follow-up, not blocking. Filed as jlevy/chopdiff#21 on 2026-06-10 — see docs/project/chopdiff-upstream-requests.md.
