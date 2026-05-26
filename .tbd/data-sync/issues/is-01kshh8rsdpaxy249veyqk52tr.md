---
type: is
id: is-01kshh8rsdpaxy249veyqk52tr
title: Update module docstring; sanity sweep across repo docs with before/after deltas
kind: task
status: open
priority: 2
version: 1
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T06:59:01.023Z
updated_at: 2026-05-26T06:59:01.023Z
---
Rewrite the tools/pprose/src/pprose/metrics.py module docstring to document: the new single-Markdown-parse pipeline; the Prose inclusion rules (paragraphs + list items + blockquotes + footnote bodies are prose; headings, table cells, code, HTML are not); the new metric catalog including heading_outline and section rollups; the pluggable splitter hook on build_structure. Rewrite the Known Limitations list — most prior limitations (phantom setext headings from HRs, banned-register false positives from quoted examples, etc.) are reduced or gone. Then run 'pprose metrics' across docs/, runbooks/, shortcuts/, and skills/ on main and on this branch; capture the before/after delta for sentence_count, paragraph_count, heading_count in a short comparison table and paste into the eventual PR description.
