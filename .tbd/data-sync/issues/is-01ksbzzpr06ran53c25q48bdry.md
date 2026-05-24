---
type: is
id: is-01ksbzzpr06ran53c25q48bdry
title: "Rollup: add err_dimensions count to DerivedRollup alongside na_dimensions"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01ksbzxycfj95nzb0mexrshpp6
created_at: 2026-05-24T03:20:46.079Z
updated_at: 2026-05-24T03:55:30.264Z
closed_at: 2026-05-24T03:55:30.263Z
close_reason: implemented on rubric-zero-to-err branch (PR pending)
---
tools/pprose/src/pprose/eval_report.py: add 'err_dimensions: int' field to DerivedRollup (~line 318), populate it in _compute_rubric_rollup (~line 558) by counting scores == 'ERR'. Surfaces 'we couldn't score X dims' instead of silently dropping them.
