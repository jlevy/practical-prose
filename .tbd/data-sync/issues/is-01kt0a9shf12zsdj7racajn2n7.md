---
type: is
id: is-01kt0a9shf12zsdj7racajn2n7
title: Golden HTML tests + schema-coverage test for render
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/done/plan-2026-05-29-static-html-eval-report.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0a9x5m907a3gz0sxtbhft1
parent_id: is-01kt0a89n7vxq8pc32h8htb3kx
created_at: 2026-06-01T00:45:51.023Z
updated_at: 2026-06-13T18:38:35.686Z
closed_at: 2026-06-01T01:17:44.050Z
close_reason: Implemented in Phase 1; tests pass, lint clean, end-to-end smoke test produces 48KB self-contained HTML
---
Add tools/pprose/tests/test_render_html.py with: (1) golden tests - render fixtures from tools/pprose/tests/fixtures/*.eval.md to HTML, diff against checked-in <name>.html golden files in the same fixtures dir. Follow the project's existing golden-test pattern. (2) schema-coverage test - construct an in-memory EvalReport that exercises every legal Score value (1, 2, 3, 4, 5, 'NA', 'ERR') and confirm rendering succeeds and emits the expected per-row CSS classes (e.g., .bi-dim.is-na, .bi-num-circle.err). (3) detection test - confirm detect_kind() correctly identifies a fixture .eval.md, a plain .md, and rejects a non-Markdown file with a clear error. No headless-browser PDF test.
