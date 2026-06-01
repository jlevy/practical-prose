---
type: is
id: is-01kt0wdfzjjqe6sdawfc77e4v1
title: Update pyproject.toml wheel includes for new layout
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0wdsdxen1z505jfgq70k2e
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:02:26.673Z
updated_at: 2026-06-01T06:14:58.476Z
closed_at: 2026-06-01T06:14:58.475Z
close_reason: Implemented in Phase 1 commit.
---
Update tools/pprose/pyproject.toml [tool.hatch.build.targets.wheel] include list to ship the new paths: src/pprose/render_html/styles/_generated/*.css, src/pprose/render_html/styles/*.css (for print.css), src/pprose/render_html/js/_generated/*.js, src/pprose/render_html/templates/*.html.jinja, src/pprose/render_html/templates/variants/*.html.jinja, src/pprose/render_html/assets/icons.svg. Remove old include patterns that referenced now-deleted files. Run  and confirm the wheel manifest contains exactly the expected files.
