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

pprose guidelines --list                           # bundled guidelines / shortcuts / runbooks
pprose shortcut shortcut-full-edit                 # print a workflow playbook the agent follows
pprose install                                     # install skills into the current repo
```

`pprose install` writes one `SKILL.md` per workflow into both `.agents/skills/` (Codex,
Gemini CLI, pi read this natively) and `.claude/skills/` (Claude Code mirror), and
maintains a marker-bounded block in `AGENTS.md`. Every generated artifact carries a
`format=fNN` stamp; re-running install is idempotent, and a newer-format artifact is
never clobbered by an older pprose.

Each generated skill bakes in a pinned, local-first invocation (`pprose` if on PATH,
else `uvx pprose@<version>`) so the same workflow commands run in any repo. Pass
`--claude` / `--codex` / `--skip-claude` / `--skip-codex` to target specific surfaces,
or `--pin <version>` to override the version baked into the bootstrap line.
Run `pprose --help` or `pprose <command> --help` for full options.

`score` requires `ANTHROPIC_API_KEY`; the package auto-loads `.env` and `.env.local`
from the current directory hierarchy and `$HOME`.

## Project docs

- Installing uv and Python: [installation.md](docs/installation.md)
- Development workflows: [development.md](docs/development.md)
- Publishing to PyPI: [publishing.md](docs/publishing.md)
