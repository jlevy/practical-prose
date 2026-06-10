---
type: is
id: is-01ktqy4y4qmqv45sr1a9h0vk6f
title: "lint: golden tests for detection (positives + licensed-use negatives)"
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktqxg5g3mepq69ktcmzgdpp0
created_at: 2026-06-10T04:55:15.350Z
updated_at: 2026-06-10T04:56:00.436Z
---
tests/test_lint_detect.py + tests/test_fixtures/lint/: one fixture doc per category with known violations -> expected Match YAML (mirror practical_prose_metrics fixture pattern); licensed-use negative fixtures that must NOT match: technical idiom for false-agency (the function returns), benchmarked state-of-the-art, single emphatic fragment, em-dash within F2.7 policy. Also fixture with violations inside code blocks/frontmatter that must be skipped (TextDoc structure-awareness test).
