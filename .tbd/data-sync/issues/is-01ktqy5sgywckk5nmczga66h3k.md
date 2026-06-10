---
type: is
id: is-01ktqy5sgywckk5nmczga66h3k
title: "lint: cli.py lint subcommand + terminal/JSON rendering + exit gating"
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktqxg5pe1jh2sg6ht8gs2cqq
created_at: 2026-06-10T04:55:43.389Z
updated_at: 2026-06-10T04:56:01.355Z
---
Extend tools/pprose/src/pprose/cli.py with lint subcommand: pprose lint <file.md> [--rules DIR] [--no-verify] [--verify-model M] [--detect-model M] [--json]. New lint_render.py (or extend eval_render.py): pretty terminal report grouped by category with span excerpts + verdicts + proposed fixes (reuse table_styles/rich conventions; leximetry report_output.py is the visual precedent); --json emits LintReport.to_json(). Exit code: nonzero ONLY on confirmed cut-severity violations (CI-safe; flag-tier never gates). Register in install.py surfaces if needed.
