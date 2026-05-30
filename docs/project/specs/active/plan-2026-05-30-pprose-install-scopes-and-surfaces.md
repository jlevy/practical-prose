---
title: pprose install — explicit scopes and a surfaces vocabulary
description: Redesign `pprose install` with explicit project/global scope, a flowmark-style `--surfaces` flag, and pre-write guard rails
author: Joshua Levy (github.com/jlevy) with LLM assistance
---
# Feature: `pprose install` — Explicit Scopes and a Surfaces Vocabulary

**Date:** 2026-05-30

**Author:** Joshua Levy

**Status:** Draft

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
| `pprose install --surfaces=bogus` | error: “unknown surface 'bogus'; valid: portable, claude, agents-md, all” |

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

These were the open questions in the first spec draft and the resolutions adopted
before implementation:

1. **`--global --surfaces=agents-md` → error**, not silent drop. Explicit user
   intent we can't satisfy should be told to the user, not hidden.
2. **Implicit project requires a git repo.** Non-git projects use
   `--project --no-repo-check` explicitly; no `pyproject.toml`/`AGENTS.md`/etc.
   project sniffing for v1.
3. **No `--print` mode.** Use `pprose skill <name>` for preview (already exists).
4. **Cross-scope coexistence is the expected pattern**, not a duplicate-install
   warning case. Project-scope shadows user-scope; that's how Codex (verified via
   the loader's scope hierarchy in the cli-agent-skill-patterns guideline) and the
   broader ecosystem (git config, PATH, npm, Python site-packages) behave. Document
   the shadowing in a one-line help epilog / README note; no warning or enforcement
   in code.
5. **Exit codes**: 0 success, 1 blocked-newer (runtime), 2 argument-shape errors
   (mutually exclusive flags, unknown surface, ambiguous scope).
6. **Pre-write target message lists the surface set** so a user can ctrl-c if the
   `--surfaces` value is wrong:
   ```
   Installing pprose skills (project mode) into: /Users/me/myrepo
     surfaces: portable, claude, agents-md
   ```
7. **`Path.home()`** for the `$HOME` refusal check; no `XDG_CONFIG_HOME` handling
   in v1 (agent skill discovery paths are universally `$HOME`-rooted per §5 of the
   cli-agent-skill-patterns guideline).
8. **`--auto` does not relax the ambiguity check**, and the error message is the
   same one a human sees. Pedagogical agent-specific wording would be
   over-engineering.

### One namespace for "surface" (locked decision)

The earlier draft had two distinct namespaces both spelled "surface" — an
artifact-metadata tag (`surface=skill-md` / `surface=agents-md`) inside generated
files, and a CLI install selector (`--surfaces=portable,claude,agents-md`). We
collapsed this to **one namespace**: `--surfaces` is the only place those names
appear. The in-file DO-NOT-EDIT markers carry only `format=fNN`; the artifact's
type is identified by its location (a `SKILL.md` under a skill directory, or the
BEGIN/END-bounded block inside `AGENTS.md`), not by an in-file tag.

This deletes a namespace rather than collapsing two. Portable and Claude
`SKILL.md` copies stay byte-identical (the marker no longer carries a
per-destination tag), and `compose_skill(name, pin)` doesn't need a destination
argument. The cli-agent-skill-patterns guideline only requires `format=fNN`
stamping; a `surface=` field is optional future-proofing that pprose doesn't need
today.

## Implementation Plan

### Phase 1: Refactor `install.py`, update tests, draft guideline addition

- [x] Refactor surface vocabulary in `install.py` to flowmark’s three-name set
  (`portable`, `claude`, `agents-md`), with `ALL_INSTALL_SURFACES` and
  `parse_surfaces(raw) -> SurfaceSpec` helper that tracks whether `agents-md` was
  named explicitly.
- [x] Drop the artifact-metadata `surface=` namespace entirely (locked decision A
  for the surface-naming overlap). DO-NOT-EDIT markers carry only `format=fNN`.
- [x] Replace `TARGET_CLAUDE` / `TARGET_CODEX` with the surface vocabulary in
  `InstallResult`, `install()`, `_print_summary`, and `agents_md_block`.
- [x] Add `_is_within_git_repo(path)` and `_protected_target_reason(path)` helpers.
- [x] Rewrite `install_main` argparse: add `--project`, `--global`, `--surfaces`,
  `--no-repo-check`; remove `--all` / `--claude` / `--codex` / `--skip-claude` /
  `--skip-codex` / `--no-agents-md` / `--print`. Manually check mutually-exclusive
  combinations so the error path returns an exit code instead of `SystemExit`.
- [x] Print “Installing pprose skills (project|user-global mode) into: <path>”
  followed by a `surfaces: …` line before any filesystem writes.
- [x] Drop `agents-md` from the surface set in GLOBAL mode silently when
  `--surfaces` is omitted/`all`; error if the user explicitly requested
  `--surfaces=agents-md` in global mode.
- [x] Add a `git_repo_tmp(tmp_path)` fixture that creates `tmp_path/.git/`.
- [x] Add a `home_tmp(tmp_path, monkeypatch)` fixture that sets `$HOME=tmp_path`.
- [x] Rewrite `tests/test_install.py` for the full error matrix:
  resources/reference subcommands, skill composition, `parse_surfaces` parsing,
  scope disambiguation (implicit + explicit-flag conflicts), `--project` mode
  (in-repo, non-repo, `$HOME` refusal, byte-identical surfaces, idempotent,
  forward-compat guard, duplicate-block collapse, `--pin` override), `--global`
  mode (writes, `--surfaces=agents-md` error, portable-only filter), `--surfaces`
  filtering in project mode, pre-write target message, discovery-copy drift.
- [x] Drop `tests/test_install.py::test_install_print_writes_nothing` (no `--print`).
- [x] Update `tests/test_cli.py::test_top_level_help_lists_subcommands` to match
  the new top-level help (no stale `--agents-md` reference).
- [x] Update `tools/pprose/README.md` install paragraph.
- [x] Update root `AGENTS.md` install paragraph.
- [x] Update `tools/pprose/src/pprose/cli.py` command summary for `install`.
- [x] Regenerate the committed discovery copies under `skills/pprose-*/SKILL.md`
  via `devtools/sync_resources.py` so they drop the now-absent `surface=` tag.
- [x] Run `uv run ruff check src tests devtools` and `uv run pytest` clean (210
  tests passing).
- [ ] Create tbd beads linked to this spec to record the work done.
- [ ] Draft a §6.6 / §6.7 addition for the cli-agent-skill-patterns guideline
  codifying the scope-when-ambiguous rule, the `--surfaces` vocabulary, the
  guard rails, and the cross-scope shadowing convention. File the proposal as
  a GitHub issue against `jlevy/tbd` via `gh`.
- [ ] Final commit of implementation + spec on the
  `pprose-skill-install-improvements` branch.

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

All locked in the "Locked decisions" section above before implementation begins.

## References

- cli-agent-skill-patterns guideline §6.6 ("Distribution & multi-agent install") and
  §6.7 ("Making the CLI available: global install vs.
  zero-install"). Run `tbd guidelines cli-agent-skill-patterns` to read.
- flowmark `--surfaces` implementation at
  [flowmark/src/flowmark/cli.py](/Users/levy/wrk/github/flowmark/src/flowmark/cli.py)
  and the surface vocabulary in
  [flowmark/src/flowmark/skill.py](/Users/levy/wrk/github/flowmark/src/flowmark/skill.py).
- git-config scope precedent: `git config` defaults to `--local` inside a repo and
  errors without a scope flag outside one.
- Prior commit on this branch (`7437f44`): initial multi-surface install with format
  stamps and forward-compat guard; this spec layers scope + surfaces vocabulary on top
  of that work.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
