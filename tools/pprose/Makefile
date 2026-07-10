# Makefile for easy development workflows.
# See docs/development.md for docs.
# Note GitHub Actions call uv directly, not this Makefile.

.DEFAULT_GOAL := default

.PHONY: default install lint test upgrade build clean

UV := env UV_NO_CONFIG=1 UV_LOCKED=1 \
      UV_BUILD_CONSTRAINT=$(CURDIR)/build-constraints.txt uv

default: install lint test

install:
	$(UV) sync --all-extras

lint:
	$(UV) run --no-sync python devtools/lint.py

test:
	$(UV) run --no-sync pytest

upgrade:
	uv lock --no-config --upgrade --exclude-newer '14 days'
	uv lock --no-config
	$(UV) sync --all-extras

build:
	$(UV) build --no-config --build-constraint build-constraints.txt --require-hashes --clear

clean:
	-rm -rf dist/
	-rm -rf *.egg-info/
	-rm -rf .pytest_cache/
	-rm -rf .mypy_cache/
	-rm -rf .venv/
	-find . -type d -name "__pycache__" -exec rm -rf {} +
