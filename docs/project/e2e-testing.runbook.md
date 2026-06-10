---
title: pprose End-to-End Manual Testing Runbook
description: Manual end-to-end validation of every pprose surface before a release, covering only what unit, integration, and golden tests structurally cannot (real LLM calls, real uvx/PyPI installs, and visual judgment).
date: 2026-06-02
last_updated: 2026-06-02
status: active
---
# pprose End-to-End Manual Testing Runbook

Version: v0.1 (last update 2026-06-02)\
Joshua Levy (github.com/jlevy)

## Purpose

A repeatable manual pass that validates the whole `pprose` toolkit end to end before a
release, and gets final human sign-off on the results an automated test cannot judge.

This runbook is the **residual manual layer**, not the primary safety net.
The project covers as much as possible with automated unit, integration, and especially
golden tests (`cd tools/pprose && uv run pytest`). This document deliberately covers
only what those tests structurally **cannot**: behavior that needs a real LLM and a paid
API key, a real `uvx`/PyPI network install, a browser and human visual judgment, or
output shapes no test currently pins.
Where a manual check here could become an automated test instead, it is flagged in
[Candidates to automate](#candidates-to-automate); prefer adding the test.

> [!IMPORTANT]
> Steps in Phase B make **live, paid** LLM calls, and Phase E needs a **published**
> release. Read the cost and ordering notes before running them.

## What the automated tests already lock (do not re-test by hand)

`uv run pytest` (266+ tests) already covers, and these need **no** manual repetition:

- **Metrics formulas** (`test_metrics.py`): prose exclusion, bracket tags, link/heading
  formulas, banned-register, plus a pinned golden YAML drift catcher.
- **Eval-report schema + alignment** (`test_eval_report.py`): score ranges, dimension
  names, derived-rollup consistency, the alignment property, `--complete` gate.
- **Compare logic** (`test_eval_compare.py`): a byte-for-byte golden on the
  `unified`+`pairs` output, bold/delta rules, version/scope/density warnings.
- **Scoring plumbing** (`test_eval_score.py`): response regrouping, model-alias
  resolution, `--dry-run`, merge semantics, metadata, the full `main()` path with the
  provider Agent mocked (no real key).
- **Render structure** (`test_render_html.py`, `test_rendered_html_e2e.py`): payload
  shape, the three component mounts, `node --check` parse of the inlined JS bundle.
- **Install** (`test_install.py`): scope resolution, `--surfaces`, format-stamp
  forward-compat guard, idempotency, byte-identical portable/Claude skills,
  flowmark-stable generation.
- **Resource sync** (`test_resources_sync.py`): the wheel mirrors match the canonical
  repo docs.

The manual pass below assumes those are green.
Run `uv run pytest` first; if it is red, stop and fix that before manual testing.

## Prerequisites

- `pprose` available: either on `PATH`, or run package-local with
  `cd tools/pprose && uv run pprose <command>`. This runbook uses the `uv run` form.
- Python toolchain installed (`cd tools/pprose && uv sync --all-extras`).
- Node.js (for the rendered-JS parse test and any visual-regression work).
- For Phase B: a provider key in the environment or an auto-loaded `.env` / `.env.local`
  (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, and `GOOGLE_API_KEY`). See the cost warning.
- For Phase C: a real browser (test in **both** Chrome and Safari) with online and
  offline access (to exercise the CDN-font fallback).
- For Phase E: a published pprose release on PyPI and a scratch directory.
- A scratch git repo for install tests:
  `mkdir /tmp/pp-scratch && cd /tmp/pp-scratch && git init`.

All commands below assume the repo root as the working directory unless shown otherwise.

## Test order

Validate in dependency order so each surface’s output feeds the next, and the cheap,
deterministic, offline core comes before the costly external surfaces:

1. Phase A — deterministic CLI (no key, no network, no browser): `metrics` → `report` →
   `compare`.
2. Phase B — LLM scoring (real key, paid): `score`.
3. Phase C — HTML render + visual review (browser).
4. Phase D — reference + install (local `uv run`).
5. Phase E — zero-install + publish (real network/PyPI; only after a real release
   exists).

Phase E is the **release gate**, not a routine step: most of it is impossible until
`v0.1.0` is actually published (see [release risks](#release-risks-to-clear-first)).

* * *

## Phase A — Deterministic CLI (no key, no network)

These are fully offline.
The automated tests exercise the underlying functions; the gaps below are the CLI argv
paths and output shapes that tests do not drive.

### A1. metrics

```bash
cd tools/pprose
uv run pprose metrics tests/test_fixtures/practical_prose_metrics/all_headings.md
uv run pprose metrics tests/test_fixtures/practical_prose_metrics/all_headings.md tests/test_fixtures/practical_prose_metrics/links_mixed.md
uv run pprose metrics tests/test_fixtures/practical_prose_metrics/all_headings.md --format yaml
uv run pprose metrics tests/test_fixtures/practical_prose_metrics/all_headings.md --format json
uv run pprose metrics does-not-exist.md   # expect: "warning: not a file" on stderr, exit 1
```

Expected: single file prints a fixed-width text table; multiple files print a summary
table with truncated long paths; `yaml`/`json` emit a **list** even for one file.

Gaps tests do not cover, so confirm by eye:

- `--banned-words-file`: write a file with two words, a `# comment`, and a blank line;
  run `uv run pprose metrics doc.md --banned-words-file words.txt`; confirm only those
  words flag and a default-list word (e.g. `monumental`) no longer hits.
- The flag-only lint signals (replacement-history, pedantic-marker, generic-heading,
  em-dash density) appear in `metrics` text output but are **intentionally dropped**
  from the eval-report `QuantMetrics` schema.
  Run `metrics` on a doc containing `previously named`, `the canonical X`, an
  `## Overview` heading, and spaced `—` em dashes; confirm each lint section reports the
  right counts. Then confirm (expected) they do **not** appear in `report`/`compare`
  output.

### A2. report

```bash
cd tools/pprose
uv run pprose report from-metrics tests/test_fixtures/practical_prose_metrics/all_headings.md \
  --label smoke --scope-class brief --out /tmp/smoke.eval.md
uv run pprose report validate /tmp/smoke.eval.md            # OK (all-ERR stub still schema-valid)
uv run pprose report validate /tmp/smoke.eval.md --complete # expect FAIL: stub is not complete
uv run pprose report compute-derived /tmp/smoke.eval.md > /dev/null
```

`--in-place` idempotency (tests assert a derived block exists but not byte-stability):
copy a complete fixture, hand-edit one `qual` score, then:

```bash
cp tests/fixtures/rev1-net.eval.md /tmp/r.eval.md
uv run pprose report compute-derived /tmp/r.eval.md --in-place
cp /tmp/r.eval.md /tmp/r1.eval.md
uv run pprose report compute-derived /tmp/r.eval.md --in-place
diff /tmp/r.eval.md /tmp/r1.eval.md && echo "idempotent ✓"
```

### A3. compare

```bash
cd tools/pprose
uv run pprose compare tests/fixtures/figma-net-r1.eval.md tests/fixtures/figma-net-r2.eval.md --format unified
uv run pprose compare tests/fixtures/figma-ddog-r1.eval.md tests/fixtures/figma-ddog-r4.eval.md --format by-doc
uv run pprose compare tests/fixtures/rev1-net.eval.md tests/fixtures/rev2-net.eval.md --pairs rev1-net=rev2-net
```

`by-doc` has **no golden/shape test** — eyeball: one section per doc, a per-doc header
line (Source / Scope / Overall mean / Rubric / Model / Eval date), group + overall
means, a numbered Violations list matching `rule_findings`, and Quant/Derived tables.

Draft/misalignment rejection on a **real** file (all committed fixtures are
complete+aligned, so only temp-file tests cover this):

```bash
cd tools/pprose
uv run pprose compare /tmp/smoke.eval.md tests/fixtures/rev1-net.eval.md            # expect exit 1: "status=draft ... pass --allow-draft"
uv run pprose compare /tmp/smoke.eval.md tests/fixtures/rev1-net.eval.md --allow-draft --allow-misalignment   # passes with stderr + inline warnings
```

* * *

## Phase B — LLM scoring (real API key, paid)

> [!WARNING]
> **Cost and the dotenv gotcha.** `.env` and `.env.local` are auto-loaded from the cwd
> hierarchy **and** `$HOME`, with later files overriding earlier.
> So `pprose score` can make a real, billable call as soon as any reachable dotenv
> defines the key — `env -u ANTHROPIC_API_KEY ...` does **not** prevent it.
> The default model is the flagship Opus (most expensive).
> Use a cheap alias and a tiny artifact for smoke tests.

### B1. No-key smoke (free)

```bash
cd tools/pprose
uv run pprose score --list-models           # alias table, no key
uv run pprose score /tmp/smoke.eval.md --dry-run > /tmp/prompt.md   # ~139KB prompt, no API call
```

In `/tmp/prompt.md` confirm: the full rubric, the prescriptive guidelines, the
rule-number bounds, an `Artifact under review (<path>)` block with the real text, and
**no** unsubstituted `{{CANONICAL_NAMES}}` / `{{DIMENSION_COUNT}}` placeholders.

### B2. One real single-model call

```bash
cd tools/pprose
# ANTHROPIC_API_KEY must be set (or in an auto-loaded .env/.env.local)
uv run pprose score /tmp/smoke.eval.md --model opus
uv run pprose report validate /tmp/smoke.eval.md --complete   # expect OK
```

Inspect the filled `/tmp/smoke.eval.md`: `qual` has real 1-5/NA scores (not all-ERR);
every sub-5 score has a matching `rule_finding` (alignment); `metadata` carries `model`,
`model_id`, `command`, all four `sha256` fields, `sdk_version`, `cache_stats`, and
`status: complete`.

### B3. Caching, batch, providers

- **Caching:** score the same report twice within ~5 min.
  First `cache_stats` shows `cache_write_tokens` large, `cache_read_tokens` 0; second
  shows `cache_read_tokens > 0` and lower `input_tokens`.
- **Batch + partial-failure:** build 3 stubs, corrupt one artifact path, then
  `uv run pprose score a.eval.md b.eval.md c.eval.md --batch --max-concurrent 2 --max-rps 2 --model opus`.
  Expect a batch header line, per-file `OK`/`FAIL`, a final `N/N OK, M failed` summary,
  the corrupt file failing **without** aborting the others, and exit 1.
- **Other providers:** with the right key, `--model gpt` (and `--model gemini`).
- **Gemini key-name gotcha:** `main()` requires `GOOGLE_API_KEY`, but environments
  commonly set `GEMINI_API_KEY`. With only `GEMINI_API_KEY` set, `--model gemini` is
  expected to fail the early guard with `GOOGLE_API_KEY not set`. This is a known UX bug
  (see [release risks](#release-risks-to-clear-first)).

### B4. Calibration drift

Re-score the pinned calibration fixtures and compare to the agreed values in
[practical-prose-eval-single.runbook.md](../../runbooks/practical-prose-eval-single.runbook.md):
`rev1-net` ~4.1 (0 NA), `rev2-net` ~3.1 (0 NA), `guidelines-self` ~4.1 (5 NA). Flag
drift if the overall-mean gap is >0.5 or any dimension gap is >1.

* * *

## Phase C — HTML render + visual review (browser)

The Python side only shapes JSON; all DOM is built client-side by the shared `bi-card`,
`tip-panels`, and `theme-toggle` components.
**No automated test renders pixels**, so the entire visual contract rests on this phase.

### C1. Render a sample

```bash
cd tools/pprose
uv run pprose render tests/fixtures/rev2-net.eval.md -o /tmp/pprose-sample.html --open
uv run pprose render tests/fixtures/rev2-net.eval.md -o /tmp/out-a4.html --page-size a4
```

### C2. Human visual checklist

Open `/tmp/pprose-sample.html` in **Chrome and Safari** and confirm each item:

- [ ] **Bi-card:** 6 group columns, 20 dimension rows, score bars + colored score
  circles.
- [ ] **Hover:** hovering each dimension row updates the left rubric panel (question +
  rules) and right assess panel (reasons/findings); both panels slide to align with the
  hovered row; a mirrored dim widget appears in the assess panel.
- [ ] **Theme toggle:** Auto / Light / Dark all render legibly; flipping OS appearance
  in Auto follows; the 6 group accents (P blue, E green, F yellow, R red, G cyan, J
  purple) and per-dim shade gradients stay distinguishable in dark mode.
- [ ] **Group icons:** each header shows its distinct icon tinted in the group accent,
  in both themes.
- [ ] **Print/PDF (Cmd+P):** no theme toggle, forced white background + black text even
  in OS dark mode, cards and tip panels do not split across pages; `--page-size a4`
  changes the `@page` size.
- [ ] **Responsive:** dragging the window across ~1152px (72rem) reflows the two panels
  from side-by-side to stacked, with no overflow/clipping.
- [ ] **Fonts:** online, Source Sans 3 (chrome) + Noto Serif (body) load from jsdelivr;
  **offline (or blocking jsdelivr)** the fallback stack still looks acceptable — the
  page must not be broken without the CDN.
- [ ] **Sentinels:** render a fixture containing NA and ERR scores (craft one if needed)
  and confirm NA shows grey, ERR shows red, numeric scores show graduated weight.

### C3. Workbench parity

Open `tools/explorations/visual-design/dimension-visualizations.html` and confirm the
shared `bi-card` / `tip-panels` / `theme-toggle` render **identically** to the
production page (the workbench-only surface-toggle is expected to differ).
Divergence means a shared component drifted.

> Note: `--format folder` currently emits HTML byte-identical to single mode and never
> references the sidecar `assets/` it writes.
> Treat folder output as suspect until that is fixed or removed (see
> [release risks](#release-risks-to-clear-first)).

* * *

## Phase D — Reference + install (local)

```bash
cd tools/pprose
uv run pprose guidelines --list && uv run pprose shortcut --list && uv run pprose runbook --list && uv run pprose skill --list
uv run pprose about | head
uv run pprose skill            # no-arg overview
```

Install into the scratch git repo, then re-run for idempotency:

```bash
cd /tmp/pp-scratch
( cd /path/to/practical-prose/tools/pprose && uv run pprose install --dir /tmp/pp-scratch --auto )
# expect 11 artifacts (5 portable + 5 claude + 1 agents-md), exit 0
```

Confirm by eye:

- [ ] `.agents/skills/<name>/SKILL.md` and `.claude/skills/<name>/SKILL.md` exist and
  are byte-identical; each has frontmatter, the `DO NOT EDIT ... format=f01` marker, and
  a `uvx pprose@<pin>` bootstrap line.
- [ ] `AGENTS.md` has a `BEGIN/END PPROSE INTEGRATION format=f01` block; re-running
  install reports all `unchanged`.
- [ ] Scope guards: `pprose install` refuses `$HOME` in project mode; explicit
  `--global` writes under `$HOME` and drops `agents-md`.

* * *

## Phase E — Zero-install + publish (post-release; network/PyPI)

Only possible **after** a real release exists.
See [release risks](#release-risks-to-clear-first) first.

Before tagging, smoke-test the local wheel:

```bash
cd tools/pprose && uv build
uv venv /tmp/whl --python 3.13
uv pip install --python /tmp/whl dist/pprose-*.whl
/tmp/whl/bin/pprose guidelines --list   # bundled resources resolve from the wheel
```

After `gh release create v0.1.0` and a successful `publish.yml` run, from a directory
**outside** the repo:

```bash
uvx pprose@0.1.0 --help
uvx pprose@0.1.0 about
uvx pprose@0.1.0 guidelines --list
cd /tmp/pp-scratch2 && git init && uvx pprose@0.1.0 install   # baked pin must resolve
```

- [ ] The pin baked into generated files is the published version (not the `0.1.0`
  `DISCOVERY_VERSION` fallback masking an unpublished release).
- [ ] In a live Claude Code / Codex session in the scratch repo, the 6 pprose skills are
  invocable and the AGENTS.md block shows in context; triggering “score this doc” routes
  to `pprose-eval`.

* * *

## Final human sign-off

- [ ] `uv run pytest` green; `make lint-check` clean at the repo root.
- [ ] Phase A deterministic checks pass (incl.
  the by-doc shape and draft-rejection UX).
- [ ] Phase B: one real score validates `--complete`; caching observed; batch isolates
  failures; calibration drift within tolerance.
- [ ] Phase C visual checklist signed off in Chrome **and** Safari, including print and
  offline fonts.
- [ ] Phase D install is idempotent and scope-guarded.
- [ ] Phase E (post-publish): `uvx pprose@<ver>` resolves and installs; a live agent
  ingests the skills.

## Release risks to clear first

These were surfaced by the readiness review and block or complicate a first release; see
also [release-readiness-2026-06.md](release-readiness-2026-06.md) for the full ranked
list:

1. **No release tag exists**, so dynamic versioning yields `0.0.1.devNN+hash` and every
   `uvx pprose@0.1.0` reference (AGENTS.md, `DISCOVERY_VERSION`, committed `skills/`)
   cannot resolve until `v0.1.0` is published.
   Publish `v0.1.0` first, or align `DISCOVERY_VERSION` to the real first tag and
   re-render `skills/`.
2. **Gemini key-name mismatch** (`GOOGLE_API_KEY` vs common `GEMINI_API_KEY`).
3. **Root README documents removed install flags** (`--claude/--codex/--skip-*`).
4. **`--format folder`** ships dead sidecar files.
5. **`publishing.md` / `installation.md`** are unedited `OWNER/PROJECT` template stubs.
6. **License metadata says MIT-only** though the wheel bundles CC-BY prose.
7. No `pprose --version`, no CHANGELOG; `detect_kind()` swallows all exceptions.

## Candidates to automate

Prefer converting these manual checks to tests (golden where possible) rather than
relying on the runbook:

- Golden: `metrics` CLI argv path (`--format yaml|json`, multi-file summary, nonexistent
  file exit 1); the flag-only lint signals (and their intended absence from `report`).
- Golden: `compare --format by-doc` (`render_per_doc_rollup`), the way unified+pairs is
  locked.
- Golden: `--banned-words-file` end to end via CLI.
- Integration: `compute-derived --in-place` idempotency; `compare` draft/misalignment
  rejection on a committed draft fixture; `score --batch` partial-failure isolation via
  the existing FunctionModel harness (no key); Gemini key-alias resolution.
- CI: `uv build` + install-from-wheel smoke (catches data-file packaging regressions).
- Visual-regression smoke (Playwright): one screenshot each of light / dark / print,
  including a sentinel (NA/ERR) fixture, to anchor the otherwise fully-manual visual
  contract.

## Related docs

- [practical-prose-eval-single.runbook.md](../../runbooks/practical-prose-eval-single.runbook.md):
  the single-document eval workflow (calibration set lives here).
- [practical-prose-eval-compare.runbook.md](../../runbooks/practical-prose-eval-compare.runbook.md):
  the multi-document comparison workflow.
- [agents-internal-guide.md](agents-internal-guide.md): repo workflows table and tooling
  layout.
- [SUPPLY-CHAIN-SECURITY.md](../../SUPPLY-CHAIN-SECURITY.md): dependency policy.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
