# Practical Prose: Agent Guide

Practical Prose is a reference system and evaluation toolkit for writing that helps a
reader understand, decide, do, verify, or maintain something.
Use it when the user asks to improve, audit, score, or compare practical documents.

Keep this file short.
Load the skill or source document for the specific workflow rather than copying the full
guidelines into every context.

## Workflows

| User intent | Use | Source |
| --- | --- | --- |
| Apply the common Markdown documentation standards (basic, universal) | [pprose-common-edit](skills/pprose-common-edit/SKILL.md) | [common-doc-guidelines.md](docs/common-doc-guidelines.md) |
| Copy edit for language and formatting (the Expression and Form dimensions) | [pprose-copy-edit](skills/pprose-copy-edit/SKILL.md) | [shortcut-copy-edit.md](shortcuts/shortcut-copy-edit.md) |
| Full editorial pass across all 20 dimensions + editorial review (also covers audit-only review) | [pprose-full-edit](skills/pprose-full-edit/SKILL.md) | [shortcut-full-edit.md](shortcuts/shortcut-full-edit.md) |
| Score one document with metrics and rubric grading | [pprose-eval](skills/pprose-eval/SKILL.md) | [practical-prose-eval-single.runbook.md](runbooks/practical-prose-eval-single.runbook.md) |
| Compare multiple evaluated drafts or variants | [pprose-compare](skills/pprose-compare/SKILL.md) | [practical-prose-eval-compare.runbook.md](runbooks/practical-prose-eval-compare.runbook.md) |

## Authoring Principles

When generating, summarizing, or rewriting practical prose:

1. Answer the reader’s task and make the main output recoverable from a skim.
2. State scope and claim boundaries early.
3. Keep evidence, inference, and recommendation distinct.
4. Make material claims traceable to sources, calculations, or explicit assumptions.
5. Use concrete language and the most specific terms the reader can parse.
6. Cut visible rigor that does not improve inspectability, accuracy, usefulness, or
   reader trust.
7. Apply fairness and robustness only when the task involves disputed or interpretive
   claims.
8. Mark unknowns instead of inventing support.

When a local rule conflicts with the reader outcome, document the justified deviation:
which rule is set aside, what reader outcome it serves, and what risk it introduces.

## Tooling

The Python package lives in `tools/pprose/`. The distribution and command are both
`pprose`, so after publication agents can run it in any repo with `uvx` and no prior
install:

```bash
uvx pprose <command> ...
```

**Evaluate** (action): `pprose metrics`, `pprose report`, `pprose score`,
`pprose compare`.

**Reference** (print bundled docs the agent follows; `--list` to enumerate):
`pprose guidelines <name>`, `pprose shortcut <name>`, `pprose runbook <name>`,
`pprose skill <name>`. The guidelines, shortcuts, runbooks, and rubric are bundled in
the wheel, so these work in any repo without this source tree.

**Setup**: `pprose install` runs in one of two scopes:

- `--project` (default when cwd is inside a git repo) writes the five Practical Prose
  skills into `<repo>/.agents/skills/` (Codex, Gemini CLI, pi) and
  `<repo>/.claude/skills/` (Claude Code), plus a marker-bounded `pprose` block in
  `<repo>/AGENTS.md`.
- `--global` writes the skills into `~/.agents/skills/pprose-*/` and
  `~/.claude/skills/pprose-*/`, available across every project. The global
  AGENTS.md is left user-authored.

Outside an unambiguous project context (`$HOME`, a non-git directory), `--project`
or `--global` must be passed explicitly. Every generated artifact carries a
`format=fNN` stamp; re-running install is idempotent and a newer-format artifact is
never clobbered by an older pprose. Each generated skill bakes in a pinned,
local-first invocation: `pprose` if on PATH, else `uvx pprose@<version>` (the
version that ran install — a trusted pin, never an unpinned runner), else they tell
the user to install uv or pprose. Pass `--surfaces=portable,claude,agents-md` to
select install destinations within the chosen scope.

For local development before publication, run from the package workspace:

```bash
cd tools/pprose
uv run pprose <command> ...
```

`score` requires `ANTHROPIC_API_KEY`; the package auto-loads `.env` and `.env.local`
from the current directory hierarchy and `$HOME`.

## Visual Design

Any work that touches palettes, eval-report rendering, or CSS should follow
[design-system.md](tools/design-system/design-system.md).
All color values are written in `hsl()`, not hex, so the system’s structure is visible
in the source.

<!-- BEGIN TBD INTEGRATION format=f04 surface=agents-md -->
## tbd

This repository uses **tbd** for git-native issue tracking (beads), spec-driven
planning, and on-demand engineering guidelines.
As the agent, you operate tbd on the user’s behalf — translate their requests into tbd
actions rather than telling them to run commands.

- Run `tbd prime` to load current project state and the full tbd workflow.
- Run `tbd skill` for the complete reusable tbd skill instructions.
- Run `tbd shortcut --list` and `tbd guidelines --list` for on-demand resources.
- Track all work as beads: `tbd create`, `tbd ready`, `tbd close`, and `tbd sync`.

<!-- END TBD INTEGRATION -->
