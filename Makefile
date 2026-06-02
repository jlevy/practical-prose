# Makefile for easy development workflows.  See docs/development.md for the
# full workflow.  Convention follows simple-modern-uv:
#
#   make install      # one-time: uv sync + npm install + git hooks
#   make              # default: install + format + generate + lint + test
#   make generate     # regenerate derivatives (design system + pprose resources)
#   make format       # auto-format Markdown with flowmark-rs (pinned)
#   make lint         # auto-fix: format + lint Python + JS, refresh generated
#   make lint-check   # CI-mode lint: read-only, fails on any drift
#   make test         # run pprose tests
#   make clean        # remove build artifacts and node_modules
#
# Source of truth: tools/design-system/design-system.yaml.
# Edit it, then `make generate` to refresh the four derivatives:
#   tools/design-system/_generated/design_system.js
#   tools/design-system/_generated/design_system.global.js
#   tools/design-system/_generated/design_system.css
#   tools/pprose/src/pprose/_generated/design_system.py
#
# Generated files ARE checked in (consumers work after a clean clone with no
# build step).  `make lint-check` verifies they're up-to-date.
#
# Note GitHub Actions call uv / npx directly, not this Makefile.

SHELL := /bin/bash

# Ruff lives in the pprose venv (tools/pprose declares it as a dev dep).
# Wrap it so the top-level lint targets can use it on files outside that tree.
RUFF := cd tools/pprose && uv run ruff
ROOT := $(CURDIR)

.DEFAULT_GOAL := default
.PHONY: default install hooks-install \
        generate generate-check format \
        lint lint-check lint-py lint-py-check lint-js lint-js-check \
        test clean

# Pinned for security/stability — bump deliberately, honoring the 14-day rule.
#
# Supply-chain exception (see SUPPLY-CHAIN-SECURITY.md): flowmark-rs is a
# first-party package (github.com/jlevy/flowmark) maintained by this repo's
# author, so we pin a version still inside the 14-day cool-off. The override is
# surgical and per-invocation — it never relaxes the global cool-off — and
# scoped to this one package via --exclude-newer-package. Reviewed-by: Joshua Levy.
#   flowmark-rs@0.3.1 published 2026-05-30; cutoff 2026-06-02 admits it.
FLOWMARK_VERSION := 0.3.1
FLOWMARK := uvx --exclude-newer-package 'flowmark-rs=2026-06-02' flowmark-rs@$(FLOWMARK_VERSION)

# Order matters: format the canonical sources first, then `generate` syncs the
# vendored mirrors and design-system derivatives off those formatted sources.
default: install format generate lint test

## ─────────────── Install ───────────────

install:
	cd tools/pprose && uv sync --all-extras
	npm ci --silent

hooks-install: install
	npx --no-install lefthook install

## ─────────────── Generate ───────────────

# Regenerate every derivative the repo carries:
#   1. design-system derivatives (JS / CSS / Python) from the YAML
#   2. pprose package resource mirrors (vendored copies of docs/,
#      runbooks/, shortcuts/, skills/) from their canonical sources
# Both are checked in; consumers should not need a build step.
generate:
	uv run --script tools/design-system/generate.py
	cd tools/pprose && uv run python devtools/sync_resources.py

# Verify checked-in derivatives match their sources; fails on any drift.
generate-check:
	uv run --script tools/design-system/generate.py --check
	cd tools/pprose && uv run python devtools/sync_resources.py --check

## ─────────────── Format (Markdown) ───────────────

# Auto-format all Markdown with flowmark-rs (semantic line breaks, smart
# quotes, safe cleanups). Pass `.` as the sole target so flowmark traverses
# the repo and honors .flowmarkignore + .gitignore. Flowmark-rs only reads
# .flowmarkignore relative to its target arg, so passing subdirs or globs
# bypasses it.
#
# INVARIANT: lefthook's `format-markdown` pre-commit hook delegates to this
# target. There must be exactly one flowmark invocation across the repo —
# do not add per-directory variants or pass {staged_files} to flowmark
# (that bypasses .flowmarkignore).
format:
	$(FLOWMARK) --auto .

## ─────────────── Lint (auto-fix) ───────────────

# Format + lint everything, auto-fixing what can be fixed.
# (`make` and `make default` run `generate` first; running `make lint` alone
# skips generation — use `make generate lint` if you want both.)
lint: lint-py lint-js

lint-py:
	$(RUFF) format $(ROOT)/tools/design-system
	$(RUFF) check --fix $(ROOT)/tools/design-system
	$(RUFF) format src tests devtools
	$(RUFF) check --fix src tests devtools

lint-js:
	npx --no-install @biomejs/biome check --write .

## ─────────────── Lint (check-only, CI mode) ───────────────

lint-check: generate-check lint-py-check lint-js-check

lint-py-check:
	$(RUFF) format --check $(ROOT)/tools/design-system
	$(RUFF) check $(ROOT)/tools/design-system
	$(RUFF) format --check src tests devtools
	$(RUFF) check src tests devtools

lint-js-check:
	npx --no-install @biomejs/biome ci .

## ─────────────── Test ───────────────

test:
	cd tools/pprose && uv run pytest

## ─────────────── Clean ───────────────

clean:
	cd tools/pprose && $(MAKE) clean
	-rm -rf node_modules
	-find . -type d -name "__pycache__" -prune -exec rm -rf {} +
