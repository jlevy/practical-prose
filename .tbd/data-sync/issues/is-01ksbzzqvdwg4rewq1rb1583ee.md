---
type: is
id: is-01ksbzzqvdwg4rewq1rb1583ee
title: "Render + compare: display ERR alongside NA in tables, scoreboards, and notes"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01ksbzxycfj95nzb0mexrshpp6
created_at: 2026-05-24T03:20:47.213Z
updated_at: 2026-05-24T03:20:47.213Z
---
tools/pprose/src/pprose/eval_render.py:41-43 (format_rubric_score): handle 'ERR' the same way as 'NA'. tools/pprose/src/pprose/eval_compare.py:47-49 (the 'Score notes' string) + ~83 (all-NA detection): mention ERR; treat ERR cells like NA cells in row-mean computation.
