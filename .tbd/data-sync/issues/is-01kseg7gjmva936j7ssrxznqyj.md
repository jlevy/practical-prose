---
type: is
id: is-01kseg7gjmva936j7ssrxznqyj
title: "CI: add GitHub Actions workflow running make lint-check"
kind: task
status: closed
priority: 1
version: 2
labels:
  - design-system
  - ci
dependencies: []
created_at: 2026-05-25T02:43:07.987Z
updated_at: 2026-06-03T06:11:22.491Z
closed_at: 2026-06-03T06:11:22.484Z
close_reason: "CI now runs lint in check-mode (devtools/lint.py --check: ruff check + format --check, no auto-fix) plus an explicit sync_resources --check step; design-system generate-check + biome ci already covered. Effectively make lint-check."
---
Add .github/workflows/check.yml that runs `make lint-check` on push and PR.  Without it, drift between the YAML and the generated derivatives can land on main unnoticed.  Should cover:
- ruff format --check + ruff check (both pprose pyproject and design-system ruff.toml)
- biome ci (JS/CSS/HTML/JSON)
- generate --check (verifies generated files match the YAML)
- pytest

Reference: tools/pprose/Makefile note 'GitHub Actions call uv directly, not this Makefile' — follow the same convention; have the workflow call uv / npx directly instead of make targets if simpler.
