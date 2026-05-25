---
type: is
id: is-01ksg3tqpt70mfp1cdqtf7cpkt
title: "Research: existing prose-visualization UIs that compose multiple overlays"
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01ksg3sj3t15ybgab2rwcnxqs3
created_at: 2026-05-25T17:44:55.257Z
updated_at: 2026-05-25T17:55:42.166Z
closed_at: 2026-05-25T17:55:42.162Z
close_reason: "Prose-visualization UI patterns survey complete. FIVE RECURRING UX PATTERNS identified across writing aids / DH / stylometry / pedagogy / annotation / AI-text detection: (A) inline color + hover detail + summary sidebar (Hemingway, Grammarly, GLTR, Sapling); (B) toggleable layers over one canvas (ProWritingAid, Microsoft Editor, INCEpTION, BRAT); (C) coordinated multi-panel views (Voyant, AntConc, Sketch Engine, BertViz); (D) global overview -> instance drill-down (LMdiff, GPTZero, Stylo rolling); (E) per-position ribbon/margin heatmap (AntConc Concordance Plot, Stylo strip, GitHub minimap). KEY CONSTRAINTS: stacked background fills break past 2 categories -- use underlines (Grammarly lesson); 4-5 categorical bins is the legibility ceiling at body-text size; bucketed discrete coloring beats continuous gradients (GLTR's choice); push numeric badges to hover/sidebar. STRONGEST REFERENCES: Strobelt corpus (GLTR + LMdiff + LIT) is the most coherent body of prose-overlay design work. RECOMMENDED COMPOSITION for pprose-eval: hybrid B+D+E+A in three regions -- (top) rubric overview, (center) single canonical document canvas with layer manager + margin ribbon, (right) inspector showing all overlays for selected span. One active fill at a time; other enabled layers render as underlines/margin dots. Pre-computed static HTML; coordinated-state store; design-system HSL colors. Multi-model = LMdiff signed-diff color on same canvas; side-by-side only past two models."
---
Survey existing UIs that render multiple overlays on the same prose (readability + register + AI-tells + rarity + voice). Goal: identify UX patterns the practical-prose project could adopt for an eval-report visualization. Cover: Hemingway Editor; ProWritingAid visualization layers; Grammarly's tone+clarity+correctness composite; Voyant Tools (digital humanities); LIWC and LIWC-22 dashboards; AcaWriter and academic-writing-feedback systems; WriteFull; Stylo R package outputs; KWIC concordance UIs (AntConc, Sketch Engine); annotation tooling (BRAT, INCEpTION, Doccano); modern AI-tell visualizers (any Slopless / stop-slop UI? check). For each: overlay model (per-token / per-sentence / per-section), composition (single overlay vs stacked vs toggleable layers), export format, license. Output: UX-pattern inventory + recommended composition pattern for pprose-eval.
