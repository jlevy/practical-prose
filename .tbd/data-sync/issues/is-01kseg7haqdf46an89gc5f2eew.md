---
type: is
id: is-01kseg7haqdf46an89gc5f2eew
title: "lefthook: better onboarding error when .venv missing"
kind: task
status: open
priority: 3
version: 1
labels:
  - tooling
dependencies: []
created_at: 2026-05-25T02:43:08.758Z
updated_at: 2026-05-25T02:43:08.758Z
---
The ruff-format and ruff-check hooks invoke tools/pprose/.venv/bin/ruff directly.  On a fresh clone where the developer hasn't run `make install` yet, the pre-commit hook fails with a cryptic 'no such file' error.

Options:
- Wrap the command in a small shell preamble that checks for .venv and prints 'run make install' if missing.
- Or run `make install` automatically (slower, surprising).
- Or use `uvx ruff` with a pinned version (no venv needed, slower first run).
