---
type: is
id: is-01kt0a988swdskqf2dxkgb5pza
title: Implement render_eval_report() + per-section templates
kind: task
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/done/plan-2026-05-29-static-html-eval-report.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0a9bqdn8nnp9qakxr61fh8
  - type: blocks
    target: is-01kt0a9gsq6batsb6vb0mcf3k0
  - type: blocks
    target: is-01kt0a9nd0xknbge25v7hz56aw
  - type: blocks
    target: is-01kt0a9shf12zsdj7racajn2n7
parent_id: is-01kt0a89n7vxq8pc32h8htb3kx
created_at: 2026-06-01T00:45:33.336Z
updated_at: 2026-06-13T18:38:35.686Z
closed_at: 2026-06-01T01:17:43.192Z
close_reason: Implemented in Phase 1; tests pass, lint clean, end-to-end smoke test produces 48KB self-contained HTML
---
Wire up renderer.py::render_eval_report(report: EvalReport, opts) -> str. Build the Jinja context from the report (qual, qual_reasons, rule_findings, quant, derived, artifact) plus design-system tokens. Implement the four section templates: (1) page_card.html.jinja (from the Visual 9B extraction bead), (2) page_detail.html.jinja - one block per dimension with id+label, group, score, rubric question (from rubric_schema.yaml), qual_reasons text, and rule_findings; break-inside: avoid on each block. (3) page_metrics.html.jinja - compact quant/derived block (simplified Visual 10). (4) page_footer.html.jinja - eval method/model/rubric version/date/source-doc ref/pprose version. Renderer emits sections based on which data blocks the report actually contains (missing block silently skips its section). Honor --sections to subset further.
