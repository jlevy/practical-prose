# Makefile for easy development workflows.  See docs/development.md for the
# full workflow.  Convention follows simple-modern-uv:
#
#   make install      # one-time: uv sync + npm install + git hooks
#   make              # default: install + lint + test  (after `make generate`)
#   make generate     # regenerate design-system derivatives from the YAML
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
        generate generate-check \
        lint lint-check lint-py lint-py-check lint-js lint-js-check \
        test clean

default: install generate lint test

## ─────────────── Install ───────────────

install:
	cd tools/pprose && uv sync --all-extras
	npm install --silent

hooks-install: install
	npx --no-install lefthook install

## ─────────────── Generate ───────────────

# Regenerate every design-system derivative from the YAML.
generate:
	uv run --script tools/design-system/generate.py

# Verify checked-in derivatives match the YAML; fails on drift.
generate-check:
	uv run --script tools/design-system/generate.py --check

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
