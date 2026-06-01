---
type: is
id: is-01kt0wbzv8hc39vy2t8ztxd5cx
title: Extract Visual 9B card CSS + JS into render-components/bi-card/
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
    target: is-01kt0wcy0gvgwmr7pxyx9qh0f9
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:01:37.383Z
updated_at: 2026-06-01T06:14:56.805Z
closed_at: 2026-06-01T06:14:56.804Z
close_reason: Implemented in Phase 1 commit.
---
From tools/explorations/visual-design/dimension-visualizations.html: (a) lift the CSS rules whose selectors start with .bi-* (excluding .bi-tip-panel) plus .grp-icon / .grp-icon svg into tools/render-components/bi-card/card.css. (b) lift the JS functions biCard, biDim9B, _biDimPrep, groupIcon, groupAvgChip, dimColorMix, scoreColor, _readScoreAlphaStep, segmentAlpha, and the el() DOM-builder helper into tools/render-components/bi-card/card.js. Wrap them in an IIFE that exposes window.PracticalProseBiCard with a single mount(containerSelector, data) entry point matching the documented data contract { groups, dimensions, rubric, doc }. Helpers stay private inside the IIFE. Write README.md documenting the data contract + a 20-line usage example.
