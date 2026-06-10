---
type: is
id: is-01ktqy5sq3vwxnys2m10ywcrjy
title: "lint: recorded-response tests for verification + e2e smoke"
kind: task
status: open
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktqxg5pe1jh2sg6ht8gs2cqq
created_at: 2026-06-10T04:55:43.586Z
updated_at: 2026-06-10T04:56:01.542Z
---
tests/test_lint_verify.py: recorded/canned VerdictModel responses via pydantic-ai TestModel/FunctionModel (no live calls in CI); verify prompt-building (context window edges: match in first/last sentence), density-context inclusion for flag-severity, exit-code gating logic. One live smoke test behind env flag (mirror existing eval smoke pattern if present).
