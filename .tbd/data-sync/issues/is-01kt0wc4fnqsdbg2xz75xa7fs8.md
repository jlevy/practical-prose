---
type: is
id: is-01kt0wc4fnqsdbg2xz75xa7fs8
title: Extract tip-panels CSS + JS into render-components/tip-panels/
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
created_at: 2026-06-01T06:01:42.131Z
updated_at: 2026-06-01T06:14:56.997Z
closed_at: 2026-06-01T06:14:56.996Z
close_reason: Implemented in Phase 1 commit.
---
From the same explorations file: (a) lift .bi-tip-panel* CSS rules and the @keyframes bi-tip-fade-in into tools/render-components/tip-panels/tip-panels.css. (b) lift the JS functions setupTipPanel, renderDim, renderGroup into tools/render-components/tip-panels/tip-panels.js. Wrap in an IIFE exposing window.PracticalProseTipPanels with a single mount(detailSelector, assessSelector, data) entry point. The component uses marked from window.marked (Phase 1: marked.min.js is bundled alongside, see scaffold bead). Write README.md with the data contract (includes rubric questions + rules per dim; per-doc scores + reasons + findings).
