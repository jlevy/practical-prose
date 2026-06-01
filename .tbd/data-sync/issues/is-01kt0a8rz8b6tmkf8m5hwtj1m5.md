---
type: is
id: is-01kt0a8rz8b6tmkf8m5hwtj1m5
title: Input-kind detection + dispatch table in renderer.py
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-29-static-html-eval-report.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0a988swdskqf2dxkgb5pza
parent_id: is-01kt0a89n7vxq8pc32h8htb3kx
created_at: 2026-06-01T00:45:17.669Z
updated_at: 2026-06-01T01:17:42.792Z
closed_at: 2026-06-01T01:17:42.791Z
close_reason: Implemented in Phase 1; tests pass, lint clean, end-to-end smoke test produces 48KB self-contained HTML
---
Implement detect_kind(path) -> 'eval_report' | None and a small dispatch table mapping kind -> render function. Detection rule for Phase 1: file ends with '.eval.md', or '.md' whose frontmatter validates as an EvalReport. Unknown kinds raise a clear error naming the detected kind plus the supported kinds. Public render(path_or_obj, opts) -> HTML string routes through the table. Phase 1 registers exactly one entry: 'eval_report' -> render_eval_report (stubbed; real implementation in a later bead). Unit-test detection on a fixture .eval.md, a plain .md, and an arbitrary text file.
