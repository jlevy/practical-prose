---
type: is
id: is-01ksbzzr01wje4d885ttp4jyrs
title: "Migration: auto-convert score 0 -> ERR on read of older (v1) rubric reports"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01ksbzxycfj95nzb0mexrshpp6
created_at: 2026-05-24T03:20:47.360Z
updated_at: 2026-05-24T03:55:31.341Z
closed_at: 2026-05-24T03:55:31.340Z
close_reason: implemented on rubric-zero-to-err branch (PR pending)
---
tools/pprose/src/pprose/eval_report.py: on load of a report whose rubric_version is the pre-bump value (e.g. 20-dim-v1), coerce any score=0 to score='ERR' before Pydantic validation, and bump the rubric_version stamp during in-place rewrites. Add a small unit test exercising the conversion.
