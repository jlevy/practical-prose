---
type: is
id: is-01kshmthfgw30hr3ptx88y4ze9
title: Update metrics.py docstring; sanity sweep across repo docs with before/after deltas
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:01:09.096Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-05-27T00:00:53.705Z
close_reason: "Superseded by spec rewrite 2026-05-26 (v3). New architecture: chopdiff v0.4.x parses each block once and exposes typed accessors (heading_level, code_language, list_info, table_info, inlines, section_tree). Pprose becomes a thin serializer with no marko import and no per-block re-parse. Replaced by a fresh bead set."
---
Rewrite the tools/pprose/src/pprose/metrics.py module docstring to document: the BlockDoc-based pipeline; the Prose inclusion rules (paragraphs + list items + blockquotes + footnote bodies are prose; headings, table cells, code, HTML are not); the new metric catalog including heading_outline and section rollups; the pluggable splitter hook. Rewrite Known Limitations — most prior limitations (phantom setext headings from HRs, banned-register false positives from quoted examples, etc.) are reduced or gone. Then run 'pprose metrics' across docs/, runbooks/, shortcuts/, and skills/ on main and on this branch; capture the before/after delta for sentence_count, paragraph_count, heading_count in a short comparison table and paste into the PR description.
