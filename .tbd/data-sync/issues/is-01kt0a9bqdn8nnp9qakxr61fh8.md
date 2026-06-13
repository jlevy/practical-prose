---
type: is
id: is-01kt0a9bqdn8nnp9qakxr61fh8
title: CSS/SVG inliner for single-file output + --format flag
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/done/plan-2026-05-29-static-html-eval-report.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0a9shf12zsdj7racajn2n7
  - type: blocks
    target: is-01kt0a9x5m907a3gz0sxtbhft1
parent_id: is-01kt0a89n7vxq8pc32h8htb3kx
created_at: 2026-06-01T00:45:36.876Z
updated_at: 2026-06-13T18:38:35.686Z
closed_at: 2026-06-01T01:17:43.393Z
close_reason: Implemented in Phase 1; tests pass, lint clean, end-to-end smoke test produces 48KB self-contained HTML
---
Implement inliner.py for single-file mode: collect styles/*.css into one inlined <style> in base.html.jinja, embed assets/icons.svg as an inline SVG symbol set (or data-URI). No external CDN refs at view time. Implement the --format folder mode as a thin alternative that writes HTML + sidecar styles/ + assets/ for dev inspection. Single-file is the default. Test: rendering a fixture in 'single' mode produces a self-contained file with no external <link> or <script> tags; opening it offline still renders correctly.
