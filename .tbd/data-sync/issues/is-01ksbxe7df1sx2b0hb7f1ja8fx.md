---
type: is
id: is-01ksbxe7df1sx2b0hb7f1ja8fx
title: Implement rendered eval reports
kind: feature
status: open
priority: 2
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-23-rendered-eval-reports.md
labels: []
dependencies: []
created_at: 2026-05-24T02:36:16.170Z
updated_at: 2026-05-25T05:20:00.393Z
---
Add a renderer-neutral presentation model and YAML/Markdown/standalone HTML output formats for single-document Practical Prose eval reports, including static HTML drill-downs and optional source examples.

## Notes

Design system foundation landed on 2026-05-25 (commit f22b2cb on visual-design): YAML source of truth + generated CSS/JS/Python at tools/design-system/.  Renderer should consume the generated CSS via <link> and the generated Python palette via pprose._generated.design_system.  Visual exploration of layouts done in tools/explorations/visual-design/ (9 chart prototypes).  This work is now unblocked.
