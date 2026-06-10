---
type: is
id: is-01ktqy4xravvps9tr8q6a7z6s9
title: "lint: lint_types.py — Match and LintReport models"
kind: task
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktqxg5g3mepq69ktcmzgdpp0
  - type: blocks
    target: is-01ktqy4xycddag568m452jg2rg
created_at: 2026-06-10T04:55:14.954Z
updated_at: 2026-06-10T04:56:00.610Z
---
New file tools/pprose/src/pprose/lint_types.py. Match(rule_id: str, span: tuple[int,int], text: str, tier: Literal[exact,fuzzy,model,structural], score: float, detail: dict); VerifiedMatch(match, verdict: Literal[violation,licensed,false_positive], reason, proposed_fix); LintReport(doc_path, matches, verified, stats; to_json()). Keep JSON shape stable: this is the contract consumed by the future overlay renderer (research pp-xrqd) and CI.
