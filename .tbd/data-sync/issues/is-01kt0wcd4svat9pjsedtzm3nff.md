---
type: is
id: is-01kt0wcd4svat9pjsedtzm3nff
title: Wire the explorations workbench to consume shared components
kind: task
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0wdsdxen1z505jfgq70k2e
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:01:51.001Z
updated_at: 2026-06-01T06:15:09.720Z
---
Deferred to follow-up — workbench file is 5500 lines and the spec calls for visual sign-off after the rewire. Tackle in a fresh session with the user actively verifying the workbench renders identically before/after. The render-components/ canonical files already exist; this bead is now purely about pointing the workbench's <style> + <script> at them.
