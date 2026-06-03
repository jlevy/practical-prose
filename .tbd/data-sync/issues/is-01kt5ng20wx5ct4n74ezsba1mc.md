---
type: is
id: is-01kt5ng20wx5ct4n74ezsba1mc
title: "Test: score --batch partial-failure isolation"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/release-readiness-2026-06.md
labels:
  - release
  - test
dependencies: []
parent_id: is-01kt5nebv6vqtrx17dfy0hy04m
created_at: 2026-06-03T02:37:42.811Z
updated_at: 2026-06-03T02:37:42.811Z
---
Automation candidate. score_batch / _concurrency.gather_limited have ZERO test coverage (grep finds no references). Using the existing FunctionModel/monkeypatch harness (no real key), add a test that one corrupt file does not abort the others (return_exceptions path), the summary line is correct, and exit code is 1-on-any-fail / 0-on-all-pass.
