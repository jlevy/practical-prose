---
type: is
id: is-01kt5a9fg8bjajmfrwyqc93rhg
title: Thread finding locations into the HTML panel payload
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-06-02-eval-output-improvements.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt5a9g0s2jbh3g9jj4kq38cb
parent_id: is-01kt58cfg7tym70xehy10c8ckc
created_at: 2026-06-02T23:21:52.903Z
updated_at: 2026-06-03T19:15:14.232Z
closed_at: 2026-06-03T19:15:14.231Z
close_reason: Superseded by reporting CLI redesign epic pp-d2j3 (spec plan-2026-06-03-reporting-cli-redesign.md); work folded into its phases.
---
In render_html/renderer.py add a compact 'locations' string to each finding dict (reuse/lift eval_render._format_locations: quote -> section -> line range -> note) so Markdown and HTML renderings match.
