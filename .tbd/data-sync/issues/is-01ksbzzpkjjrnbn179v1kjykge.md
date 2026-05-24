---
type: is
id: is-01ksbzzpkjjrnbn179v1kjykge
title: "Pydantic: update Score type to int 1-5 | Literal['NA','ERR']"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01ksbzxycfj95nzb0mexrshpp6
created_at: 2026-05-24T03:20:45.937Z
updated_at: 2026-05-24T03:55:30.150Z
closed_at: 2026-05-24T03:55:30.149Z
close_reason: implemented on rubric-zero-to-err branch (PR pending)
---
tools/pprose/src/pprose/eval_report.py:43 (Score alias) and the validator/comment block above it. Field constraint ge=1 (was ge=0). Update the inline comments at lines ~38-43 and ~536-543 explaining why ERR + NA are excluded from rollup means.
