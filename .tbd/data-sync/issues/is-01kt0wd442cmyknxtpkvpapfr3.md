---
type: is
id: is-01kt0wd442cmyknxtpkvpapfr3
title: Author base.html.jinja shell + interactive variant
kind: task
status: closed
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0wd6xe32z4gjbtjbapgs58
  - type: blocks
    target: is-01kt0wdbv1016t7ta4nxxaqwyz
  - type: blocks
    target: is-01kt0wdfzjjqe6sdawfc77e4v1
  - type: blocks
    target: is-01kt0wdn9eh9m81ct8n1gr8k7y
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:02:14.529Z
updated_at: 2026-06-01T06:14:57.930Z
closed_at: 2026-06-01T06:14:57.929Z
close_reason: Implemented in Phase 1 commit.
---
Rewrite tools/pprose/src/pprose/render_html/templates/base.html.jinja into the variant-agnostic outer shell: <html data-surface="white" data-theme-mode="auto"><head> with inlined CSS via {{ css|safe }} and inlined JS via {{ js|safe }}, <body> with the inlined icon sprite ({{ icons_svg|safe }}), the theme-toggle partial ({% include 'theme-toggle.html.jinja' %}), then Jinja blocks: {% block layout %} (the per-variant DOM scaffolding) and {% block bootstrap %} (the per-variant <script> that calls mount() on the components). Add tools/pprose/src/pprose/render_html/templates/variants/interactive.html.jinja that extends base, fills  with the empty .bi-stack container + the two .bi-tip-panel-detail / .bi-tip-panel-assess asides, and fills  with the three mount() calls plus the <script type="application/json" id="pp-eval-data"> block carrying the JSON payload. Delete page_card.html.jinja, page_detail.html.jinja, page_metrics.html.jinja, page_footer.html.jinja.
