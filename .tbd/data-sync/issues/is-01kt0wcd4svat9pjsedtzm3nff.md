---
type: is
id: is-01kt0wcd4svat9pjsedtzm3nff
title: Wire the explorations workbench to consume shared components
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0wdsdxen1z505jfgq70k2e
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:01:51.001Z
updated_at: 2026-06-01T06:32:01.009Z
closed_at: 2026-06-01T06:32:01.005Z
close_reason: "Phase 1a complete: workbench loads shared CSS via <link> + shared JS via <script src> from tools/render-components/. mountThemeToggle moved out of lib/design-color-controls.js. 8 new test_workbench_consumes_shared.py tests verify the imports. Deletion of duplicated inline copies tracked as pp-h1v0 (Phase 1b — needs renderBidirectional refactor to call PracticalProseTipPanels.mount with a scope option)."
---
Deferred to follow-up — workbench file is 5500 lines and the spec calls for visual sign-off after the rewire. Tackle in a fresh session with the user actively verifying the workbench renders identically before/after. The render-components/ canonical files already exist; this bead is now purely about pointing the workbench's <style> + <script> at them.
