---
title: CLI cleanup — startup snappiness, color output, and listing UX
description: Make pprose start fast via selective lazy imports, add auto-detected color output with agent/CI-safe plain fallback, and standardize how bundled resources are listed.
author: Joshua Levy (github.com/jlevy) with LLM assistance
---
# Feature: CLI cleanup — startup snappiness, color output, and listing UX

**Date:** 2026-06-11 (last updated 2026-06-13)

**Author:** Joshua Levy with agent assistance

**Status:** Implemented; merged to main in PR #28 (2026-06-13); part of the pending
v0.2.0 release. Selective lazy command imports (startup ~1.16s to ~56ms), auto-detected
color output with `--color {auto,always,never}`, and the listing UX (`--list` removed;
bare-name listings plus a new top-level `pprose list`) all landed.

## Overview

Three CLI-quality problems, fixed together because they share the same files (`cli.py`,
`reference.py`) and the same goal: a CLI that feels first-class both to a human at a
terminal and to an agent driving it programmatically.

1. **Startup is slow.** `pprose --help` takes ~1.3s wall (warm).
   Profiling (`python -X importtime`) shows `import pprose.cli` costs ~1.16s, dominated
   by the eager import chain in `cli.py` line 11: `eval_score` pulls `pydantic_ai` →
   `anthropic` (~0.8s) and `eval_compare` pulls `pydantic_ai` again (~0.3s). Help,
   version, reference printing, and install never need these.
2. **No color support.** Output is monochrome plaintext everywhere; there is no
   TTY/agent detection, no `NO_COLOR`/`FORCE_COLOR`/`CI` handling, and no visual
   hierarchy in help or listings.
3. **Listing UX is inconsistent.** The reference commands document a `--list` flag
   ("Print a bundled guideline doc (--list to see them)") but running
   `pprose guidelines` with no arguments already prints the same listing, so the flag is
   redundant and its documentation misleading.
   There is also no single top-level view of everything bundled (guidelines + shortcuts
   \+ runbooks + skills).

## Goals

- `pprose --help`, `pprose --version`, `pprose guidelines` (and every reference/listing
  path) complete in under ~150ms of Python work (post-interpreter), with a regression
  test guarding the import graph.
- Colored, readable output when attached to an interactive terminal; byte-identical
  plain output when piped, in CI, under `NO_COLOR`, or driven by an agent.
- One obvious listing behavior, documented once, consistent across `guidelines`,
  `shortcut`, `runbook`, and `skill` — plus a single top-level inventory command.
- No behavior change for scoring/eval workflows; no new heavyweight dependencies.

**Compatibility stance: this is a hard cut.** pprose is pre-1.0; backward compatibility
is explicitly *not* a goal.
Every change here picks the cleanest end state and deletes the old shape outright — no
aliases, no deprecation windows, no compatibility shims.
Anything generated (skills, AGENTS.md blocks, bundled doc copies) is regenerated at the
next release.

## Non-Goals

- No TUI, spinners, or progress bars (nothing here is long-running except `score`, which
  already reports per-file progress).
- No JSON output mode for reference commands (revisit if a consumer appears; `metrics`
  already has `--format yaml|json`).
- No CLI framework migration (stays argparse; Typer/Click would re-add startup cost and
  churn for little gain at this command count).
- Not restyling `pprose render` HTML output (covered by the design system).

## Background

Sources consulted (synthesis below; no single source followed slavishly):

- **`tbd guidelines python-cli-patterns`**: respect `NO_COLOR` and `CI`; route data to
  stdout and errors/progress to stderr; exit codes 0/1/2/130; agent compatibility via
  explicit flags; dynamic versioning via `importlib.metadata`.
- **textpress** (`~/wrk/kmd/textpress`): the canonical lazy-import structure.
  Top-level module imports only stdlib + lightweight helpers; every heavy command does
  its imports *inside* the function body, with an explicit comment that this keeps help
  snappy; `--version` resolved lazily after parse; `TYPE_CHECKING` guards for type-only
  imports. Uses `rich` for color (auto-detects TTY and respects `NO_COLOR`).
- **repren** (`attic/repren`, zero-dependency): hand-rolled minimal ANSI constants;
  `use_color = sys.stdout.isatty()` decided at point of use; `CI` env detection;
  terminal width clamped 40-88 with a fixed default when non-TTY; stderr for errors.
  Notably it does *not* honor `NO_COLOR` — we adopt its minimalism but add the standard
  env handling per the guideline and no-color.org.
- **Current pprose**: `cli.py` imports all subsystems eagerly at module top; reference
  listing duplicated between no-args and `--list`.

Decision on color dependency: pprose already has nontrivial dependencies, but the CLI
path should stay light.
We hand-roll a ~40-line ANSI helper (repren-style) rather than adding `rich` to the
startup path: our needs are bold/dim/a few hues for help text and listings, not tables
or markdown. If needs grow, revisit.

## Design

### Approach

**1. Lazy imports with a fast core (startup).**

- `cli.py` keeps only stdlib imports at module level.
  The line
  `from pprose import eval_compare, eval_report, eval_score, install, metrics, reference`
  is replaced by per-command dispatch functions that import inside the function body
  (textpress pattern), e.g. the `score` handler does `from pprose import eval_score`
  in-function. Parser construction, help text, and command routing use only static
  strings — no subsystem import needed to print help or argument errors.
- Reference commands (`guidelines`, `shortcut`, `runbook`, `skill`, `about`) import only
  `pprose.reference` (filesystem + text; verify it is light — if it imports heavy
  modules transitively, split the data-listing core out).
- `--version` stays on `importlib.metadata`, resolved after parse (already cheap).
- Module-level `__getattr__` lazy aliasing is *not* used: explicit in-function imports
  are easier to read and grep, and there are only ~10 command entry points.
- **Guardrails:** a test imports `pprose.cli` in a subprocess with `-X importtime` and
  asserts that `pydantic_ai`, `anthropic`, `openai`, and `google` SDK modules are absent
  from the import log; a second test asserts `python -c "import pprose.cli"` stays under
  a generous wall budget so regressions surface before users feel them.

**2. Terminal output layer (color).**

New small module `pprose/term.py` (stdlib-only):

- `use_color(stream) -> bool`: False when `NO_COLOR` is set (any value), when `CI` is
  set, when the stream is not a TTY, or when `TERM=dumb`; True when `FORCE_COLOR` is set
  (overrides all of the above except an explicit `--color=never`); else
  `stream.isatty()`.
- Optional `--color {auto,always,never}` top-level flag (default `auto`) for explicit
  control, per common convention; env vars cover the agent/CI cases without flags.
- A minimal style set as functions or constants (e.g. `bold`, `dim`, `heading`,
  `command`, `warn`, `err`) that render to plain text when color is off — so call sites
  never branch.
- Output discipline (from the guideline): requested data → stdout; errors, warnings, and
  hints → stderr. Listings are data.
  Width: clamp to 40-100, fixed default when non-TTY (repren pattern).
- Apply styles to: top-level help epilog, command help, reference listings (name in
  bold, description dim), error messages, and the install report.
  Plain-mode output must remain byte-stable for agents (golden-test the plain
  rendering).

**3. Listing UX (one obvious way).**

This is a hard cut: pprose is pre-1.0 and we do not preserve backward compatibility.
Pick the cleanest design and delete the rest; everything regenerates at the next
release.

- **Rule: no-args lists; an argument prints.** `pprose guidelines` lists all guidelines;
  `pprose guidelines <name>` prints one.
  Same for `shortcut`, `runbook`, `skill`. This is the current de facto behavior — we
  make it the documented contract.
- **Remove `--list` entirely** — from the argparse definitions, every help string, and
  every doc. No alias, no hidden flag, no deprecation period.
  If an unregenerated skill from an older release still runs `pprose guidelines --list`,
  argparse errors cleanly; the fix is reinstalling, which the next release does anyway.
- New top-level `pprose list` prints the full bundled inventory grouped by kind
  (guidelines, shortcuts, runbooks, skills), one line each: bold name + dim description.
  `pprose list --kind guidelines` filters.
  The per-command no-arg listings remain (they are what the generated skills and
  AGENTS.md route to).
- Scrub every surface that mentions `--list`: command help strings, the no-args help
  epilog, README (Quick Start + Tooling), the AGENTS.md block template in `install.py`,
  the generated-skill preamble, agents-internal-guide, and any bundled resource docs
  (the resource sync propagates the doc copies).

### Components

- `tools/pprose/src/pprose/cli.py` — lazy dispatch, `--color` flag, `list` command.
- `tools/pprose/src/pprose/term.py` — new color/width/stream helper (stdlib-only).
- `tools/pprose/src/pprose/reference.py` — listing output via `term`, drop `--list` from
  documented surface.
- `tools/pprose/src/pprose/install.py` — preamble/AGENTS.md template wording.
- `tools/pprose/tests/` — import-graph guard, startup budget, golden plain-mode
  listings, color on/off unit tests (force via env in test).
- Docs: README, agents-internal-guide, CHANGELOG (`Unreleased`).

### Phases

**Phase 1 — startup + listing contract (one pass, mostly mechanical):** lazy imports in
`cli.py`; import-graph and budget tests; no-args-lists contract with `--list` removed
outright; `pprose list`; all doc surfaces scrubbed of `--list` and resynced.

**Phase 2 — color layer:** `term.py`, `--color` flag, styled help/listings/errors,
golden plain-mode tests.
(Separate phase so Phase 1’s byte-stable output lands first and the color diff is
reviewable on its own.)

## Risks and Mitigations

- **Lazy imports can hide ImportErrors until a command runs** → the e2e runbook already
  exercises every command; add a smoke test that invokes each command’s `--help`.
- **Color codes leaking into agent transcripts** → default-off outside TTYs plus
  `NO_COLOR`/`CI` respect; golden tests pin the plain output.
- **flowmark/lint hooks on generated listings** → listings are runtime output, not
  files; no interaction.

## Open Questions

- Should `pprose list` also show the eval commands (a full command inventory), or only
  bundled reference docs?
  (Spec assumes docs only; `--help` already inventories commands.)
- Is `reference.py` import-light today?
  (Verify during Phase 1; split if not.)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
