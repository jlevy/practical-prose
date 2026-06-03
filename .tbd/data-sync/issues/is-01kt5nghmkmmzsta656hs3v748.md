---
type: is
id: is-01kt5nghmkmmzsta656hs3v748
title: Visual-regression smoke (Playwright) for the rendered eval page
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/release-readiness-2026-06.md
labels:
  - release
  - test
  - render
dependencies: []
parent_id: is-01kt5nebv6vqtrx17dfy0hy04m
created_at: 2026-06-03T02:37:58.803Z
updated_at: 2026-06-03T02:37:58.803Z
---
Risk #8. The entire visual contract (group icons, score bars, hover tip-panels, dark mode, print pagination, responsive 72rem reflow) rests on manual review; no test renders pixels. Add a Playwright screenshot/visual-regression smoke covering light + dark + print, including a sentinel (NA/ERR) fixture, to anchor the visual contract. Complements the manual checklist in docs/project/e2e-testing.runbook.md.
