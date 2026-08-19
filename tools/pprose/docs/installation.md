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

## Choosing a Scope

Install once for yourself and the skills are available in every repo you work in:

```shell
uvx pprose install -g
```

This writes only to `~/.agents/skills/` and `~/.claude/skills/`, so it adds capability
without changing any repository.
Install into a repo instead when Practical Prose should be that repo’s committed policy;
project scope additionally writes the managed `AGENTS.md` block and `CLAUDE.md` bridge
that make the skills a standing instruction:

```shell
uvx pprose install          # project scope is the default inside a git repo
```

A project-scope skill shadows a user-scope skill of the same name, so installing both is
a supported pattern rather than a conflict.

## Upgrading

New pprose releases can add guidelines, shortcuts, runbooks, and skills.
Skills installed by `pprose install` bake in the version that installed them
(`uvx pprose@<version>`), so an installed scope keeps serving that release’s bundled
docs until you upgrade and re-run install in each scope (each project repo, and once for
`-g`):

```shell
uvx pprose@latest install                          # zero-install
# or, with a persistent tool install:
uv tool install --upgrade pprose && pprose install
```

Re-running install is idempotent and reconciles the whole scope: it refreshes every
pprose-managed artifact and the version pin it bakes, updates the managed `AGENTS.md`
and `CLAUDE.md` blocks, adds skills that are new in the release (for example,
`pprose-de-slop` in v0.3.0), and prunes deselected generated skills only when they carry
a pprose format marker.
A symlinked `AGENTS.md` or `CLAUDE.md` is written through to its target, so the
shared-entry-file pattern survives an install (fixed in v0.4.0; earlier versions
replaced the link with a regular file).
Artifact formats are stamped (`format=fNN`) and upgraded in place; a newer-format
artifact is never clobbered by an older pprose.
Skills installed with the skills CLI are refreshed the same way they were installed:
re-run `npx skills add jlevy/practical-prose[@skill]`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
