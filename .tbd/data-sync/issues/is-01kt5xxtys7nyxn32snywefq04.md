---
type: is
id: is-01kt5xxtys7nyxn32snywefq04
title: "[chopdiff] Add NodeKind.footnote_ref (typed inline footnote reference)"
kind: task
status: open
priority: 3
version: 1
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - upstream-chopdiff
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-06-03T05:05:02.936Z
updated_at: 2026-06-03T05:05:02.936Z
---
chopdiff 0.3.1 has no typed inline node kind for footnote references ([^1]); pprose keeps a regex. Optional upstream follow-up: add footnote_ref to NodeKind, surfaced via collect(kinds={footnote_ref}, inline=True). Not blocking. See docs/project/chopdiff-upstream-requests.md (request #4).
