---
title: pprose install — explicit scopes and a surfaces vocabulary
description: Redesign `pprose install` with explicit project/global scope, a flowmark-style `--surfaces` flag, and pre-write guard rails
author: Joshua Levy (github.com/jlevy) with LLM assistance
---
# Feature: `pprose install` — Explicit Scopes and a Surfaces Vocabulary

**Date:** 2026-05-30

**Author:** Joshua Levy

**Status:** Phase 1 implemented (commit 549e556, 2026-06-02: scopes, surfaces, ambiguity
checks, format stamps).
Phase 2 items have partially landed since (`pprose about` and `pprose skill` overview
shipped); remaining Phase 2 doc moves are deferred.

> [!NOTE]
> The Phase 2 listing examples below are historical design notes.
> The later
> [CLI listing plan](../done/plan-2026-06-11-cli-snappiness-color-and-listing.md)
> removed `--list`: use bare category commands such as `pprose guidelines` or the
> top-level `pprose list` for the current interface.

## Overview

Replace the current `pprose install` argument shape with a two-axis design:

1. **Scope** — `--project` (default when cwd is unambiguously inside a git repo) or
   `--global` (user-wide install under `$HOME`). Outside an unambiguous project context,
   one of the two must be explicit.
2. **Surfaces** — a single `--surfaces=<comma-list>` flag (flowmark’s pattern) replaces
   the per-agent `--claude` / `--codex` / `--skip-*` / `--no-agents-md` flag soup.

Adds pre-write guard rails so an accidental `cd ~ && pprose install` cannot silently
land pprose into the user’s global agent surfaces, and prints the resolved target before
any writes.

## Goals

- Make scope a deliberate user choice, never silently inferred when ambiguous.
- Support both project-local and user-global install as first-class modes (pprose is a
  general-purpose writing tool; both are valid).
- Replace per-agent flags with an extensible `--surfaces` vocabulary so adding a new
  agent surface in the future is a no-op for the CLI shape.
- Match the principle in cli-agent-skill-patterns §6.6 ("project and global must be kept
  separate, global must be explicit") with a concrete syntax the guideline can then
  codify.

## Non-Goals

- A `--global-agents-md` opt-in to write `~/.codex/AGENTS.md`. Deferred; users who want
  that can hand-author the block today, and we can add the flag if demand appears.
- A `pprose uninstall` command.
  Out of scope; users can remove the marker-bounded block and skill directories
  manually.
- Changing what `pprose install` writes per surface (already covered by the existing
  format-stamp, forward-compat, idempotent-reporting work on this branch).
- A separate top-level subcommand (`pprose install-global`). One command with a scope
  flag is enough.

## Background

`pprose install` currently:

- Always writes project-locally to `<cwd>/.agents/skills/` + `<cwd>/.claude/skills/` +
  `<cwd>/AGENTS.md`.
- Has per-agent flags: `--all` / `--claude` / `--codex` / `--skip-claude` /
  `--skip-codex` / `--no-agents-md`.
- Has no guard rails — `cd ~ && pprose install` silently writes into the user’s global
  agent surfaces (`~/.claude/skills/`, `~/.agents/skills/`) and global instruction file
  (`~/AGENTS.md`), changing every project’s agent behavior.

The cli-agent-skill-patterns guideline (§6.6) names the principle:

> Keep project-local setup separate from global/user setup.
> Writing `~/.codex/AGENTS.md`, `~/.agents/skills/`, or `~/.claude/skills/` should be an
> explicit global install command or documented manual step, not something
> `setup --auto` does silently.

It does not prescribe a syntax.
tbd is project-only; flowmark (Rust, current) defaults user-global; no widely-deployed
skill installer today implements explicit dual-scope with required-scope-when-ambiguous.
The git-config pattern (implicit local in a repo, error without a flag outside a repo)
is the closest mainstream analog.

flowmark’s `--surfaces=<comma-list>` is a clean, extensible replacement for per-agent
flags:

```
flowmark --install-skill --surfaces=portable,agents-md
```

Values: `portable` (`.agents/skills/<name>/`), `claude` (`.claude/skills/<name>/`),
`agents-md` (marker block in `AGENTS.md`), and `all` (default).
pprose adopts the same vocabulary.

## Design

### Argument shape

```
pprose install [SCOPE] [--surfaces=LIST] [--dir DIR] [--no-repo-check]
               [--pin VERSION] [--auto]
```

`pprose install --print` is **removed**. Use `pprose skill <name>` to preview a single
composed `SKILL.md`; for the rendered `AGENTS.md` block, install into a scratch dir
(`pprose install --project --no-repo-check --dir /tmp/preview`).

#### Scope flags

| Flag | Meaning |
| --- | --- |
| `--project` | Install project-locally |
| `--global` | Install user-globally (under `$HOME`) |
| *(neither)* | Implicit `--project` if cwd is unambiguously a project, else error |

Mutually exclusive: `--project` ↔ `--global`, and `--global` ↔ `--dir`.

#### Surfaces flag (replaces per-agent flags)

```
--surfaces=portable,claude,agents-md
--surfaces=all   # default if omitted
```

Values: `portable` (`.agents/skills/pprose-*/SKILL.md` — Codex, Gemini CLI, pi),
`claude` (`.claude/skills/pprose-*/SKILL.md` — Claude Code), `agents-md` (marker block
in `AGENTS.md`), `all` (alias for the full set).

Empty or unknown tokens produce a clear error with the valid set.

### Disambiguation rule

```
def determine_scope(args, cwd):
    if args.global and args.project:
        return error("--project and --global are mutually exclusive")
    if args.global and args.dir:
        return error("--global and --dir are mutually exclusive")

    if args.global:
        return (GLOBAL, Path.home())
    if args.project:
        return (PROJECT, _project_target(args, cwd))

    # Implicit: project iff unambiguous
    target = _project_target(args, cwd)
    if _is_protected(target):    # $HOME or filesystem root
        return error("ambiguous; pass --project or --global explicitly")
    if not _is_within_git_repo(target):
        return error(
            "ambiguous; pass --project (with --no-repo-check) or --global explicitly"
        )
    return (PROJECT, target)
```

### Per-scope guards

| Scope | `$HOME` refused? | Non-repo refused? | `--no-repo-check`? |
| --- | --- | --- | --- |
| `PROJECT` (explicit or implicit) | yes (always) | yes unless `--no-repo-check` | yes |
| `GLOBAL` | no (target IS `$HOME`) | no | n/a |

`$HOME` is refused in PROJECT even with `--no-repo-check` and explicit `--project`. If
the user actually wants to install under `$HOME`, that is what `--global` is for.

### Per-scope writes

| Surface | PROJECT mode | GLOBAL mode |
| --- | --- | --- |
| `portable` | `<target>/.agents/skills/pprose-*/SKILL.md` | `$HOME/.agents/skills/pprose-*/SKILL.md` |
| `claude` | `<target>/.claude/skills/pprose-*/SKILL.md` | `$HOME/.claude/skills/pprose-*/SKILL.md` |
| `agents-md` | `<target>/AGENTS.md` (marker block) | **disabled** — error if requested explicitly, dropped from `all` |

`agents-md` in GLOBAL is deliberately disabled.
Codex reads `~/.codex/AGENTS.md` globally (loads on every turn), and skills are
progressive-disclosure (~100 tokens listing only until invoked).
Writing a global pprose block to `~/.codex/AGENTS.md` would tax every Codex session, in
every project, for a tool the user only sometimes wants.
The `claude` and `portable` skill surfaces are enough for global discovery.

### Pre-write target message

Always printed before any filesystem writes so an interactive user can ctrl-c:

```
Installing pprose skills (project mode) into: /Users/me/myrepo
```

or
```
Installing pprose skills (user-global mode) into: /Users/me
```

### Error matrix

| Invocation | Behavior |
| --- | --- |
| `pprose install` inside git repo, not `$HOME` | implicit `--project`, install |
| `pprose install` in `$HOME` | error: “ambiguous; pass --project or --global” |
| `pprose install` in non-repo dir | error: “ambiguous; pass --project --no-repo-check or --global” |
| `pprose install --project` in repo | install |
| `pprose install --project` in non-repo | error: “not inside a git repo; pass --no-repo-check” |
| `pprose install --project --no-repo-check` in non-repo, not `$HOME` | install |
| `pprose install --project --dir $HOME` (or implicit cwd=`$HOME`) | error: “refusing $HOME in project mode; use --global” |
| `pprose install --global` (cwd anywhere) | install user-globally |
| `pprose install --global --dir X` | error: mutually exclusive |
| `pprose install --project --global` | error: mutually exclusive |
| `pprose install --global --surfaces=agents-md` | error: “agents-md is not supported in --global mode” |
| `pprose install --surfaces=bogus` | error: “unknown surface ‘bogus’; valid: portable, claude, agents-md, all” |

### Help-text outline

```
pprose install [OPTIONS]

  Install Practical Prose skills into a project (--project, default when cwd
  is unambiguously inside a git repo) or globally for the current user
  (--global). Outside an unambiguous project context, --project or --global
  must be explicit.

Scope:
  --project            Install project-locally (default when in a git repo)
  --global             Install for the current user (~/.agents + ~/.claude)
  --dir DIR            Project root for --project (default: cwd)
  --no-repo-check      Allow --project outside a git repository

Surfaces (apply within whichever scope):
  --surfaces=LIST      Comma-separated subset of surfaces to install.
                       Values: portable (.agents/skills/),
                               claude    (.claude/skills/),
                               agents-md (AGENTS.md block, project mode only),
                               all       (default if omitted).
                       Example: --surfaces=portable,agents-md

Other:
  --pin VERSION        Override the pprose version pin baked into generated
                       skills (default: installed pprose if it's a real PyPI
                       release, else DISCOVERY_VERSION).
  --auto               Non-interactive (for agents). Does not relax the
                       ambiguity check — agents must pass --project or
                       --global explicitly when context is ambiguous.
```

### `install()` library function

```python
def install(
    target_root: Path,
    surfaces: frozenset[str] = ALL_SURFACES,
    *,
    pin: str | None = None,
    allow_agents_md: bool = True,    # GLOBAL passes False
) -> list[InstallResult]: ...
```

`install_main` chooses scope, sets `target_root` and `allow_agents_md`, then calls
`install()`. `agents-md` is silently dropped when `allow_agents_md=False` so callers
don’t have to filter the surface set themselves.

### Removed flags

The following are removed in this redesign (no deprecation alias since pprose is
unreleased and the prior shape shipped only on this branch):

- `--all` → use `--surfaces=all` or omit
- `--claude` → use `--surfaces=claude`
- `--codex` → use `--surfaces=portable,agents-md`
- `--skip-claude`, `--skip-codex` → invert the `--surfaces` selection
- `--no-agents-md` → `--surfaces` without `agents-md`
- `--print` → use `pprose skill <name>` to preview one composed `SKILL.md`; for the
  rendered `AGENTS.md` block, install into a scratch dir
  (`pprose install --project --no-repo-check --dir /tmp/preview`).

### Locked decisions (was: Open Questions)

These were the open questions in the first spec draft and the resolutions adopted before
implementation:

1. **`--global --surfaces=agents-md` → error**, not silent drop.
   Explicit user intent we can’t satisfy should be told to the user, not hidden.
2. **Implicit project requires a git repo.** Non-git projects use
   `--project --no-repo-check` explicitly; no `pyproject.toml`/`AGENTS.md`/etc.
   project sniffing for v1.
3. **No `--print` mode.** Use `pprose skill <name>` for preview (already exists).
4. **Cross-scope coexistence is the expected pattern**, not a duplicate-install warning
   case. Project-scope shadows user-scope; that’s how Codex (verified via the loader’s
   scope hierarchy in the cli-agent-skill-patterns guideline) and the broader ecosystem
   (git config, PATH, npm, Python site-packages) behave.
   Document the shadowing in a one-line help epilog / README note; no warning or
   enforcement in code.
5. **Exit codes**: 0 success, 1 blocked-newer (runtime), 2 argument-shape errors
   (mutually exclusive flags, unknown surface, ambiguous scope).
6. **Pre-write target message lists the surface set** so a user can ctrl-c if the
   `--surfaces` value is wrong:
   ```
   Installing pprose skills (project mode) into: /Users/me/myrepo
     surfaces: portable, claude, agents-md
   ```
7. **`Path.home()`** for the `$HOME` refusal check; no `XDG_CONFIG_HOME` handling in v1
   (agent skill discovery paths are universally `$HOME`-rooted per §5 of the
   cli-agent-skill-patterns guideline).
8. **`--auto` does not relax the ambiguity check**, and the error message is the same
   one a human sees. Pedagogical agent-specific wording would be over-engineering.

### One namespace for “surface” (locked decision)

The earlier draft had two distinct namespaces both spelled “surface” — an
artifact-metadata tag (`surface=skill-md` / `surface=agents-md`) inside generated files,
and a CLI install selector (`--surfaces=portable,claude,agents-md`). We collapsed this
to **one namespace**: `--surfaces` is the only place those names appear.
The in-file DO-NOT-EDIT markers carry only `format=fNN`; the artifact’s type is
identified by its location (a `SKILL.md` under a skill directory, or the
BEGIN/END-bounded block inside `AGENTS.md`), not by an in-file tag.

This deletes a namespace rather than collapsing two.
Portable and Claude `SKILL.md` copies stay byte-identical (the marker no longer carries
a per-destination tag), and `compose_skill(name, pin)` doesn’t need a destination
argument. The cli-agent-skill-patterns guideline only requires `format=fNN` stamping; a
`surface=` field is optional future-proofing that pprose doesn’t need today.

## Implementation Plan

### Phase 1: Refactor `install.py`, update tests, draft guideline addition

- [x] Refactor surface vocabulary in `install.py` to flowmark’s three-name set
  (`portable`, `claude`, `agents-md`), with `ALL_INSTALL_SURFACES` and
  `parse_surfaces(raw) -> SurfaceSpec` helper that tracks whether `agents-md` was named
  explicitly.
- [x] Drop the artifact-metadata `surface=` namespace entirely (locked decision A for
  the surface-naming overlap).
  DO-NOT-EDIT markers carry only `format=fNN`.
- [x] Replace `TARGET_CLAUDE` / `TARGET_CODEX` with the surface vocabulary in
  `InstallResult`, `install()`, `_print_summary`, and `agents_md_block`.
- [x] Add `_is_within_git_repo(path)` and `_protected_target_reason(path)` helpers.
- [x] Rewrite `install_main` argparse: add `--project`, `--global`, `--surfaces`,
  `--no-repo-check`; remove `--all` / `--claude` / `--codex` / `--skip-claude` /
  `--skip-codex` / `--no-agents-md` / `--print`. Manually check mutually-exclusive
  combinations so the error path returns an exit code instead of `SystemExit`.
- [x] Print “Installing pprose skills (project|user-global mode) into: <path>” followed
  by a `surfaces: …` line before any filesystem writes.
- [x] Drop `agents-md` from the surface set in GLOBAL mode silently when `--surfaces` is
  omitted/`all`; error if the user explicitly requested `--surfaces=agents-md` in global
  mode.
- [x] Add a `git_repo_tmp(tmp_path)` fixture that creates `tmp_path/.git/`.
- [x] Add a `home_tmp(tmp_path, monkeypatch)` fixture that sets `$HOME=tmp_path`.
- [x] Rewrite `tests/test_install.py` for the full error matrix: resources/reference
  subcommands, skill composition, `parse_surfaces` parsing, scope disambiguation
  (implicit + explicit-flag conflicts), `--project` mode (in-repo, non-repo, `$HOME`
  refusal, byte-identical surfaces, idempotent, forward-compat guard, duplicate-block
  collapse, `--pin` override), `--global` mode (writes, `--surfaces=agents-md` error,
  portable-only filter), `--surfaces` filtering in project mode, pre-write target
  message, discovery-copy drift.
- [x] Drop `tests/test_install.py::test_install_print_writes_nothing` (no `--print`).
- [x] Update `tests/test_cli.py::test_top_level_help_lists_subcommands` to match the new
  top-level help (no stale `--agents-md` reference).
- [x] Update `tools/pprose/README.md` install paragraph.
- [x] Update root `AGENTS.md` install paragraph.
- [x] Update `tools/pprose/src/pprose/cli.py` command summary for `install`.
- [x] Regenerate the committed discovery copies under `skills/pprose-*/SKILL.md` via
  `devtools/sync_resources.py` so they drop the now-absent `surface=` tag.
- [x] Run `uv run ruff check src tests devtools` and `uv run pytest` clean (210 tests
  passing).
- [ ] Create tbd beads linked to this spec to record the work done.
- [ ] Draft a §6.6 / §6.7 addition for the cli-agent-skill-patterns guideline codifying
  the scope-when-ambiguous rule, the `--surfaces` vocabulary, the guard rails, and the
  cross-scope shadowing convention.
  File the proposal as a GitHub issue against `jlevy/tbd` via `gh`.
- [ ] Final commit of implementation + spec on the `pprose-skill-install-improvements`
  branch.

### Phase 2: CLI doc coverage and dogfooded `AGENTS.md` install

After landing Phase 1, the user identified two related gaps:

1. **Doc coverage**: bundled CLI docs are limited to `/docs/*.md`, `/shortcuts/*.md`,
   `/runbooks/*.runbook.md`, and the skills.
   Public-facing content useful from *any* repo — the `README.md` project narrative, the
   `tools/design-system/design-system.md` reference, and the authoring principles
   currently buried in `/AGENTS.md` — isn’t accessible via pprose.
2. **AGENTS.md handling**: pprose’s own repo had no `<!-- BEGIN PPROSE INTEGRATION -->`
   block — its `/AGENTS.md` had been hand-authored without dogfooding `pprose install`.

The corrected framing: pprose’s job is to **install a marker-bounded block into whatever
AGENTS.md a project already has**, alongside whatever other tools or hand-authored
content live there. Our own `/AGENTS.md` is not special — it gets the same block any
other project would.
There is no “drift-tested generated AGENTS.md” mode and no need for one.

The CLI bundles **public, cross-repo content only**. Repo-internal content (how to
develop pprose, this repo’s specific agent guide, internal specs) stays local and is not
exposed via the CLI — an agent in another repo has no use for “how to release pprose to
PyPI.” Two clear lines:

| CLI-bundled (public, useful in any repo) | Repo-internal (local to practical-prose) |
| --- | --- |
| Principles, guidelines, rubric, bibliography, metrics, common-doc-guidelines, ai-prose-corrections | `/docs/development.md` (how to dev the pprose tool) |
| Shortcuts, runbooks, skills | `/docs/project/` (specs, research, plans) |
| `README.md` (project narrative) | `/AGENTS.md` (this repo’s agent guide) |
| `tools/design-system/design-system.md` | New internal doc for the rich workflows table currently in `/AGENTS.md` |
| New: `practical-prose-authoring-principles.md` |  |

#### Design

1. **`pprose about`** new top-level command.
   Prints the bundled `README.md` (project narrative — what Practical Prose is and why
   it matters). One-shot command; no `--list` / subcommand.
   The natural name for the project intro.

2. **`pprose guidelines design-system`** — add `tools/design-system/design-system.md` to
   the bundled guidelines so agents working on palettes / eval-report CSS can pull it on
   demand from any repo.

3. **`pprose guidelines practical-prose-authoring-principles`** — extract the eight
   numbered authoring principles currently in `/AGENTS.md` into a new bundled doc at
   `/docs/practical-prose-authoring-principles.md` (which `sync_resources.py` already
   covers by category).
   Available from any repo via the CLI.

4. **`pprose skill` (no args) → richer overview.** Today `pprose skill` and
   `pprose skill --list` print the same terse `name\tdescription` table.
   Change:
   - `pprose skill` (no args) — short overview paragraph + the skill table + a “for more
     detail” footer routing to `pprose guidelines --list`, `pprose shortcut --list`,
     `pprose runbook --list`. Makes `pprose skill` the natural entry-point answer to
     “what does pprose do?”
   - `pprose skill --list` — keep terse listing for scripting / quick reference.
   - `pprose skill <name>` — unchanged (full composed `SKILL.md` content).

5. **Keep the `agents_md_block` minimal.** The currently-installed block already carries
   trigger keywords + routing pointers + a per-skill bullet list.
   Trim the bullet list — `pprose skill --list` covers that, and the block needs to sit
   comfortably alongside other tools’ blocks (tbd, flowmark, …) in someone else’s
   AGENTS.md. End state of the block:

   ```
   <!-- BEGIN PPROSE INTEGRATION format=f01 -->
   ## Practical Prose (pprose)

   Practical Prose: an evaluation toolkit and editorial workflows for practical
   documents. Use when the user asks to improve, audit, score, or compare
   practical documents.

   Run `pprose --help` for commands; `pprose skill --list`,
   `pprose shortcut --list`, `pprose guidelines --list`, and
   `pprose runbook --list` for on-demand workflows, playbooks, style guides,
   and procedures. Run pprose as `pprose <command>` if on PATH, else
   `uvx pprose@<pin> <command>`.

   <!-- END PPROSE INTEGRATION -->
   ```

   ~10 lines. No workflows table, no per-skill bullet list, no project intro (the host
   project owns those lines).
   Just trigger keywords + routing.

6. **Unbundle `/docs/development.md`.** It’s about how to develop the pprose tool itself
   — useless to an agent working in another repo.
   Move it to `/docs/project/development.md` so `sync_resources.py`’s non-recursive
   `/docs/*.md` glob stops picking it up.
   (Alternative: keep at `/docs/development.md` and exclude by name; less clean.)

7. **Slim `/AGENTS.md` and point it at an internal doc.** Our own `/AGENTS.md` currently
   carries content that doesn’t belong in the bundled CLI (this-repo workflows table,
   pprose tooling overview, visual design pointer) *and* isn’t strictly part of pprose’s
   marker block. Reshape it:

   - Top of file: title + brief project description + one-line pointer at the internal
     doc
     (`See \`docs/project/agents-internal-guide.md\` for the practical-prose-specific workflows table and tooling notes.`).
   - One-line pointer at `pprose guidelines practical-prose-authoring-principles` for
     the project-wide authoring principles.
   - The `<!-- BEGIN PPROSE INTEGRATION -->` block (added by dogfooding
     `pprose install --project`).
   - The existing `<!-- BEGIN TBD INTEGRATION -->` block (managed by tbd).

   The rich hand-authored content (workflows table for this repo’s specific skill
   layout, tooling overview, visual design pointer) moves to
   `/docs/project/agents-internal-guide.md` (new file, NOT bundled — lives in the same
   internal-only directory as the specs).

8. **Dogfood the install on our own repo.** Run `pprose install --project` to write the
   pprose marker block into `/AGENTS.md`. Once Phase 2’s slimmer block shape and the
   internal-doc reshuffle have landed, `/AGENTS.md` is ~15 lines: project header +
   internal pointer + principles pointer + pprose block + tbd block.

9. **Not in scope:**
   - No “generated AGENTS.md” mode.
     Pprose owns its block; the host project owns everything else.
   - No auto-generated workflows table in the block.
     The host project may have its own workflows table outside the markers (the
     internal-doc version, for this repo) — that’s project-specific content, not
     pprose’s to manage.
   - No bundling of `/docs/development.md` or `/AGENTS.md` (both repo-internal).
   - No `--global-agents-md` flag (still deferred; global skills are enough).

#### Implementation checklist

- [ ] **Bundling — additions.** Add `tools/design-system/design-system.md` to the
  `sync_resources.py` plan under the `guidelines` category.
  Add `README.md` under a new `about` category (or as a small special case in the loader
  — only one document).
- [ ] **Bundling — removal.** Move `/docs/development.md` to
  `/docs/project/development.md` (`sync_resources.py` is non-recursive over `/docs/`, so
  the move alone unbundles it).
  Update any internal links that pointed at the old path.
- [ ] **Authoring principles bundled doc.** Create
  `/docs/practical-prose-authoring-principles.md` with the eight numbered principles
  currently in `/AGENTS.md`, plus the closing “When a local rule conflicts…” paragraph.
- [ ] **Internal doc for repo-specific agent guide.** Create
  `/docs/project/agents-internal-guide.md` with the workflows table and the
  hand-authored “Tooling” / “Visual Design” sections currently in `/AGENTS.md`. Adjust
  any cross-references.
- [ ] **`pprose about` command.** Add to `cli.py` and a small command body that prints
  the bundled `README.md`. No `--list`; one-shot.
- [ ] **`pprose skill` overview mode.** Expand `skill_main` so the no-args call prints
  an overview view (short intro paragraph + the skill table + a routing footer);
  `--list` keeps the terse table; `<name>` is unchanged.
- [ ] **Slim `agents_md_block`.** Drop the per-skill bullet list.
  End state: trigger description + routing pointers (`pprose --help`, the four `--list`
  commands, the `pprose <command>` / `uvx pprose@<pin>` line).
  ~10 lines total.
- [ ] **Dogfood install.** Run `pprose install --project` against this repo to write the
  pprose marker block into `/AGENTS.md`. Slim the surrounding hand-authored content:
  replace the Authoring Principles / Workflows / Tooling / Visual Design sections with
  one-line pointers at the bundled doc
  (`pprose guidelines practical-prose-authoring-principles`) and the internal doc
  (`docs/project/agents-internal-guide.md`).
- [ ] **Regenerate discovery copies.** `devtools/sync_resources.py` re-renders the
  `/skills/pprose-*/SKILL.md` discovery copies against the slimmer block (the discovery
  copies themselves don’t carry the block — they’re standalone SKILL.md files — but the
  bundled resources sync may pick up new docs).
- [ ] **Tests.**
  - New test: `pprose about` prints bundled README content; covers a small sentinel
    string ("Practical Prose project aims to improve" or similar).
  - New test: `pprose skill` (no args) prints the overview view (a sentinel string from
    the new intro paragraph, plus all skill names).
  - New test: `pprose skill --list` is the terse table (existing behavior; keep test).
  - Update: existing `test_project_agents_md_block_carries_format_stamp` for the slimmer
    block content; drop assertions on bullet-list lines.
  - New test: `pprose guidelines design-system` resolves; bundled.
  - New test: `pprose guidelines practical-prose-authoring-principles` resolves;
    bundled.
  - New test: `pprose guidelines development` no longer resolves (development doc moved
    to `/docs/project/`, intentionally unbundled).
- [ ] **Docs updates.** `tools/pprose/README.md` mentions `pprose about` and the new
  bundled guidelines. `pprose --help` epilog mentions `pprose about` and the four
  `--list` commands.
- [ ] **Lint + tests clean.**
- [ ] **Commit** on the same `pprose-skill-install-improvements` branch with the bead
  IDs referenced.

## Testing Strategy

Existing 191-test suite is the regression baseline (currently green on this branch).

New test coverage in `tests/test_install.py`:

- **Fixtures**
  - `git_repo_tmp(tmp_path)` → creates `tmp_path/.git/` and returns `tmp_path`.
  - `home_tmp(tmp_path, monkeypatch)` → sets `$HOME=tmp_path`; returns `tmp_path`.
- **Scope disambiguation**
  - Implicit project inside a repo: no scope flag → install.
  - Implicit project outside repo: errors with “ambiguous … --no-repo-check or
    --global”.
  - Implicit project in `$HOME` (cwd or `--dir`): errors with “ambiguous … --global”.
  - `--project --global`: errors with “mutually exclusive”.
  - `--global --dir X`: errors with “mutually exclusive”.
- **Project mode**
  - `--project` in repo: install.
  - `--project` in non-repo: errors with “not inside a git repo … --no-repo-check”.
  - `--project --no-repo-check` in non-repo, not `$HOME`: install.
  - `--project --dir <home_tmp>`: errors with “refusing $HOME in project mode”.
- **Global mode**
  - `--global`: writes only `$HOME/.agents/skills/` and `$HOME/.claude/skills/`; no
    `$HOME/AGENTS.md`.
  - `--global --surfaces=portable`: writes only `$HOME/.agents/skills/`.
  - `--global --surfaces=agents-md`: errors with “agents-md is not supported in global
    mode”.
- **Surfaces flag**
  - `--surfaces=portable,claude`: drops `agents-md` write.
  - `--surfaces=all`: equivalent to default.
  - `--surfaces=` (empty): errors with valid-values message.
  - `--surfaces=bogus`: errors with valid-values message.
- **Pre-write target message**
  - Project mode prints “(project mode) into: <abspath>”.
  - Global mode prints “(user-global mode) into: <home>”.
- **Forward-compat guard** (unchanged behavior, re-verified)
  - A newer-format artifact in the global-mode target is not overwritten.

## Rollout Plan

- Land the refactor on the existing `pprose-skill-install-improvements` branch.
- The prior surface flags shipped only on this branch and only in an unreleased state;
  no deprecation aliases needed.
- Update `tools/pprose/README.md` and root `AGENTS.md` in the same commit so the
  documented commands match the new shape.
- Open a follow-up PR to the tbd guideline (`cli-agent-skill-patterns`) with the drafted
  §6.6 addition once the implementation has shaken out in practice.

## Open Questions

All locked in the “Locked decisions” section above before implementation begins.

## References

- cli-agent-skill-patterns guideline §6.6 ("Distribution & multi-agent install") and
  §6.7 ("Making the CLI available: global install vs.
  zero-install"). Run `tbd guidelines cli-agent-skill-patterns` to read.
- flowmark `--surfaces` implementation at
  [flowmark/src/flowmark/cli.py](https://github.com/jlevy/flowmark/blob/main/src/flowmark/cli.py)
  and the surface vocabulary in
  [flowmark/src/flowmark/skill.py](https://github.com/jlevy/flowmark/blob/main/src/flowmark/skill.py).
- git-config scope precedent: `git config` defaults to `--local` inside a repo and
  errors without a scope flag outside one.
- Prior commit on this branch (`7437f44`): initial multi-surface install with format
  stamps and forward-compat guard; this spec layers scope + surfaces vocabulary on top
  of that work.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
