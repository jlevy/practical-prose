---
title: pprose First-Release Readiness Review (2026-06)
description: A snapshot assessment of how well-organized pprose is for a first public release — what works, the ranked risks to clear, and what should become automated tests.
date: 2026-06-02
last_updated: 2026-06-02
status: active
---
# pprose First-Release Readiness Review (2026-06)

Version: v0.1 (last update 2026-06-02)\
Joshua Levy (github.com/jlevy)

## Purpose

A point-in-time assessment of whether `pprose` is well-organized and working well enough
for a first public release.
It pairs with [e2e-testing.runbook.md](e2e-testing.runbook.md), which is the manual
validation pass; this document is the **findings and punch list**. Both were produced
from a surface-by-surface review of the CLI, its tests, the rendered HTML, and the
packaging/publish path.

## Overall assessment

The toolkit is **functionally complete and well-tested at the unit/integration level**,
but **not yet releasable for the headline zero-install path**, and it carries a handful
of doc-drift and organization rough edges that a first public release should not ship
with.

What is solid:

- The deterministic core (`metrics`, `report`, `compare`) is fully testable offline and
  well covered, including a byte-for-byte golden on the comparison output.
- The eval-report schema, alignment property, and `--complete` publish gate are
  thoroughly validated.
- `install` is robust: scope auto-detection, `$HOME`/git guards, format-stamp
  forward-compat, idempotency, byte-identical portable/Claude skills.
- The build/publish mechanics (Hatchling, dynamic versioning, OIDC trusted publishing)
  are sound, and the wheel correctly bundles all runtime data (verified by installing
  the built wheel into a clean venv and loading bundled resources).

What is not ready: the version/publish story (no tag exists yet), a few stale docs, and
an entirely manual visual contract.
Details below.

## Ranked release risks

Ordered by severity.
Each has a one-line fix.
The [e2e runbook](e2e-testing.runbook.md) points back here.

1. **No release tag → `uvx pprose@0.1.0` cannot resolve.** Dynamic versioning yields
   `0.0.1.devNN+hash`; `DISCOVERY_VERSION`, the `AGENTS.md` block, and every committed
   `skills/` copy hard-code `0.1.0`. *Fix: publish `v0.1.0` to PyPI as the first tag (or
   align `DISCOVERY_VERSION` to the real first tag) and re-render `skills/` before
   announcing zero-install.*
2. **Zero-install / publish path has zero automated coverage and is untested live.** The
   headline onboarding could fail for the very first user (unpublished version, wheel
   packaging regression, OIDC misconfig).
   *Fix: add a CI `uv build` + install-from-wheel smoke job; manually run
   `uvx pprose@0.1.0 …` immediately post-publish.*
3. **Gemini key-name mismatch.** `main()` hard-requires `GOOGLE_API_KEY`, but
   environments commonly set `GEMINI_API_KEY`; `--model gemini` is blocked despite a
   valid key being present.
   *Fix: accept `GEMINI_API_KEY` as an alias, or document the required export.*
4. **Strong dotenv autoload + flagship default model = silent paid calls.** `.env` /
   `.env.local` auto-load from the cwd hierarchy and `$HOME`; `env -u VAR` does not
   prevent a real billable Opus call.
   *Fix: document the autoload + default-cost behavior prominently; consider a cheaper
   default or a cost confirmation.*
5. **Root README documents removed install flags** (`--claude/--codex/--skip-*`); the
   real CLI is `--project/--global/--surfaces/--pin`. *Fix: update the root README to
   match the shipped CLI (tools/pprose/README.md is already correct).*
6. **`--format folder` ships dead files.** The emitted HTML is byte-identical to single
   mode and never references the sidecar `assets/` it writes.
   *Fix: wire folder HTML to `<link>`/`<script src>`, or remove the option before
   release.*
7. **`publishing.md` / `installation.md` are unedited template stubs** with
   `OWNER/PROJECT` placeholders.
   *Fix: substitute `jlevy/practical-prose` and `pprose` so a first releaser does not
   misconfigure trusted publishing.*
8. **The entire visual contract rests on manual review** (icons, bars, hover panels,
   dark mode, print pagination, responsive).
   *Fix: add a Playwright screenshot/visual-regression smoke, or at minimum ship the
   manual checklist (now in the e2e runbook).*
9. **No golden/shape test for `compare --format by-doc`** (only unified+pairs is
   byte-locked). *Fix: add a golden test.*
10. **License metadata says MIT-only but the wheel bundles CC-BY prose.** *Fix: add a
    metadata/README note clarifying bundled prose stays CC BY 4.0.*
11. **Curated `SUGGESTED_MODELS` hard-code versions** that drift as providers
    ship/retire models; aliases fail only at the live boundary.
    *Fix: add a maintenance note tying the table to the pricing data source, and a
    release-checklist re-verify.*
12. **Metrics→eval-report lint asymmetry is undocumented.** Rich lint signals
    (replacement-history, pedantic-marker, generic-heading, em-dash density) are
    silently dropped at the `QuantMetrics` boundary.
    *Fix: one doc note at the command boundary.*
13. **No `pprose --version` and no CHANGELOG** for a tool that bakes pins into
    artifacts. *Fix: add `--version` and a CHANGELOG stub.*
14. **`detect_kind()` swallows all exceptions**, so an almost-valid `.md` renders a
    confusing/empty page instead of erroring.
    *Fix: narrow the catch and emit a clear error.*
15. **print.css duplicates light-mode tokens by hand**, outside the sync `--check` gate,
    so it can silently drift from `design-system.yaml`. *Fix: generate the print token
    block too.*
16. **Repo clutter for a dual doc+tool repo.** The root mixes prose deliverables
    (`docs/`, `runbooks/`, `shortcuts/`, `skills/`, `example-texts/`, `evals/`) with
    tooling configs (`biome.json`, `package.json`, `node_modules/`, `ruff.toml`,
    `lefthook.yml`) and large archives (`attic/` with vendored copies,
    `research-archive/`). Project specs live in **two** places
    (`docs/project/specs/active` and `tools/docs/project/specs/active`). *Fix: pick one
    specs home, and gitignore or remove `attic/` and loose root drafts before tagging.*
    Moving the JS tooling (`package.json`/`node_modules`) under `tools/` was considered
    and **deliberately deferred**: lefthook’s git hook discovers its binary by walking
    `<repo-root>/node_modules` (never down into a subdir) and this hook template sources
    no rc file, so a full move would break hook discovery or force a second root
    `package.json` — more clutter, not less.
    `package.json`/`node_modules` are kept at the root as git-hook infrastructure;
    `biome.json` stays beside them so biome resolves its config from the same root.

## What works (do not re-litigate)

- `metrics` / `report` / `compare` deterministic pipeline and golden coverage.
- `score` plumbing (response regrouping, alias resolution, merge, metadata,
  `--dry-run`), with the provider Agent mocked in tests.
- `install` scope/surface/idempotency/forward-compat behavior.
- Wheel data-file bundling (verified by a clean-venv install-from-wheel).
- Resource-sync drift gate and flowmark-idempotent generation.

## Candidates to automate

See the matching section in
[e2e-testing.runbook.md](e2e-testing.runbook.md#candidates-to-automate).
In short: golden tests for the `metrics` CLI argv path, the flag-only lint signals,
`compare --format by-doc`, and `--banned-words-file`; integration tests for
`compute-derived --in-place` idempotency, `compare` draft rejection, and `score --batch`
partial-failure isolation; a CI wheel-install smoke; and a Playwright visual-regression
smoke. The genuinely manual residue (real paid scoring, live caching accounting, real
`uvx`/PyPI resolution, live agent ingestion, cross-browser typography) stays in the
runbook.

## Method

Findings came from a parallel surface-by-surface review (five area mappers + a
synthesis) that read the source and tests and ran `--help` / `--dry-run` / `uv build` /
install-from-wheel / a real HTML render.
No real LLM calls and no repo mutations were made during the review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
