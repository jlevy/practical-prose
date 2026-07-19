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
pprose score doc.eval.md --model opus              # LLM rubric scoring (Anthropic, OpenAI, or Google)
pprose compare a.eval.md b.eval.md                 # compare N eval reports
pprose render doc.eval.md                          # render an eval report as static HTML

pprose about                                       # the project narrative (bundled README)
pprose skill                                       # workflow skills overview + routing pointers
pprose list                                        # every bundled guideline, shortcut, runbook, skill
pprose guidelines <name>                           # print one style guide (no name lists them)
pprose install --profile common-docs               # common documentation policy only
pprose install --profile practical-prose           # complete suite (also the default)
pprose install --skill pprose-de-slop               # focused, runtime-free AI-tell cleanup
pprose install --skill pprose-review               # exact selection; repeat --skill as needed
pprose install --global --profile common-docs      # user-wide skills, no instruction files
```

`pprose install` runs in one of two **scopes**:

- **Project** (`--project`, the default when cwd is inside a git repo) writes into
  `<repo>/.agents/skills/` (Codex, Gemini CLI, pi), `<repo>/.claude/skills/` (Claude
  Code), a marker-bounded block in `<repo>/AGENTS.md`, and a minimal `<repo>/CLAUDE.md`
  bridge or managed block so Claude Code sees the standing policy.
- **User-global** (`--global`) writes into `~/.agents/skills/pprose-*/` and
  `~/.claude/skills/pprose-*/`, making the skills available across every project.
  Skips `~/.codex/AGENTS.md` so the global instruction file stays user-authored.

Outside an unambiguous project context (`$HOME`, a non-git directory), `--project` or
`--global` must be passed explicitly; there is no silent default.
`$HOME` is always refused under `--project`; use `--global` for a user-wide install.
Pass `--profile=common-docs|practical-prose` to select a public skill set, or repeat
`--skill <name>` for an exact custom set.
Pass `--surfaces=portable,claude,agents-md,claude-md` (or `--surfaces=all`, the default)
to select destinations within the chosen scope, or `--pin <version>` to override the
version baked into CLI-backed skill bootstrap lines.
Changing the selection removes deselected skill directories only when they carry a
pprose-generated format marker; unmarked user content and newer-format artifacts are
preserved.

Every generated artifact carries a `format=fNN` stamp; re-running install is idempotent,
and a newer-format artifact is never clobbered by an older pprose.
CLI-backed generated skills bake in a pinned, local-first invocation (`pprose` if on
PATH, else `uvx pprose@<version>`). `pprose-common-edit` and `pprose-de-slop` instead
bundle their complete guideline references and need no runtime.
Cross-scope coexistence is the supported pattern: project-scope skills shadow user-scope
skills of the same name in modern agents.
Run `pprose --help` or `pprose install --help` for full options.

**Upgrading:** new releases can add guidelines, shortcuts, runbooks, and skills.
Because installed skills pin the version that installed them, a repo picks up additions
only after you upgrade pprose and re-run install (`uvx pprose install`, or
`uv tool upgrade pprose && pprose install`); re-running refreshes both the artifacts and
the baked version pin.

`score` requires the API key for the chosen provider (`ANTHROPIC_API_KEY`,
`OPENAI_API_KEY`, or `GOOGLE_API_KEY`); the package auto-loads `.env` and `.env.local`
from the current directory hierarchy and `$HOME`.

## Project Docs

- Installing uv and Python: [installation.md](docs/installation.md)
- Development workflows: [development.md](docs/development.md)
- Publishing to PyPI: [publishing.md](docs/publishing.md)

## License

The package code is MIT licensed (the `license` field in package metadata).
The wheel also bundles practical-prose **content** (the guidelines, rubric, runbooks,
and other prose under `resources/`), which is licensed under Creative Commons
Attribution 4.0 ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)). See the
[repository LICENSE](https://github.com/jlevy/practical-prose/blob/main/LICENSE).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
