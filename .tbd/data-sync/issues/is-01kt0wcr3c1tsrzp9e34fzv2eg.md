---
type: is
id: is-01kt0wcr3c1tsrzp9e34fzv2eg
title: Rewrite inliner.py + drop hand-edited per-section CSS
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0wd442cmyknxtpkvpapfr3
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:02:02.219Z
updated_at: 2026-06-01T06:14:57.562Z
closed_at: 2026-06-01T06:14:57.561Z
close_reason: Implemented in Phase 1 commit.
---
Rewrite tools/pprose/src/pprose/render_html/inliner.py to read CSS from styles/_generated/{design_system,bi-card,tip-panels,theme-toggle}.css plus the renderer-owned styles/print.css, and JS from js/_generated/{marked.min,bi-card,tip-panels,theme-toggle}.js. Drop the old hand-edited per-section CSS files (card.css, detail.css, surface_white.css, static_adaptations.css, base.css, metrics.css, local_extras.css) — they're either now sourced from _generated/ or no longer needed (the variant template owns layout). The bundled_css() function still rewrites size: letter -> size: A4 when --page-size a4 is passed. Add bundled_js() returning the concatenated script bundle. write_folder_assets() now writes the synced _generated/ tree as-is (no flat assets/ rewrite) so dev-mode inspection mirrors the wheel layout.
