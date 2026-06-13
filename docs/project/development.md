# Development

## One-Time Setup

```bash
make install         # uv sync + npm install
make hooks-install   # installs lefthook git pre-commit + pre-push hooks
```

`uv` is the Python tool runner ([astral.sh/uv](https://docs.astral.sh/uv/)). Node is
required for the JS toolchain (Biome and lefthook).
Bun is **not** required.

## Daily Commands

```bash
make format       # auto-format Markdown with flowmark-rs (canonical sources)
make generate     # regenerate derivatives (design system + vendored pprose resources)
make lint         # auto-fix: format + lint Python + JS
make test         # run pprose tests
make lint-check   # CI-mode lint: read-only, fails on any drift (what CI runs)
make default      # install + format + generate + lint + test (the daily loop)
```

## Toolchain

| Language | Format | Lint | Type-check |
| --- | --- | --- | --- |
| Python | `ruff format` | `ruff check` | `basedpyright` |
| JS / CSS / HTML / JSON | `biome format` | `biome check` | — |
| Markdown | `flowmark-rs` | — | — |

Versions are pinned exactly in `tools/pprose/pyproject.toml` and `tools/pprose/uv.lock`
(Python), `package.json` and `package-lock.json` (JS), the PEP 723 header of
`tools/design-system/generate.py` (the design-system generator’s two deps), and the
`FLOWMARK` variable at the top of the `Makefile` (the Markdown formatter fetched via
`uvx`). `make install` uses `npm ci` so the JS toolchain comes from the lockfile, not a
fresh resolve. All layers follow the
[14-day package-age rule](https://github.com/jlevy/tbd/blob/main/docs/guidelines/bun-monorepo-patterns.md#supply-chain-mitigation):
no dependency upgrade lands until the published version is at least 14 days old, to give
the ecosystem time to surface supply-chain compromises.

[Biome](https://biomejs.dev) is a single binary that replaces prettier and eslint for
the JS/CSS/HTML/JSON side.
The config is `biome.json` at the repo root.

[ruff](https://docs.astral.sh/ruff/) handles both formatting and linting for Python.
The top-level `ruff.toml` covers `tools/design-system/` and mirrors the rule set in
`tools/pprose/pyproject.toml` so the pprose package and the design system stay
consistent.

[flowmark-rs](https://github.com/jlevy/flowmark) auto-formats every tracked Markdown
file in the repo (semantic line breaks, smart quotes, safe cleanups).
`make format` is the single invocation: both the Makefile and the `format-markdown`
pre-commit hook call it, so behavior is identical locally and at commit time.

Flowmark formats canonical *sources* only; *generated* and *vendored* Markdown is listed
in `.flowmarkignore` (gitignore syntax, at the repo root) so formatting flows through
the right pipeline:

| Excluded path | Why |
| --- | --- |
| `example-texts/` | Verbatim third-party corpora (IRS, NASA, SQLite). |
| `.tbd/`, `.claude/skills/tbd/`, `.codex/` | Vendored agent state, overwritten on resync. |
| `tools/pprose/src/pprose/resources/` | Synced mirrors of `docs/`, `runbooks/`, `shortcuts/`, `skills/`. Picked up via `make generate` (which runs `devtools/sync_resources.py`), not directly. |
| `tools/pprose/tests/fixtures/`, `tools/pprose/tests/test_fixtures/` | Byte-exact golden outputs and curated metric-test inputs; reformatting would break the regression locks. |

Anything already in `.gitignore` is skipped automatically.

[lefthook](https://lefthook.dev) runs format + lint on staged files at commit time and
the generator check + tests at push time.
The config is `lefthook.yml`.

## The Design System

[`tools/design-system/design-system.yaml`](tools/design-system/design-system.yaml) is
the single source of truth for surfaces, group palette, dimension palette, score ramp,
and icon mapping.

`generate.py` validates the YAML through Pydantic and emits four derivatives:

| Output | Consumer |
| --- | --- |
| `tools/design-system/_generated/design_system.js` | ES-module consumers |
| `tools/design-system/_generated/design_system.global.js` | Static HTML pages (`window.PracticalProseDesignSystem`) |
| `tools/design-system/_generated/design_system.css` | Any HTML page that wants the tokens via `<link>` |
| `tools/pprose/src/pprose/_generated/design_system.py` | The Python runtime (consumed by `table_styles.py`) |

**All four generated files are checked in.** This keeps the repo zero-build for
consumers: clone, open an HTML page, run pprose, with no `npm run build` step required.

CI verifies the checked-in copies match the YAML via `make generate-check`. The
pre-commit hook re-runs the generator when anything under `tools/design-system/` is
staged and stages the refreshed outputs alongside your edit.

## Vendored Resources in the pprose Package

The pprose wheel must work standalone in any repo, so canonical Markdown under `docs/`,
`runbooks/`, `shortcuts/`, and `skills/` is mirrored into
`tools/pprose/src/pprose/resources/` by `tools/pprose/devtools/sync_resources.py`. The
mirror is checked in and is the source of truth for runtime lookups
(`pprose guidelines`, `pprose runbook`, …).

`make generate` runs the sync as a second step (after the design-system generator).
The pre-commit `pprose-resources-sync` hook re-syncs the mirror whenever a source file
under `docs/`, `runbooks/`, `shortcuts/`, or `skills/*/SKILL.md` is staged, and the
pre-push `resources-sync-check` (plus `tools/pprose/tests/test_resources_sync.py`) fails
on any drift.

## The Pre-Commit and Pre-Push Contract

Pre-commit (per staged file):

1. **Biome** formats and fixes JS/JSON/CSS/HTML.
2. **ruff format + check --fix** formats and fixes Python.
3. **flowmark-rs** auto-formats Markdown via `make format` whenever any `*.md` file is
   staged. The run is whole-repo (not per-staged-file) so `.flowmarkignore` is honored;
   the incremental cache keeps it fast.
4. If anything under `tools/design-system/` was touched, the generator runs and any
   refreshed `*.generated.*` files are staged alongside your commit.
5. If any source under `docs/`, `runbooks/`, `shortcuts/`, or `skills/*/SKILL.md` was
   touched, `sync_resources.py` resyncs the vendored mirror under
   `tools/pprose/src/pprose/resources/` and stages it alongside your commit.

Pre-push (whole repo):

1. **`generate.py --check`**: fails if any design-system derivative is stale.
2. **`sync_resources.py --check`**: fails if any pprose resource mirror is stale.
3. **`pytest`**: fails on any regression.

Bypass with `git commit --no-verify` only for genuine emergencies (broken tooling,
etc.). Don’t ship that to a PR.

## Repository Layout

```
tools/
├── design-system/              ← production runtime (YAML → JS / CSS / Python)
├── pprose/                     ← the Python package (eval CLI + library)
├── render-components/          ← shared card/panel/toggle CSS + JS + Jinja partials
└── explorations/               ← design-only experiments (HTML + design-tool JS)
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
