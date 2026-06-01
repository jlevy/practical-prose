---
type: is
id: is-01kt0a8xtz8w43sm00sjkqzank
title: Extract Visual 9B card markup + CSS from explorations into Jinja template
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-29-static-html-eval-report.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0a988swdskqf2dxkgb5pza
parent_id: is-01kt0a89n7vxq8pc32h8htb3kx
created_at: 2026-06-01T00:45:22.654Z
updated_at: 2026-06-01T01:17:42.586Z
closed_at: 2026-06-01T01:17:42.585Z
close_reason: Implemented in Phase 1; tests pass, lint clean, end-to-end smoke test produces 48KB self-contained HTML
---
From tools/explorations/visual-design/dimension-visualizations.html: (a) lift CSS scoped under .bi-, .bi-ltr, .doc-kicker, .doc-name into tools/pprose/src/pprose/render_html/styles/card.css; (b) port the JS-built DOM in biCard()/biDim9B() to static Jinja in templates/page_card.html.jinja, driven by an EvalReport context. Per-dim hues are emitted as inline CSS custom properties on each row (style='--dim-hue: 72'). The hover-driven tip panels are REMOVED here; their content moves to the per-dim detail page bead. No JavaScript in the rendered page. Acceptance: rendering one fixture report produces an HTML card visually matching Visual 9B side-by-side with the explorations file.
