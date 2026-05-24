---
type: is
id: is-01ksbzzq12pg20htppqdndyhy8
title: "Validation: align alignment-validation rules for score==ERR with current score==0 behavior"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01ksbzxycfj95nzb0mexrshpp6
created_at: 2026-05-24T03:20:46.369Z
updated_at: 2026-05-24T03:55:30.504Z
closed_at: 2026-05-24T03:55:30.503Z
close_reason: implemented on rubric-zero-to-err branch (PR pending)
---
tools/pprose/src/pprose/eval_report.py:430-442: where the validator excuses violations for score 0 or NA, swap 0 -> ERR. Same downstream invariants (no violations required for ERR; excluded from any mean).
