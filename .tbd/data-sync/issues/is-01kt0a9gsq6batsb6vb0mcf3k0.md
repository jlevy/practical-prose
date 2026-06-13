---
type: is
id: is-01kt0a9gsq6batsb6vb0mcf3k0
title: "Print CSS: @page rules, page-size flag, break-inside boundaries"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/done/plan-2026-05-29-static-html-eval-report.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0a9x5m907a3gz0sxtbhft1
parent_id: is-01kt0a89n7vxq8pc32h8htb3kx
created_at: 2026-06-01T00:45:42.070Z
updated_at: 2026-06-13T18:38:35.686Z
closed_at: 2026-06-01T01:17:43.614Z
close_reason: Implemented in Phase 1; tests pass, lint clean, end-to-end smoke test produces 48KB self-contained HTML
---
Add print CSS to styles/base.css (or styles/print.css if cleaner): @media print { @page { size: letter; margin: 0.6in; } } with --page-size letter|a4 generating the right @page rule. Add break-inside: avoid on the .bi-card, on each per-dim detail block, and on each metrics block. Hide on-screen-only chrome (e.g., any nav) under @media print. Reference: /Users/levy/wrk/kmd/textpress/src/textpress/docs/templates/textpress_webpage.html.jinja for the @page pattern. Verification is manual: open in browser, hit Cmd-P, check that page 1 holds the whole card, detail blocks don't split awkwardly, and 'Save as PDF' produces a clean N-page document at both Letter and A4.
