---
type: is
id: is-01kx3zka7ekk1tpz37nxfh61ba
title: Accessibility smoke test for the rendered eval page
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-07-09T17:42:51.886Z
updated_at: 2026-07-09T17:42:51.886Z
---
The bibliography carries a full accessibility section and cites WCAG 2.2 as normative, but the pprose render HTML pipeline has no a11y check: tip panels are hover-driven (keyboard access?), theme toggle, contrast of the score ramp, alt/aria on the card SVG icons. Add an axe-core (or equivalent) smoke to the e2e render test; pairs with the visual-regression bead pp-5zgc. From review-2026-07-09.
