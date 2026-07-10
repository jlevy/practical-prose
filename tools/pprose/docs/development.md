# Development

## Setting Up uv

This project is set up to use [uv](https://docs.astral.sh/uv/) to manage Python and
dependencies. First, be sure you
[have uv installed](https://docs.astral.sh/uv/getting-started/installation/).

Then
[fork the jlevy/practical-prose repo](https://github.com/jlevy/practical-prose/fork)
(having your own fork will make it easier to contribute) and
[clone it](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

## Basic Developer Workflows

The `Makefile` offers the supported `uv` workflows for local development.
Routine commands ignore personal uv configuration, reject lock drift, and use the hashed
build constraints. GitHub Actions enforce the same contract directly.

```shell
# First, install all dependencies and set up your virtual environment.
# Installs the committed runtime/development lock without re-resolving it.
make install

# Run uv sync, lint, and test:
make

# Build wheel:
make build

# Linting:
make lint

# Run tests:
make test

# Delete all the build artifacts:
make clean

# Upgrade dependencies to compatible versions:
make upgrade

# To run tests by hand without syncing:
UV_NO_CONFIG=1 UV_LOCKED=1 uv run --no-sync pytest
UV_NO_CONFIG=1 UV_LOCKED=1 uv run --no-sync pytest -s tests/test_metrics.py

# Build and install current dev executables, to let you use your dev copies
# as local tools:
uv tool install --editable .

# Dependency management directly with uv:
# After verifying the exact version clears the 14-day rule, add a dependency:
uv add 'package_name==X.Y.Z'
# Add an exact development dependency:
uv add --dev 'package_name==X.Y.Z'
# Re-lock after changing a dependency declaration. The first pass applies the
# 14-day gate; the second removes environment-specific resolver metadata while
# preserving the reviewed selections:
uv lock --no-config --exclude-newer '14 days'
uv lock --no-config
# Update one package by changing its exact declaration, then run the two passes above.
```

Review every dependency and hash change before the second pass.
See [SUPPLY-CHAIN-SECURITY.md](../../../SUPPLY-CHAIN-SECURITY.md) and the
[uv docs](https://docs.astral.sh/uv/) for details.

## IDE Setup

If you use VSCode or a fork like Cursor or Windsurf, you can install the following
extensions:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

- [Based Pyright](https://marketplace.visualstudio.com/items?itemName=detachhead.basedpyright)
  for type checking. Note that this extension works with non-Microsoft VSCode forks like
  Cursor.

## Publishing Releases

See [publishing.md](publishing.md) for instructions on publishing to PyPI.

## Documentation

- [uv docs](https://docs.astral.sh/uv/)

- [basedpyright docs](https://docs.basedpyright.com/latest/)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
