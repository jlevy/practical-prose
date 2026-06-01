---
type: is
id: is-01kt0wdbv1016t7ta4nxxaqwyz
title: Print rules + light-mode forcing in styles/print.css
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0wdn9eh9m81ct8n1gr8k7y
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:02:22.433Z
updated_at: 2026-06-01T06:14:58.295Z
closed_at: 2026-06-01T06:14:58.294Z
close_reason: Implemented in Phase 1 commit.
---
Rewrite tools/pprose/src/pprose/render_html/styles/print.css: keep the @page rules (size: letter; margin: 0.6in) and break-inside: avoid on cards/panels; add @media print { .theme-toggle { display: none !important; } } so the toggle is hidden in printed PDFs; add @media print { :root, :root[data-theme="dark"], :root[data-surface="white"][data-theme="dark"] { ...force light tokens... } } that overrides every surface and per-dim hue to its light-mode value so a user in dark mode still prints a clean light PDF. Mirror the light values from the canonical design_system.css :root block. Manual visual sign-off — confirm Cmd-P preview is clean light + toggle hidden, on both Letter and A4.
