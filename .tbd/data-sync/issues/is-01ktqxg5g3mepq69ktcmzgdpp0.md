---
type: is
id: is-01ktqxg5g3mepq69ktcmzgdpp0
title: Implement phase-A lint detection (regex + fuzzy) in pprose
kind: feature
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktqxg5pe1jh2sg6ht8gs2cqq
created_at: 2026-06-10T04:43:54.754Z
updated_at: 2026-06-10T04:44:07.325Z
---
lint_detect.py: tier 0 compiled regex (extend banned-register machinery in metrics.py) + tier 1 rapidfuzz windowed n-grams over rule files; Match(rule_id, span, tier, score) records; overlapping-span dedup; golden tests incl. licensed-use negative fixtures. Spec Phase 3.
