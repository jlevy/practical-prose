---
type: is
id: is-01ktqhdssx963r6mzpn0z9yak8
title: "Optional: in-package 'pprose snapshot' (eval.md -> PNG) without heavy deps"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-06-10T01:12:54.332Z
updated_at: 2026-06-10T01:12:54.332Z
---
Deferred: we chose a dev-workflow (Chrome + pdftoppm + magick, documented in eval-screenshots.runbook.md) over an in-package command to avoid a heavy headless-browser dependency. If we later want a first-class 'pprose snapshot', revisit a light approach (shell out to system Chrome, or optional extra). Related: pp-5zgc (Playwright visual-regression).
