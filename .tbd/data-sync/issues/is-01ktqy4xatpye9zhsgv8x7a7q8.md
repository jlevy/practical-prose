---
type: is
id: is-01ktqy4xatpye9zhsgv8x7a7q8
title: "lint: rules_schema.py — pydantic rule models + loader + anchor validation"
kind: task
status: open
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktqxg5a0ja7mf8sv4e8175t1
  - type: blocks
    target: is-01ktqy4xhsfvm7anze87zcwr53
  - type: blocks
    target: is-01ktqy4xycddag568m452jg2rg
created_at: 2026-06-10T04:55:14.521Z
updated_at: 2026-06-10T04:56:00.779Z
---
New file tools/pprose/src/pprose/rules_schema.py. Functions/classes: Severity (enum flag|cut); FuzzyPattern(pattern, threshold); DetectSpec(exact: list[str], fuzzy: list[FuzzyPattern], model_hints: str, structural: str); RuleExamples(bad, good); Rule(id, summary, correction, exceptions, detect, examples, source, first_flagged); RuleFile(category, doc_anchor, severity, rules). load_rules(rules_dir: Path) -> list[Rule] with YAML parse + pydantic validation; validate_doc_anchors(rules, docs_dir) -> list[str] (checks each doc_anchor heading exists in docs/ai-prose-mitigations.md / ai-prose-corrections.md so code and prose cannot drift). Mirror rubric_schema.py conventions. Unit tests in tests/test_rules_schema.py.
