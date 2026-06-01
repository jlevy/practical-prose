---
type: is
id: is-01kt0y0s9skpjt8fytng566npn
title: Delete duplicated inline CSS/JS from explorations workbench (Phase 1b)
kind: task
status: open
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0wdsdxen1z505jfgq70k2e
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:30:27.384Z
updated_at: 2026-06-01T06:30:29.213Z
---
After pp-eece's Phase 1a (which added <link>/<script src> references to the shared render-components), the workbench's inline <style> + main inline <script> still carry duplicate copies of the .bi-* CSS, the bi-card/tip-panels function definitions, and the .theme-toggle CSS. The shared files are byte-identical (verified by the sync drift check), so the duplicates are inert but they're the long-tail cleanup. To finish: 1) Replace the workbench's call to setupTipPanel(detailEl, assessEl) with PracticalProseTipPanels.mount() — this likely requires extending the shared mount() to accept a  option for per-viz hover scoping (the workbench has 9A and 9B side-by-side). 2) Rewrite renderBidirectional to source biCard/biDim9B/groupAvgChip/groupIcon from PracticalProseBiCard.makeApi(). 3) Delete the inline .bi-*, .bi-tip-panel*, .grp-icon, .theme-toggle CSS rules. 4) Delete the inline function defs (biCard, biDim9B, _biDimPrep, groupIcon, groupAvgChip, _readScoreAlphaStep, dimColorMix, scoreColor, segmentAlpha, setupTipPanel). 5) Tighten tests/test_workbench_consumes_shared.py to assert the inline copies are gone. Visual sign-off required — open the workbench before/after and confirm 9A + 9B + theme toggle + surface toggle all still work.
