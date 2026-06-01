---
type: is
id: is-01kt0wc871tfh3b6qgqqrrpdej
title: Extract mountThemeToggle into render-components/theme-toggle/
kind: task
status: closed
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0wcd4svat9pjsedtzm3nff
  - type: blocks
    target: is-01kt0wcj8vnf5gk2c92fqzadvr
  - type: blocks
    target: is-01kt0wd442cmyknxtpkvpapfr3
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:01:45.952Z
updated_at: 2026-06-01T06:14:57.185Z
closed_at: 2026-06-01T06:14:57.185Z
close_reason: Implemented in Phase 1 commit.
---
Move only the mountThemeToggle half of tools/explorations/visual-design/lib/design-color-controls.js into tools/render-components/theme-toggle/theme-toggle.js. mountSurfaceToggle and the surface UI stay in the workbench's local lib/. Lift the .theme-toggle CSS rules (not .surface-toggle) from the explorations HTML's <style> block into tools/render-components/theme-toggle/theme-toggle.css. Write tools/render-components/theme-toggle/theme-toggle.html.jinja with the three-button markup verbatim from the workbench. Wrap the JS in an IIFE exposing window.PracticalProseDesignColorControls.mountThemeToggle(containerSelector, opts?). README.md documents the markup contract and the mode option.
