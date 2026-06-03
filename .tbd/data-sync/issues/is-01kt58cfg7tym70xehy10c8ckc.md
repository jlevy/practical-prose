---
type: is
id: is-01kt58cfg7tym70xehy10c8ckc
title: "Phase 2: surface rule-finding location anchors in the interactive HTML panel"
kind: task
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-06-02-eval-output-improvements.md
labels: []
dependencies: []
parent_id: is-01kt58c3t45ac6ag66v1wfcgvc
child_order_hints:
  - is-01kt5a9fg8bjajmfrwyqc93rhg
  - is-01kt5a9g0s2jbh3g9jj4kq38cb
  - is-01kt5a9gfhnwb2znzn4w4yfm94
created_at: 2026-06-02T22:48:34.054Z
updated_at: 2026-06-03T19:15:12.293Z
closed_at: 2026-06-03T19:15:12.291Z
close_reason: Superseded by reporting CLI redesign epic pp-d2j3 (spec plan-2026-06-03-reporting-cli-redesign.md); work folded into its phases.
---
Thread compact-formatted locations (shared with eval_render._format_locations) into the finding payload in render_html/renderer.py. Render them under each finding in tip-panels.js; style in tip-panels.css. Regenerate _generated mirrors via sync_render_html_styles.py; make generate-check clean. HTML e2e test asserts a known anchor reaches the output.
