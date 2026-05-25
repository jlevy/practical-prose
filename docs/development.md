# Development

## One-time setup

```bash
make install         # uv sync + npm install
make hooks-install   # installs lefthook git pre-commit + pre-push hooks
```

`uv` is the Python tool runner ([astral.sh/uv](https://docs.astral.sh/uv/)).
Node is required for the JS toolchain (Biome + lefthook).
Bun is **not** required.

## Daily commands

```bash
make generate     # regenerate design-system derivatives from the YAML
make lint         # auto-fix: format + lint Python + JS
make test         # run pprose tests
make lint-check   # CI-mode lint: read-only, fails on any drift — what CI runs
make default      # install + generate + lint + test (the daily loop)
```

## Toolchain

| Language | Format | Lint | Type-check |
| --- | --- | --- | --- |
| Python | `ruff format` | `ruff check` | `basedpyright` |
| JS / CSS / HTML / JSON | `biome format` | `biome check` | — |

Versions are pinned exactly in `tools/pprose/pyproject.toml` + `tools/pprose/uv.lock`
(Python), `package.json` + `package-lock.json` (JS), and the PEP 723 header of
`tools/design-system/generate.py` (the design-system generator's two deps).
`make install` uses `npm ci` so the JS toolchain comes from the lockfile, not a
fresh resolve. All three layers follow the
[14-day package-age rule](https://github.com/jlevy/tbd/blob/main/docs/guidelines/bun-monorepo-patterns.md#supply-chain-mitigation):
no dependency upgrade lands until the published version is at least 14 days
old, to give the ecosystem time to surface supply-chain compromises.

[Biome](https://biomejs.dev) is a single binary that replaces prettier + eslint
for the JS/CSS/HTML/JSON side.
The config is `biome.json` at the repo root.

[ruff](https://docs.astral.sh/ruff/) handles both formatting and linting for
Python.
The top-level `ruff.toml` covers `tools/design-system/` and mirrors the rule
set in `tools/pprose/pyproject.toml` so the pprose package and the design
system stay consistent.

[lefthook](https://lefthook.dev) runs format + lint on staged files at commit
time and the generator check + tests at push time.
The config is `lefthook.yml`.

## The design system

[`tools/design-system/design-system.yaml`](tools/design-system/design-system.yaml)
is the single source of truth for surfaces, group palette, dimension palette,
score ramp, and icon mapping.

`generate.py` validates the YAML through Pydantic and emits four derivatives:

| Output | Consumer |
| --- | --- |
| `tools/design-system/_generated/design_system.js` | ES-module consumers |
| `tools/design-system/_generated/design_system.global.js` | Static HTML pages (`window.PracticalProseDesignSystem`) |
| `tools/design-system/_generated/design_system.css` | Any HTML page that wants the tokens via `<link>` |
| `tools/pprose/src/pprose/_generated/design_system.py` | The Python runtime (consumed by `table_styles.py`) |

**All four generated files are checked in.**
This keeps the repo zero-build for consumers: clone, open an HTML page, run
pprose — no `npm run build` step required.

CI verifies the checked-in copies match the YAML via `make generate-check`.
The pre-commit hook re-runs the generator when anything under
`tools/design-system/` is staged and stages the refreshed outputs alongside
your edit.

## The pre-commit / pre-push contract

Pre-commit (per staged file):

1. **Biome** formats and fixes JS/JSON/CSS/HTML.
2. **ruff format + check --fix** formats and fixes Python.
3. If anything under `tools/design-system/` was touched, the generator runs
   and any refreshed `*.generated.*` files are staged alongside your commit.

Pre-push (whole repo):

1. **`generate.py --check`** — fails if any generated file is stale.
2. **`pytest`** — fails on any regression.

Bypass with `git commit --no-verify` only for genuine emergencies (broken
tooling, etc.).
Don't ship that to a PR.

## Repository layout

```
tools/
├── design-system/              ← production runtime (YAML → JS / CSS / Python)
├── pprose/                     ← the Python package (eval CLI + library)
├── explorations/               ← design-only experiments (HTML + design-tool JS)
└── docs/                       ← project docs
```
