---
type: is
id: is-01kt0wbtdd2fnj2qfb70jv59je
title: Scaffold tools/render-components/ directory structure
kind: task
status: closed
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0wbzv8hc39vy2t8ztxd5cx
  - type: blocks
    target: is-01kt0wc4fnqsdbg2xz75xa7fs8
  - type: blocks
    target: is-01kt0wc871tfh3b6qgqqrrpdej
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:01:31.820Z
updated_at: 2026-06-01T06:04:39.213Z
closed_at: 2026-06-01T06:04:39.212Z
close_reason: Scaffold dirs created (bi-card, tip-panels, theme-toggle, vendor); marked@12.0.2 vendored (35KB).
---
Create tools/render-components/ with subdirs bi-card/, tip-panels/, theme-toggle/, vendor/. Each component dir gets an initially-empty README.md, .css, and .js file. theme-toggle/ also gets .html.jinja. vendor/ gets a downloaded marked.min.js (marked@12.0.2 per the explorations file's CDN reference). No content yet — just the empty skeletons so subsequent extraction beads have targets to write into.
