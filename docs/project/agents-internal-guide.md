---
title: "Practical Prose: Agent Guide (Internal)"
description: "Repo-internal agent reference: this-repo workflows table, tooling layout, and visual-design notes. Not bundled into the pprose CLI (see /docs/ for public docs)."
author: Joshua Levy (github.com/jlevy) with LLM assistance
---
# Practical Prose: Agent Guide (Internal)

This document is **internal to the practical-prose repo**. It holds material an agent
working on *this* repo needs but that doesn’t belong in the public pprose CLI surface
(which bundles docs useful from any repo).

For the always-on root entrypoint, see [/AGENTS.md](../../AGENTS.md).
For development workflows (build, test, format, lint), see
[development.md](development.md).

Repo layout notes: planning specs live only under [specs/active/](specs/active/) and
[specs/done/](specs/done/). The gitignored `attic/` directory holds reference checkouts
of other repos (flowmark, tbd); their docs and specs belong to those projects, not to
this one.

## Workflows

| User intent | Use | Source |
| --- | --- | --- |
| Apply the common Markdown documentation standards (basic, universal) | [pprose-common-edit](../../skills/pprose-common-edit/SKILL.md) | [common-doc-guidelines.md](../common-doc-guidelines.md) |
| Copy edit for language and formatting (the Expression and Form dimensions) | [pprose-copy-edit](../../skills/pprose-copy-edit/SKILL.md) | [shortcut-copy-edit.md](../../shortcuts/shortcut-copy-edit.md) |
| Full editorial pass across all 20 dimensions + editorial review (also covers audit-only review) | [pprose-full-edit](../../skills/pprose-full-edit/SKILL.md) | [shortcut-full-edit.md](../../shortcuts/shortcut-full-edit.md) |
| Review one document and report tiered feedback (common-edit, copy-edit, and substantive layers) without editing or scoring | [pprose-review](../../skills/pprose-review/SKILL.md) | [shortcut-review.md](../../shortcuts/shortcut-review.md) |
| Score one document with metrics and rubric grading | [pprose-eval](../../skills/pprose-eval/SKILL.md) | [practical-prose-eval-single.runbook.md](../../runbooks/practical-prose-eval-single.runbook.md) |
| Compare multiple evaluated drafts or variants | [pprose-compare](../../skills/pprose-compare/SKILL.md) | [practical-prose-eval-compare.runbook.md](../../runbooks/practical-prose-eval-compare.runbook.md) |
| Regenerate this repo’s baseline eval set (example texts + self-eval docs) | (this repo) | [practical-prose-baseline-evals.runbook.md](practical-prose-baseline-evals.runbook.md) |
| Manually validate every pprose surface before a release | (this repo) | [e2e-testing.runbook.md](e2e-testing.runbook.md), [release-readiness-2026-06.md](release-readiness-2026-06.md) |

## Tooling

The Python package lives in `tools/pprose/`. The distribution and command are both
`pprose`, so after publication agents can run it in any repo with `uvx` and no prior
install:

```bash
uvx pprose <command> ...
```

**Evaluate** (action): `pprose metrics`, `pprose report`, `pprose score`,
`pprose compare`, `pprose render`.

`pprose render <doc.eval.md>` emits a clean, print-friendly static HTML page from an
eval report, a single self-contained file by default.
It is the shareable artifact for a single-doc eval.
Pair it with `pprose score <doc.md> --render-html` to score and render in one shot; the
two are composable primitives.
Open the resulting HTML in any modern browser and use the print dialog to save as PDF
(Letter by default; `--page-size a4` for A4). The page is built from a small set of
named **variants**; `pprose render --list-variants` shows what’s available, and today
only `interactive` ships (one card, two hover-driven tip panels, and a theme toggle).
See
[plan-2026-05-29-static-html-eval-report.md](specs/done/plan-2026-05-29-static-html-eval-report.md).

The card, tip panels, and theme toggle are **shared render components** at
[tools/render-components/](../../tools/render-components/): one set of CSS, JavaScript,
and Jinja partials consumed by both the explorations playground and the `pprose render`
pipeline. The CSS and JS lifted into the wheel are mirrored verbatim by
`tools/pprose/devtools/sync_render_html_styles.py`; CI fails on drift via
`tests/test_render_html.py::test_sync_render_html_styles_in_sync`. To edit how the card
or panels look, edit the component file under `tools/render-components/` and re-run the
sync script. See
[plan-2026-05-31-shared-render-components.md](specs/active/plan-2026-05-31-shared-render-components.md).

**Reference** (print bundled docs the agent follows): `pprose list` for the full
inventory; `pprose guidelines <name>`, `pprose shortcut <name>`, `pprose runbook <name>`
print one (omit the name to list that kind); `pprose skill <name>` and `pprose about`.
The guidelines, shortcuts, runbooks, and rubric are bundled in the wheel, so these work
in any repo without this source tree.

**Setup**: `pprose install` runs in one of two scopes:

- `--project` (default when cwd is inside a git repo) writes the five Practical Prose
  skills into `<repo>/.agents/skills/` (Codex, Gemini CLI, pi) and
  `<repo>/.claude/skills/` (Claude Code), plus a marker-bounded `pprose` block in
  `<repo>/AGENTS.md`.
- `--global` writes the skills into `~/.agents/skills/pprose-*/` and
  `~/.claude/skills/pprose-*/`, available across every project.
  The global AGENTS.md is left user-authored.

Outside an unambiguous project context (`$HOME`, a non-git directory), `--project` or
`--global` must be passed explicitly.
Every generated artifact carries a `format=fNN` stamp; re-running install is idempotent
and a newer-format artifact is never clobbered by an older pprose.
Each generated skill bakes in a pinned, local-first invocation: `pprose` if on PATH,
else `uvx pprose@<version>` (the version that ran install: a trusted pin, never an
unpinned runner), else they tell the user to install uv or pprose.
Pass `--surfaces=portable,claude,agents-md` to select install destinations within the
chosen scope.

For local development before publication, run from the package workspace:

```bash
cd tools/pprose
uv run pprose <command> ...
```

`score` requires `ANTHROPIC_API_KEY`; the package auto-loads `.env` and `.env.local`
from the current directory hierarchy and `$HOME`.

## Visual Design

Any work that touches palettes, eval-report rendering, or CSS should follow
[design-system.md](../../tools/design-system/design-system.md).
All color values are written in `hsl()`, not hex, so the system’s structure is visible
in the source.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
