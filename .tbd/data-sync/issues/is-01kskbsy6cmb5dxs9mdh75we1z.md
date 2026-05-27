---
type: is
id: is-01kskbsy6cmb5dxs9mdh75we1z
title: Update metrics.py docstring; sanity sweep across repo docs with before/after deltas
kind: task
status: open
priority: 2
version: 1
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:02:01.034Z
updated_at: 2026-05-27T00:02:01.034Z
---
Rewrite the tools/pprose/src/pprose/metrics.py module docstring to document: the single-parse pipeline (chopdiff parses once; pprose reads typed accessors); the Prose inclusion rules (paragraphs + list + blockquote + footnote are prose; headings + table + code + html are not); the new metric catalog including heading_outline and section rollups; the pluggable splitter hook. Rewrite Known Limitations — most prior limitations are reduced or gone. Then run 'pprose metrics' across docs/, runbooks/, shortcuts/, and skills/ on main and on this branch; capture the before/after delta for sentence_count, paragraph_count, heading_count in a short comparison table and paste into the PR description.
