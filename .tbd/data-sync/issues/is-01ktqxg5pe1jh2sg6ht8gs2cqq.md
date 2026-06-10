---
type: is
id: is-01ktqxg5pe1jh2sg6ht8gs2cqq
title: Implement phase-B parallel verification and pprose lint CLI
kind: feature
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md
labels: []
dependencies: []
created_at: 2026-06-10T04:43:54.958Z
updated_at: 2026-06-10T04:43:54.958Z
---
lint_verify.py: one focused verification call per candidate in parallel (_concurrency.py); prompt = span±2 sentences + single rule's summary/correction/exceptions/exemplar; verdict + proposed_fix; density context for flag-severity. CLI: pprose lint with --json, --no-verify, --detect-model, --verify-model; exit code gated on confirmed cut-severity only. Recorded-response fixtures. Spec Phase 3.
