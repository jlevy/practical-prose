## Installing uv and Python

This project uses [**uv**](https://docs.astral.sh/uv/) to manage Python and
dependencies.

Install uv (macOS/Linux):

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On macOS with [Homebrew](https://brew.sh/), `brew install uv` also works.
See [uv’s install docs](https://docs.astral.sh/uv/getting-started/installation/) for
other platforms.

Then install a Python toolchain:

```shell
uv python install 3.13  # or another version
```

After publication, run Practical Prose without a project install:

```shell
uvx pprose --help
```

## Upgrading

New pprose releases can add guidelines, shortcuts, runbooks, and skills.
Skills installed in a repo by `pprose install` bake in the version that installed them
(`uvx pprose@<version>`), so a repo keeps serving that release’s bundled docs until you
upgrade and re-run install:

```shell
uvx pprose@latest install                          # zero-install
# or, with a persistent tool install:
uv tool install --upgrade pprose && pprose install
```

Re-running install is idempotent: it refreshes the generated artifacts and the version
pin they bake, and a newer-format artifact is never clobbered by an older pprose.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
