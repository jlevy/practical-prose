# Feature: Cross-Agent Skills for Practical Prose

**Date:** 2026-05-13 (last updated 2026-05-13)

**Author:** Joshua Levy with agent assistance

**Status:** Draft

## Overview

Add a small, agent-neutral skill layer to the repo so any modern coding agent (Claude
Code, Codex CLI, Cursor, Gemini CLI, Copilot, and others adopting the Agent Skills open
standard) can pick up Practical Prose and use it for applying common documentation
guidelines, pre-publish auditing, copy-editing, single-document evaluation, and N-way
comparison.

Each skill is one of two kinds, and the distinction is called out explicitly in every
description so an agent (and a user) knows what to expect:

- **Apply** skills modify the target document (rewrite, reformat, add missing pieces).
  `prose-apply-common-guidelines` and `prose-copy-edit` are apply skills.
- **Audit / evaluate** skills are read-only.
  They inspect the document and produce findings or scores, but do not change the
  source file.
  `prose-quick-check`, `prose-eval`, and `prose-compare` are audit/evaluate skills.

The design treats the repo as the distribution: content and CLI are packaged together,
the `prose-eval` CLI is invoked as a single `uvx prose-eval ...` entry point, and
frontmatter stays within the portable Agent Skills subset so the same files work
everywhere.

## Goals

- A user can point any modern coding agent at this repo (or clone it locally) and get
  working apply-common-guidelines, quick-check, copy-edit, single-doc-eval, and
  N-way-compare workflows with no setup beyond having `uv` installed.
- The same skill files work in Claude Code, Codex CLI, Cursor, Gemini CLI, and Copilot.
- The `prose-eval` Python package publishes a single `prose-eval` console script, so a
  user or agent can run `uvx prose-eval ...` with no install step and no `--from` flag.
- Reference content (principles, guidelines, rubric, bibliography, metrics) is reused in
  place; no duplication into skill files.
- Three install paths are documented: zero-install (point an agent at the repo
  directory), symlink (works for any agent), and `/plugin marketplace add` (Claude Code
  convenience).

## Non-Goals

- A maximalist CLI-as-skill setup (no `setup --auto` wizard, no Claude hooks, no doc
  bundling inside the Python package, no context-injection commands).
  Practical Prose is stateless reference-and-eval; the maximalist pattern is not
  warranted.
- An MCP server wrapper for the CLI. This is a worthwhile follow-up but is out of scope
  for the initial cross-agent skill rollout.
- Submitting to third-party “marketplace” sites beyond the official Anthropic plugin
  directory and `buildwithclaude.com`.
- Localization of skill files; English only for now.
- Changes to the rubric, guidelines, principles, metrics, or other reference content.

## Background

Research summary: as of May 2026, the agent-extension ecosystem has converged on two
primitives: `AGENTS.md` for repo-level rules (read natively by Codex, Cursor, Gemini
CLI, Copilot, Windsurf, Amp, and others) and `SKILL.md` directories (Agent Skills open
standard, ~32 agent adopters including Claude Code).
Claude Code does not yet read `AGENTS.md` natively but supports a one-line `@AGENTS.md`
import from `CLAUDE.md` as the official shim.

The current Practical Prose surface that maps naturally to skills:

| Skill | Kind | Source content (already in repo) | CLI involvement |
| --- | --- | --- | --- |
| `prose-apply-common-guidelines` | Apply | `common-doc-guidelines.md` | None (pure content) |
| `prose-quick-check` | Audit | `shortcuts/practical-prose-quick-checklist.md` | None (pure content) |
| `prose-copy-edit` | Apply | `shortcuts/shortcut-copy-edit.md` | None (pure content) |
| `prose-eval` | Evaluate | `runbooks/practical-prose-eval-single.runbook.md` | `uvx prose-eval score …` plus `metrics` / `report` subcommands |
| `prose-compare` | Evaluate | `runbooks/practical-prose-eval-compare.runbook.md` | `uvx prose-eval compare …` |

Three skills are content-only; two shell out to the Python CLI.
The shared invocation pattern is “agent reads SKILL.md → agent reads linked reference
docs as needed → for CLI skills, agent runs `uvx prose-eval <subcommand> …`.”

`prose-apply-common-guidelines` is the lightest-weight skill: it applies the general
`common-doc-guidelines.md` (organization, structuring, writing style, formatting, and
the guideline footer) to any document.
It is not specific to practical prose and is appropriate for any markdown doc.
The other four are Practical-Prose-specific and assume the document is practical prose
(meant to help a reader understand, decide, do, verify, or maintain something).
A typical sequence on a fresh doc is `prose-apply-common-guidelines` first, then
`prose-quick-check` to audit, then `prose-copy-edit` for the editing pass, then
`prose-eval` for the rubric score.

## Design

### Approach

Single phase.
Add the agent-skill scaffolding alongside the existing content; do not move
or restructure existing reference docs.

Repository layout after the change:

```
practical-prose/
├── AGENTS.md                          # NEW: cross-agent rules + skill pointers
├── CLAUDE.md                          # NEW: one-line `@AGENTS.md` shim
├── README.md
├── LICENSE
├── .claude/
│   └── skills/                              # NEW: symlinks for Claude native discovery
│       ├── prose-apply-common-guidelines -> ../../skills/prose-apply-common-guidelines
│       ├── prose-quick-check             -> ../../skills/prose-quick-check
│       ├── prose-copy-edit               -> ../../skills/prose-copy-edit
│       ├── prose-eval                    -> ../../skills/prose-eval
│       └── prose-compare                 -> ../../skills/prose-compare
├── skills/                                  # NEW: canonical, agent-neutral
│   ├── prose-apply-common-guidelines/SKILL.md
│   ├── prose-quick-check/SKILL.md
│   ├── prose-copy-edit/SKILL.md
│   ├── prose-eval/SKILL.md
│   └── prose-compare/SKILL.md
├── shortcuts/                         # unchanged; referenced by SKILL.md
├── runbooks/                          # unchanged; referenced by SKILL.md
├── tools/
│   ├── docs/                          # unchanged; referenced by SKILL.md
│   └── prose-eval/                    # unchanged; publish to PyPI
├── evals/                             # unchanged
├── attic/                             # unchanged
└── docs/project/                      # specs and research live here
```

### Components

**`AGENTS.md` at repo root.** Short (target ≤200 lines).
Three sections:

1. **What this repo is:** one paragraph value statement; when to reach for it.
2. **Workflows:** a small table mapping user intent → skill → file path, so agents that
   don’t auto-discover skills still find them.
3. **Authoring principles (always apply):** a tight distillation of
   `shortcuts/practical-prose-agent-policy.md`, the priority list.
   This is the part that loads into every session and shapes how the agent writes.

`AGENTS.md` should **not** repeat the guidelines, rubric, or metrics in full; those
live in `docs/` and are linked from the relevant `SKILL.md` files.

**`CLAUDE.md` shim.** One line:

```markdown
@AGENTS.md
```

Per the [Claude Code memory docs][cc-mem], this imports `AGENTS.md` at session start.
When Anthropic adds native `AGENTS.md` support, this file can be deleted with no other
changes.

[cc-mem]: https://code.claude.com/docs/en/memory

**Five `SKILL.md` files under `skills/`.** Each is small (target 100-200 lines, hard
ceiling 300). Frontmatter is restricted to the portable subset:

```yaml
---
name: prose-copy-edit
description: <capability statement>. Use when the user asks to <literal trigger phrases>.
---
```

Each SKILL.md body has:

- Brief value statement (1-2 sentences).
- Required inputs (e.g., path to the document; optional label, scope class).
- Step-by-step workflow, with explicit links to the source shortcut / runbook and to any
  reference doc the agent should read first.
- For CLI skills, the exact `uvx prose-eval <subcommand> …` invocations.
- “When to use this skill” callout that mirrors the description triggers, so an agent
  reading the body still gets reinforcement on activation conditions.

The body should **not** duplicate the source shortcut or runbook content; it should
orchestrate the agent’s actions and link to those files.
The SKILL.md is a router; the existing markdown is the canonical content.

**`.claude/skills/` symlinks.** Five symlinks (one per skill) so Claude Code’s native
skill discovery picks them up without duplicating files.
The symlinks are committed; they are nice-to-have, not load-bearing. `AGENTS.md` /
`CLAUDE.md` also point at the canonical `skills/` paths so Claude works without them
too.

**Single `prose-eval` CLI entry point.** Add `src/prose_eval/cli.py` and publish one
console script:

```toml
[project.scripts]
prose-eval = "prose_eval.cli:main"
```

Use subcommands instead of separate top-level script names:

| Current script | New command |
| --- | --- |
| `prose-metrics` | `uvx prose-eval metrics ...` |
| `eval-score` | `uvx prose-eval score ...` |
| `eval-report` | `uvx prose-eval report ...` |
| `eval-compare` | `uvx prose-eval compare ...` |

This follows the modern Python CLI pattern: one package-named entry point, a dedicated
`cli.py` module, command handlers kept testable, useful `--help` output, and
automation-friendly behavior. Preserve stdout/stderr discipline, respect `CI` and
`NO_COLOR`, and support `--no-progress` anywhere progress output is introduced.
Keep the existing scripts as compatibility aliases for the first release if that lowers
rollout risk, but document only the new `uvx prose-eval ...` form in skills and README.

**PyPI publishing for `prose-eval`.** The `tools/prose-eval` package is already
structured for PyPI release via GitHub Actions (`tools/prose-eval/docs/publishing.md`
documents the flow inherited from `simple-modern-uv`). Cut a `v0.1.0` (or first
appropriate) tagged release so `uvx prose-eval score` and `uvx prose-eval compare`
work.

For local development before/after the first release, run the same entry point from the
package workspace, for example: `cd tools/prose-eval && uv run prose-eval score ...`.
The SKILL.md text can mention this local form only in a development note; the primary
workflow should stay `uvx prose-eval ...`.

**README update.** Add an “Install” section that lists the three install paths, plus a
short “Skills” section that surfaces the five skill names with their one-line
descriptions, linking to each SKILL.md.
The existing “Tooling” section stays; cross-link it from the Skills section.

### Skill descriptions (proposed)

Each description leads with the **kind** (apply or audit / evaluate) so the agent and
the user both know whether running the skill will modify the source document.

| Skill | Proposed description |
| --- | --- |
| `prose-apply-common-guidelines` | Apply the common documentation guidelines to a markdown document (organization, structuring, writing style, formatting, and the required guideline footer). Modifies the doc. Use when the user asks to tidy, clean up, conform, fix formatting, add the footer, or apply common doc guidelines to a doc. |
| `prose-quick-check` | Audit a document against the Practical Prose pre-publish checklist (18 quality dimensions). Read-only: produces a findings list without modifying the doc. Use when the user asks to audit, review, self-audit, quality-check, or pre-publish-check a doc. |
| `prose-copy-edit` | Copy-edit a markdown document against the Practical Prose guidelines. Modifies the doc. Use when the user asks to copy edit, proofread, polish, tighten, line edit, rewrite, or style-edit a doc. |
| `prose-eval` | Score a single document against the Practical Prose rubric using deterministic metrics plus rubric-based grading. Read-only on the source doc; writes an eval report. Use when the user asks to score, evaluate, grade, rubric-check, or measure quality of a doc. |
| `prose-compare` | Compare N versions or variants of a document side-by-side using rubric scores and deterministic metrics. Read-only on the source docs; writes a comparison report. Use when the user asks to compare versions, A/B drafts, diff two docs by quality, or pick the best of several variants. |

These should be refined during implementation by trial in both Claude Code and Codex;
descriptions are the highest-leverage authoring decision and worth iterating on once
the bodies exist.

Avoid overlap in trigger phrasings.
"Clean up" is ambiguous between apply-common-guidelines (light, formatting) and
copy-edit (heavier rewrite); the descriptions resolve it by reserving "clean up,
tidy, fix formatting" for the apply-common-guidelines skill and "polish, rewrite,
tighten" for copy-edit.
"Review" / "audit" are reserved for quick-check.

### API Changes

Add one public `prose-eval` console script with subcommands.
The intended public interface is:

```shell
uvx prose-eval metrics ...
uvx prose-eval score ...
uvx prose-eval report ...
uvx prose-eval compare ...
```

Keep the existing top-level scripts (`prose-metrics`, `eval-score`, `eval-report`,
`eval-compare`) as compatibility aliases for now unless implementation proves that doing
so creates avoidable maintenance cost.
No reference-doc schema changes.

### File and function design

This implementation must stay aligned with the repo-as-skill research findings:
portable skill frontmatter only, short router-style `SKILL.md` bodies, progressive
disclosure into existing docs/runbooks, no setup wizard, no hooks, no docs bundled into
the CLI package, and a clean `uvx prose-eval ...` command surface.

**CLI files and functions:**

- **`tools/prose-eval/src/prose_eval/cli.py`** (new): package-named command entry point.
  - `COMMANDS: dict[str, CommandSpec]`: maps `metrics`, `score`, `report`, and
    `compare` to their dispatcher functions and short help text.
  - `main(argv: list[str] | None = None) -> int`: parses the first subcommand, prints
    top-level help for `-h` / `--help`, and delegates the remaining args to the existing
    implementation module.
  - `_run_with_prog(command: str, func: Callable[[list[str] | None], int], args:
    list[str]) -> int`: temporarily sets `sys.argv[0]` to `prose-eval <command>` so
    each delegated `argparse` help page is self-documenting.
- **`tools/prose-eval/src/prose_eval/metrics.py`**: change `main() -> int` to
  `main(argv: list[str] | None = None) -> int` and pass `argv` to
  `parser.parse_args(argv)`, matching `eval_score.py`, `eval_report.py`, and
  `eval_compare.py`.
- **`tools/prose-eval/pyproject.toml`**: add
  `prose-eval = "prose_eval.cli:main"` under `[project.scripts]`; keep
  `prose-metrics`, `eval-score`, `eval-report`, and `eval-compare` as compatibility
  aliases for the first release.
- **`tools/prose-eval/tests/test_cli.py`** (new): test the new entry point without
  network access.
  - `test_top_level_help_lists_subcommands`
  - `test_subcommand_help_uses_prose_eval_command_name`
  - `test_metrics_subcommand_matches_compatibility_script`
  - `test_report_subcommand_dispatches_validate`
  - `test_unknown_subcommand_exits_validation_error`

**Agent-facing files:**

- **`AGENTS.md`** (new): always-on cross-agent guide with one short value statement,
  a workflow-to-skill table, and condensed authoring rules. It must not duplicate the
  full rubric, guidelines, or runbooks.
- **`CLAUDE.md`** (new): one line, `@AGENTS.md`, matching the Claude Code memory
  workaround recommended in the research.
- **`skills/prose-apply-common-guidelines/SKILL.md`** (new): apply skill wrapping
  `docs/common-doc-guidelines.md`; modifies the target doc.
- **`skills/prose-quick-check/SKILL.md`** (new): read-only audit skill wrapping
  `shortcuts/practical-prose-quick-checklist.md`.
- **`skills/prose-copy-edit/SKILL.md`** (new): apply skill wrapping
  `shortcuts/shortcut-copy-edit.md`; modifies the target doc.
- **`skills/prose-eval/SKILL.md`** (new): read-only-on-source evaluation skill wrapping
  `runbooks/practical-prose-eval-single.runbook.md` and documenting
  `uvx prose-eval metrics`, `uvx prose-eval report`, and `uvx prose-eval score`.
- **`skills/prose-compare/SKILL.md`** (new): read-only comparison skill wrapping
  `runbooks/practical-prose-eval-compare.runbook.md` and documenting
  `uvx prose-eval compare`.
- **`.claude/skills/<name>`** (new symlinks): relative symlinks from Claude Code’s
  native skill-discovery directory to the canonical `skills/<name>` directories.
  Because `.claude/` is otherwise local agent state, update `.gitignore` with a narrow
  exception that tracks `.claude/skills/` while leaving hooks/settings ignored.
- **`README.md`**: add install paths and a short Skills section; document only
  `uvx prose-eval ...` for user-facing CLI flows.

**Skill authoring constraints:**

- Frontmatter uses only `name` and `description`; no `allowed-tools`, `paths`,
  arguments, hooks, model, or other agent-specific fields.
- Each description leads with the capability and ends with literal trigger phrases.
  Keep descriptions short enough for large skill collections.
- Each `SKILL.md` is a router, not a duplicate reference doc. Target 100-200 lines and
  stay under 300 unless a concrete workflow requires more.
- Reference chains stay shallow: `SKILL.md` links directly to source docs/runbooks.
- Apply skills state clearly that they modify source files; audit/evaluate skills state
  clearly that they are read-only on source files.

## Implementation Plan

### Phase 1

- [ ] Draft `AGENTS.md` at repo root.
  Condense `shortcuts/practical-prose-agent-policy.md` into the principles section; add
  the workflows table; add the one-paragraph value statement.
- [ ] Add `CLAUDE.md` containing `@AGENTS.md`.
- [ ] Add the single CLI entry point in `tools/prose-eval`:
  - [ ] Add `src/prose_eval/cli.py` with `metrics`, `score`, `report`, and `compare`
    subcommands delegating to the existing command implementations.
  - [ ] Add `prose-eval = "prose_eval.cli:main"` to `pyproject.toml`.
  - [ ] Preserve the existing console scripts as compatibility aliases unless there is a
    concrete reason to remove them before the first release.
  - [ ] Ensure `uvx prose-eval --help` and each subcommand `--help` are useful to a
    human and to an agent.
- [ ] Create `skills/prose-apply-common-guidelines/SKILL.md`: wraps
  `common-doc-guidelines.md`; instructs the agent to apply the guidelines and ensure
  the required footer is present.
- [ ] Create `skills/prose-quick-check/SKILL.md`: wraps
  `shortcuts/practical-prose-quick-checklist.md`; read-only audit producing a findings
  list.
- [ ] Create `skills/prose-copy-edit/SKILL.md`: wraps
  `shortcuts/shortcut-copy-edit.md`; modifies the doc.
- [ ] Create `skills/prose-eval/SKILL.md`: wraps
  `runbooks/practical-prose-eval-single.runbook.md`; documents
  `uvx prose-eval score`, `uvx prose-eval metrics`, and `uvx prose-eval report`
  invocations.
- [ ] Create `skills/prose-compare/SKILL.md`: wraps
  `runbooks/practical-prose-eval-compare.runbook.md`; documents
  `uvx prose-eval compare` for the multi-input invocation.
- [ ] Add `.claude/skills/<name>` symlinks for all five skills.
- [ ] Cut a first PyPI release of `prose-eval` so `uvx prose-eval ...` resolves.
  (If the package name is taken, pick an alternative whose package name and console
  script still match, so `uvx <name> ...` stays clean.)
- [ ] Update README with the “Install” section (three paths) and a “Skills” section
  surfacing the five skill names with one-line descriptions and links.
- [ ] Manual test pass in Claude Code: verify each skill triggers from its intended user
  phrasings, runs end-to-end on a small sample doc in `evals/` or `attic/`, and produces
  the expected outputs.
- [ ] Manual test pass in Codex CLI: same verification.
- [ ] Iterate on skill descriptions if triggering is unreliable.
  The bar is each skill activating from at least three distinct natural-language
  phrasings on each tested agent.

## Testing Strategy

This is mostly content-and-glue, but the new CLI entry point needs automated coverage.
Keep the skill activation checks manual and add focused CLI tests for the command
surface.

For `tools/prose-eval`, add tests that verify:

1. `prose-eval --help` lists `metrics`, `score`, `report`, and `compare`.
2. Each subcommand help page exits 0 and names the underlying workflow clearly.
3. `uv run prose-eval <subcommand> ...` dispatches to the same implementation as the
   existing compatibility script for a small fixture.
4. Output behavior stays agent-friendly: data goes to stdout, errors to stderr, and no
   progress UI appears in non-TTY or `CI` contexts.

Per skill, in each target agent (Claude Code and Codex CLI at minimum), verify:

1. **Activation.** A user phrasing that matches the description ("copy edit this",
   “score this doc”, etc.)
   causes the agent to load the SKILL.md.
   Test at least three distinct phrasings per skill.
2. **End-to-end run.** The agent follows the SKILL.md, reads the referenced source
   content, and produces the expected output (rewritten doc, checklist results, eval
   report YAML, comparison table).
3. **Cross-link integrity.** Every link in the SKILL.md resolves; every referenced
   `uvx prose-eval …` invocation runs cleanly.

Sample input docs for the runs can be drawn from `attic/` or any existing markdown in
the repo.
The objective is the workflow firing, not benchmarking output quality; quality
is the job of the rubric itself.

If the manual passes surface deeper CLI behavior bugs, file separate issues rather than
expanding this rollout beyond the entry-point cleanup.

## Rollout Plan

The change is additive and reversible.
Suggested rollout sequence:

1. Land all the new files in a single PR. The PR description points at this spec.
2. After merge, dogfood for a week or two on real editing work in this repo and one or
   two other repos that pull Practical Prose in.
3. Once descriptions and bodies feel stable, **optionally**: submit to
   [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official)
   `external_plugins/` and list on [`buildwithclaude.com`](https://buildwithclaude.com).
   Skip the third-party aggregator sites (`tonsofskills.com`, `claudemarketplaces.com`).

Rollback is `git revert` of the PR; no migrations, no external state.

## Open Questions

- **AGENTS.md scope.** How much of `practical-prose-agent-policy.md` belongs in
  `AGENTS.md` directly versus staying in the policy file and being referenced?
  The trade-off is context-budget cost (AGENTS.md is always loaded) vs.
  always-on guidance. Working assumption: condense the eight-priority list into
  AGENTS.md; leave the guidelines / rubric / principles in `docs/` and link to them.
- **PyPI package and command name.** `prose-eval` is unclaimed on PyPI as of this
  writing (verified 2026-05-13). Reserve and publish, or pick a more specific name
  (e.g., `practical-prose-eval`) if there’s a risk of collision with adjacent tools?
  Working assumption: claim `prose-eval` and publish a matching `prose-eval` console
  script so `uvx prose-eval ...` stays clean.
- **MCP wrapper.** Defer to a follow-up spec, but worth a one-line note in the README
  ("future: MCP server for non-coding-agent clients") so the path is signposted.
- **Whether to ship a per-skill `references/` subdirectory** under each skill, or rely
  entirely on links into the existing `docs/` / `shortcuts/` / `runbooks/` layout.
  Working assumption: link into existing files, no duplication.
  Reconsider only if specific runs need an intermediate “skill-shaped” reference.
- **Skill description wording.** The proposed descriptions above are a first draft;
  expect to iterate them during manual testing.
- **Whether a “quick fix” middle-ground skill is needed.** The current split is
  read-only audit (`prose-quick-check`) vs. full edit pass (`prose-copy-edit`), with
  `prose-apply-common-guidelines` as a separate, narrower apply.
  If users routinely ask for "a quick cleanup" expecting modifications but lighter
  than copy-edit, consider a third apply skill (`prose-quick-fix` or similar) that
  applies just the obvious fixes from the quick-checklist.
  Hold for now; revisit after dogfooding.

## References

- [shortcuts/practical-prose-agent-policy.md](../../../../../shortcuts/practical-prose-agent-policy.md):
  source for the AGENTS.md principles section.
- [common-doc-guidelines.md](../../../../../docs/common-doc-guidelines.md): source for the
  `prose-apply-common-guidelines` skill.
- [shortcuts/shortcut-copy-edit.md](../../../../../shortcuts/shortcut-copy-edit.md): source
  for the `prose-copy-edit` skill.
- [shortcuts/practical-prose-quick-checklist.md](../../../../../shortcuts/practical-prose-quick-checklist.md):
  source for the `prose-quick-check` skill.
- [runbooks/practical-prose-eval-single.runbook.md](../../../../../runbooks/practical-prose-eval-single.runbook.md):
  source for the `prose-eval` skill.
- [runbooks/practical-prose-eval-compare.runbook.md](../../../../../runbooks/practical-prose-eval-compare.runbook.md):
  source for the `prose-compare` skill.
- [tools/prose-eval/docs/publishing.md](../../../../../tools/prose-eval/docs/publishing.md):
  PyPI publishing flow for the CLI.
- [Agent Skills open standard](https://agentskills.io/home) and
  [AGENTS.md spec](https://agents.md/).
- [Claude Code memory docs](https://code.claude.com/docs/en/memory) (AGENTS.md import).

<!-- This document follows common-doc-guidelines.md.
Review guidelines before editing.
-->
