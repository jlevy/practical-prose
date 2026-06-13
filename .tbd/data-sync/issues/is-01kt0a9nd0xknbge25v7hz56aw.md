---
type: is
id: is-01kt0a9nd0xknbge25v7hz56aw
title: Wire 'pprose score --render-html' to compose score + render
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/done/plan-2026-05-29-static-html-eval-report.md
labels: []
dependencies: []
parent_id: is-01kt0a89n7vxq8pc32h8htb3kx
created_at: 2026-06-01T00:45:46.783Z
updated_at: 2026-06-13T18:38:35.686Z
closed_at: 2026-06-01T01:17:43.833Z
close_reason: Implemented in Phase 1; tests pass, lint clean, end-to-end smoke test produces 48KB self-contained HTML
---
Add --render-html (boolean) plus the forwarded render flags (--page-size, --sections, --format, --open, -o/--output) to pprose score's argparse setup. On successful score, after the .eval.md is written to disk, call render_html.renderer.render_eval_report() on the just-written report and write the HTML alongside (default path: <doc-stem>.eval.html). No new logic - pure composition of the two primitives. Without --render-html, score behaves exactly as today. Acceptance: 'pprose score doc.md --render-html' produces doc.eval.md AND doc.eval.html in one call; result is byte-identical to running 'pprose score doc.md' then 'pprose render doc.eval.md'.
