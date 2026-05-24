---
type: is
id: is-01ksbzzpwf3z5m79a4tqkx11h8
title: "Aggregation + stub: update _mean_scored to skip ERR, regenerate stub with ERR instead of 0"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01ksbzxycfj95nzb0mexrshpp6
created_at: 2026-05-24T03:20:46.223Z
updated_at: 2026-05-24T03:55:30.383Z
closed_at: 2026-05-24T03:55:30.382Z
close_reason: implemented on rubric-zero-to-err branch (PR pending)
---
tools/pprose/src/pprose/eval_report.py:_mean_scored (~543): treat ERR identically to NA (skip from mean). Update the stub generator (~658-700) so the placeholder qual block uses 'ERR' for every dimension (was 0). Update the 'no scored dimensions' check (~698) to detect all-ERR-or-NA.
