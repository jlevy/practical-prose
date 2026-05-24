---
type: is
id: is-01ksbzzr90mr7hztqp2pmtzr6r
title: "Tests + fixtures: cover ERR semantics; remove or convert any 0-score test cases"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01ksbzxycfj95nzb0mexrshpp6
created_at: 2026-05-24T03:20:47.647Z
updated_at: 2026-05-24T03:55:31.581Z
closed_at: 2026-05-24T03:55:31.580Z
close_reason: implemented on rubric-zero-to-err branch (PR pending)
---
Sweep tools/pprose/tests/ and any committed eval YAML fixtures for score: 0 or score == 0. Convert to ERR (or to 1 + rule cite, depending on what the fixture is exercising). Add positive tests for: (a) ERR excluded from group/overall mean, (b) err_dimensions counter populated, (c) migration of a v1 report with 0 to a v2 report with ERR.
