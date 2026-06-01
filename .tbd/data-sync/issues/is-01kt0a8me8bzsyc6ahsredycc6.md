---
type: is
id: is-01kt0a8me8bzsyc6ahsredycc6
title: Add 'pprose render' subcommand skeleton + render_html package scaffold
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-05-29-static-html-eval-report.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0a8rz8b6tmkf8m5hwtj1m5
  - type: blocks
    target: is-01kt0a92st5e3r1p2k9188sx6p
parent_id: is-01kt0a89n7vxq8pc32h8htb3kx
created_at: 2026-06-01T00:45:13.031Z
updated_at: 2026-06-01T01:17:42.382Z
closed_at: 2026-06-01T01:17:42.381Z
close_reason: Implemented in Phase 1; tests pass, lint clean, end-to-end smoke test produces 48KB self-contained HTML
---
Create tools/pprose/src/pprose/render_html/ with __init__.py, cli.py (argparse), renderer.py (stub), inliner.py (stub), templates/, styles/, assets/. Register 'render' in tools/pprose/src/pprose/cli.py COMMANDS table under the 'Evaluate' group with a one-line summary. Wire importlib.resources so bundled templates/styles/assets load from the installed wheel (mirror how rubric_schema.yaml and resources/ are loaded today). At this stage the subcommand parses args and prints 'not implemented'; verify the package shows up in 'pprose --help'.
