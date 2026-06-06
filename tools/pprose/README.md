# pprose

Practical Prose tooling: deterministic metrics, rubric scoring, evaluation reports, and
comparisons for practical documents.

`pprose` is the command-line companion to
[Practical Prose](https://github.com/jlevy/practical-prose), a reference system and
evaluation toolkit for writing that helps a reader understand, decide, do, verify, or
maintain something.

## Install

The distribution and command are both `pprose`. After publication, run with no install
using [uv](https://docs.astral.sh/uv/):

```bash
uvx pprose <command> ...
```

Or install it:

```bash
uv tool install pprose
```

## Commands

```bash
pprose metrics doc.md                              # deterministic metrics for a document
pprose report from-metrics doc.md --out doc.eval.md  # build an eval report stub
pprose score doc.eval.md                           # qualitative rubric scoring (Anthropic SDK)
pprose compare a.eval.md b.eval.md                 # compare N eval reports

pprose about                                       # the project narrative (bundled README)
pprose skill                                       # workflow skills overview + routing pointers
pprose guidelines --list                           # bundled style guides and writing rules
pprose shortcut --list                             # workflow playbooks the skills invoke
pprose runbook --list                              # operational procedures (eval, compare)
pprose install                                     # install skills into the current project
pprose install --global                            # install skills user-wide for every project
```

`pprose install` runs in one of two **scopes**:

- **Project** (`--project`, the default when cwd is inside a git repo) writes into
  `<repo>/.agents/skills/` (Codex, Gemini CLI, pi), `<repo>/.claude/skills/` (Claude
  Code), and a marker-bounded block in `<repo>/AGENTS.md`.
- **User-global** (`--global`) writes into `~/.agents/skills/pprose-*/` and
  `~/.claude/skills/pprose-*/`, making the skills available across every project.
  Skips `~/.codex/AGENTS.md` so the global instruction file stays user-authored.

Outside an unambiguous project context (`$HOME`, a non-git directory), `--project` or
`--global` must be passed explicitly — no silent default.
`$HOME` is always refused under `--project`; use `--global` for a user-wide install.
Pass `--surfaces=portable,claude,agents-md` (or `--surfaces=all`, the default) to select
install destinations within the chosen scope, or `--pin <version>` to override the
version baked into the bootstrap line.

Every generated artifact carries a `format=fNN` stamp; re-running install is idempotent,
and a newer-format artifact is never clobbered by an older pprose.
Each generated skill bakes in a pinned, local-first invocation (`pprose` if on PATH,
else `uvx pprose@<version>`). Cross-scope coexistence is the supported pattern:
project-scope skills shadow user-scope skills of the same name in modern agents.
Run `pprose --help` or `pprose install --help` for full options.

`score` requires `ANTHROPIC_API_KEY`; the package auto-loads `.env` and `.env.local`
from the current directory hierarchy and `$HOME`.

## Project docs

- Installing uv and Python: [installation.md](docs/installation.md)
- Development workflows: [development.md](docs/development.md)
- Publishing to PyPI: [publishing.md](docs/publishing.md)

## License

The package code is MIT licensed (the `license` field in package metadata).
The wheel also bundles practical-prose **content** (the guidelines, rubric, runbooks,
and other prose under `resources/`), which is licensed under Creative Commons
Attribution 4.0 ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)). See the
[repository LICENSE](https://github.com/jlevy/practical-prose/blob/main/LICENSE).
