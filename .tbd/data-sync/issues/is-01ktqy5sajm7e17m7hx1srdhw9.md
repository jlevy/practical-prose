---
type: is
id: is-01ktqy5sajm7e17m7hx1srdhw9
title: "lint: lint_verify.py — parallel per-candidate verification via pydantic-ai"
kind: task
status: open
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktqxg5pe1jh2sg6ht8gs2cqq
  - type: blocks
    target: is-01ktqy5sgywckk5nmczga66h3k
  - type: blocks
    target: is-01ktqy5sq3vwxnys2m10ywcrjy
created_at: 2026-06-10T04:55:43.185Z
updated_at: 2026-06-10T04:57:59.559Z
---
New file tools/pprose/src/pprose/lint_verify.py. Classes/functions: VerdictModel (pydantic: verdict Literal[violation,licensed,false_positive], reason: str, proposed_fix: str|None) used as pydantic-ai output_type for schema-enforced output (no fragile parsing — improves on leximetry Score.parse approach); build_verify_prompt(match, rule, context) (span ±2 sentences via TextDoc.sentence_at_offset; include ONLY the one rule summary+correction+exceptions+bad/good exemplar; density context appended for flag-severity rules); verify_candidate(match, rule, model) -> VerifiedMatch (one focused Agent.run per candidate — the per-judgment pattern proven in leximetry evaluate_single_metric); verify_all(report, model_name) -> LintReport via existing _concurrency.gather_limited (max_concurrent/max_rps already tuned in eval_score.py). Model selection via existing _resolve_model/pydantic-ai provider prefixes; default verify model per fast-models research bead.
MODEL PICKS (researched 2026-06-09): default verify model claude-haiku-4-5 (structured output GA; binary per-criterion verdicts are the reliable regime for small judges per GLIDER arXiv:2412.14140); VerdictModel gains confidence field; route uncertain verdicts to Sonnet 4.6 (~10% escalation, sub-cent cost). Include 1-2 positive/negative exemplars per rule in the prompt. Consider verdict-on-Haiku, fix-on-Sonnet if fix quality disappoints.
