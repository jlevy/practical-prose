---
type: is
id: is-01kskbrg0px9w2baeeeryg896a
title: "[chopdiff v0.4.x] Add Paragraph.code_language + code_line_count"
kind: task
status: open
priority: 1
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
dependencies:
  - type: blocks
    target: is-01kskbs2ymzshjbfvnsg1wp8n9
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:01:13.748Z
updated_at: 2026-05-27T00:02:13.222Z
---
Tracked here; work in jlevy/chopdiff. Add two cached properties on Paragraph: code_language: str | None (fence info string for fenced code, None for indented code or no info) and code_line_count: int | None (number of lines in the code body, None if not a code block). Enables pprose metrics: fenced_code_counts_by_language, total_code_line_count.
