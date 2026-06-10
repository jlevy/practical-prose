---
title: Reporting CLI redesign — the eval → report → show pipeline
description: Redesign the pprose CLI around a clean, composable three-stage pipeline (eval produces one canonical result, report fans it out to any selection of formats, show opens an artifact), backed by a single shared report-view so every format is the same evaluation at a chosen fidelity
author: Joshua Levy (github.com/jlevy) with LLM assistance
---
# Feature: Reporting CLI Redesign — eval → report → show

**Date:** 2026-06-03

**Author:** Joshua Levy

**Status:** Draft — not started as of 2026-06-10 (no eval/report/show pipeline in
cli.py). Implementation tracked under epic pp-d2j3 (phases pp-f86c, pp-qpa2, pp-3evy)
plus the metrics-schema chain (pp-pd8t, pp-vusm, pp-h75u, pp-is5n).

## Overview

The pprose evaluation surface grew command by command, and the result is a set of
overlapping verbs with no single mental model: `metrics`, `report from-metrics`,
`score`, `compare`, and `render`, plus a planned `show`. Producing a result, exporting
structured data, and rendering a visual page are tangled across these commands, two of
them (`score --render-html` and `render`) emit the same HTML, and the YAML writer, the
Markdown body, and the HTML payload each show a *different* subset of the same
evaluation.

This redesign reorganizes the whole surface around one clear, composable pipeline:

```
  doc.md
    │  pprose eval     measure + score → save the complete result
    ▼
  doc.eval.md          ← the canonical artifact (YAML frontmatter + Markdown body)
    │  pprose report   transform the saved eval → output format(s); no model
    ▼
  doc.html  doc.yaml  doc.json  doc.report.md
    │  pprose show     open an artifact in a browser / local app
    ▼
  (displayed)
```

Three principles drive it: every stage is runnable on its own, stages compose with a
clear artifact contract between them, and common end-to-end chains are one flag away
(`pprose eval doc.md --report html --open`).

There are no backward-compatibility constraints.
The current commands are reorganized into the new model rather than preserved.
This spec subsumes
[plan-2026-06-02-eval-output-improvements.md](../done/plan-2026-06-02-eval-output-improvements.md):
its three threads (the `frontmatter-format` YAML writer, the whole-report structured
export, and the finding-location anchors in the visual output) are carried forward as
phases here, generalized so they serve every format rather than one command.

## Goals

- One canonical result artifact.
  `pprose eval <doc.md>` runs deterministic metrics, model scoring, and derived rollups,
  then writes a complete, validated `.eval.md` that holds every score, reason, rule
  finding, and location anchor.
  Nothing downstream re-derives or re-scores.
- One transform stage.
  `pprose report <eval.md> --format <list>` renders the saved eval into one, a
  selection, or all output formats, with no model calls.
  `--format html`, `--format html,yaml,md`, and `--format all` are the one/selection/all
  cases of a single flag.
- One display verb. `pprose show <artifact>` opens an artifact in the browser or a local
  app. Given an `.eval.md`, it renders to HTML first, then opens.
- One shared report-view behind every format, so `html`, `md`, `yaml`, and `json` are
  provably the same evaluation at a chosen fidelity.
  No format silently drops findings, location anchors, or quantitative tables (the
  current HTML payload drops all three).
- Predictable output rules: a single text format with no `--output` goes to stdout; one
  format with `--output FILE` writes that file; two or more formats require an output
  directory and write `<stem>.<ext>` per format.
- Composition sugar on `eval`: `--report <list>` and `--open` chain eval → report → show
  through the same code paths the standalone commands use.
- CLI conventions are uniform across all commands per the `python-cli-patterns`
  guideline: long flags only (`--output`, never `-o`), `--format` for output shape
  everywhere, data to stdout and diagnostics to stderr.
- Consistent YAML. All `EvalReport` YAML (the `.eval.md` frontmatter and the `yaml`
  report format) is produced by one `frontmatter-format` writer with one logical key
  order.

## Non-Goals

- No change to the scoring prompt, the model behavior, the rubric, the 20 dimensions,
  the metrics, or the derived rollups.
  This is a surface and plumbing redesign, not a scoring change.
- No `--detail full` yet.
  `report` ships with `standard` detail only.
  `full`, which embeds the full source document inline with per-span score annotations,
  is explicitly reserved as future work (see *Detail levels*).
- No theme or layout-variant selection.
  The single existing `interactive` HTML layout is the only one; `--theme` and
  `--variant` are out of scope for this change.
- No raster or print image export.
  `svg`, `png`, and `pdf` are named in the format design but not implemented here;
  raster needs a new headless or rasterizer dependency with a supply-chain cool-off,
  tracked as a follow-on.
- No change to the on-disk `.eval.md` shape (still YAML frontmatter + Markdown body).

## Background

The current surface and its seams:

| Command | Job today | Output shape control |
| --- | --- | --- |
| `pprose metrics` | deterministic measurement only | `--format text\|yaml\|json` |
| `pprose report from-metrics\|validate\|compute-derived` | build stub / validate / recompute `.eval.md` | subcommands |
| `pprose score` | fill qual + findings; can also render HTML | `--out`, `--render-html` + `--render-*` |
| `pprose compare` | N reports → comparison Markdown | `--format unified\|sections\|by-doc\|both` |
| `pprose render` | one `.eval.md` → static HTML | `--variant` (only `interactive`), `--page-size`, `-o` |

Problems this redesign fixes:

1. **No single result step.** Producing a complete eval requires `report from-metrics`
   then `score`. There is no one verb for “evaluate this document and save the result”.
2. **Three renderers, not at parity.**
   [render_single_doc_rollup](../../../../tools/pprose/src/pprose/eval_render.py) (the
   Markdown body) shows scores, reasons, violations *with* locations, and quantitative
   tables. [build_payload](../../../../tools/pprose/src/pprose/render_html/renderer.py)
   (the HTML payload) shows scores, reasons, and findings, but drops `locations` and has
   no quant tables. `_format_locations` lives only in the Markdown path.
   The same evaluation looks materially different depending on the output.
3. **No flexible fan-out.** Each command emits one artifact.
   There is no “one or a selection or all” generation, and `score --render-html`
   duplicates `render`.
4. **Inconsistent conventions.** `render` uses `-o/--output`; everyone else is
   long-only. “Output shape” is `--format` in three commands but `--variant` in `render`.
   YAML is written two ways (`EvalReport.to_yaml` sorts keys alphabetically; `metrics`
   does not).
5. **Misnamed display.** The previously planned `pprose show` printed structured
   YAML/JSON to stdout, which is *reporting to stdout*, not *showing*. This redesign
   reclaims `show` for the open-in-browser/app action and folds structured stdout into
   `report`.

## Design

### The pipeline and its contracts

- `doc.md` → **eval** → `doc.eval.md` (complete, validated, canonical).
- `doc.eval.md` → **report** → `doc.html` / `doc.yaml` / `doc.json` / `doc.report.md`.
- any artifact → **show** → opened in a browser or local app.

`eval` is the only stage that measures or calls a model.
`report` only transforms what `eval` saved.
`show` only displays.
The contract between stages is the file on disk, so any stage can be run independently
and the boundary is inspectable.

### Command surface

**Evaluate group**

- `pprose metrics <doc.md…> [--format text|yaml|json]` — unchanged in spirit:
  deterministic measurement, no model, no API key.
  The fast substrate and quick peek.
  Stays its own command so `eval` is unambiguously “the real, saved evaluation”.
- `pprose eval <doc.md> [options]` — the new result-producing command.
  Runs metrics + scoring + rollups and writes a complete `.eval.md`. Subsumes
  `report from-metrics` and `score`. Options carry over from those commands: `--model`
  (required for scoring), `--scope-class`, `--label`, `--evaluator`, `--method`,
  `--commit-sha`, `--rubric-version`, the batch controls (`--batch`, `--max-concurrent`,
  `--max-rps`), `--dry-run`, `--list-models`, `--allow-misaligned`. Default output is
  `<stem>.eval.md` beside the input; `--output PATH` overrides; `--output -` writes to
  stdout. Composition flags: `--report <format-list>` and `--open` (see *Composition*).
  - Metrics-only path (no model): `pprose eval <doc.md> --no-score` writes the draft
    `.eval.md` stub (the old `from-metrics` behavior) so an eval can be staged without a
    provider key.
- `pprose compare <eval.md…> [--format unified|sections|by-doc|both] [...]` — unchanged
  in role (multi-doc, second-order comparison).
  Flags realigned to the shared conventions.
- `pprose validate <eval.md> [--complete] [--allow-misalignment] [--recompute]` — new
  top-level command absorbing `report validate` and `report compute-derived`. Validates
  schema, the alignment property, and (with `--complete`) completeness.
  `--recompute` recomputes derived rollups and rewrites the body in place, replacing
  `compute-derived`.

**Report group**

- `pprose report <eval.md> [--format <list>] [--detail standard] [--output <path|dir>]`
  — the transform stage.
  Renders the saved eval into the requested formats.
  No model. See *Formats and output rules*.
- `pprose show <artifact> [--app <name>]` — open an artifact.
  If given an `.html` (or other directly viewable file), open it.
  If given an `.eval.md`, render it to HTML via the `report` path, then open.
  This is the old `render --open` promoted to a verb.

**Reference / Setup groups** — `guidelines`, `shortcut`, `runbook`, `skill`, `about`,
`install` are unchanged.

### The shared report-view (the load-bearing refactor)

Introduce a single intermediate model, the *report view*, that every format renders
from. It is built once from a validated `EvalReport` and carries the full evaluation:
groups and dimensions, per-dimension score + reason, every rule finding with its
formatted location anchors, the violation subset, the quantitative rows, the derived
density and structure ratios, the rubric rollup, and metadata.

- `report --format md` and the `.eval.md` body both render from the report view (today’s
  `render_single_doc_rollup` becomes a renderer *over* the view rather than a parallel
  reader of the raw model).
- `report --format html` builds its JSON payload from the *same* view, so findings,
  location anchors, and quantitative tables all reach the page.
  `_format_locations` becomes a property of the view, shared by the Markdown and HTML
  renderers, so the two cannot drift.
- `report --format yaml|json` serializes the validated `EvalReport` directly (always
  complete; see *Detail levels*), not the view, since structured consumers want the
  canonical schema, not a presentation projection.

This is what makes `report` an honest fan-out: html/md are the same evaluation at the
same fidelity, and yaml/json are the complete underlying data.
It also generalizes the 2026-06-02 plan’s panel-location fix: instead of threading
`locations` into one renderer, the anchors live on the view and reach every human-facing
format at once.

### Formats and output rules

`--format` accepts a comma-separated list.
`all` expands to every implemented format.

| Format | Renders from | Content | Status |
| --- | --- | --- | --- |
| `md` | report view | clean softschema summary (Markdown + YAML frontmatter) | implemented |
| `html` | report view | interactive static HTML (self-contained, inlined) | implemented |
| `yaml` | EvalReport | full structured frontmatter (pure YAML, no body) | implemented |
| `json` | EvalReport | full structured data as JSON | implemented |
| `svg` / `png` / `pdf` | report view | rasterized / print visual | reserved (not built) |

Default format for `report` is `md` to stdout: a bare `pprose report doc.eval.md` prints
a readable summary. The visual and binary formats are opt-in.

Output location follows one rule:

- one text format (`md`/`yaml`/`json`), no `--output` → **stdout**.
- one format + `--output FILE` → that file; when `--format` is omitted, infer it from
  the extension (`.html`→html, `.yaml`/`.yml`→yaml, `.json`→json, `.md`→md).
  An explicit `--format` always wins.
- two or more formats → `--output` must be a directory (created if absent); each format
  is written as `<eval-stem>.<ext>` inside it.
  Default directory is alongside the input.

### Detail levels

`report` exposes `--detail`, which currently accepts only `standard` (the default).
`standard` is the full rollup as rendered today (scores, reasons, violations with
locations, quantitative tables).
The flag exists now so the surface is stable and the roadmap is visible; its help text
names `full` as reserved.

`full` (future, not in this change) will embed the full source document inline with
per-span annotations tying each scored region back to the findings that cite it.
It applies to the human-facing formats (`md`, `html`). Structured formats (`yaml`,
`json`) always emit the complete schema regardless of `--detail`, so a machine consumer
never gets a truncated report.

### Composition

`eval` chains the pipeline through the same code paths the standalone commands use:

```
pprose eval doc.md --report html --open    # eval → report(html) → show
pprose eval doc.md --report all            # eval → every implemented format
pprose eval doc.md                         # eval only; writes doc.eval.md
```

`--report` takes the same format list as `pprose report --format`. `--open` implies a
viewable format and opens the result (HTML if present, else the default).
Each underlying stage remains independently runnable; the flags are sugar, not a
separate path.

### YAML serialization

Adopt `frontmatter-format` (first-party, `jlevy` org) as the single YAML writer for both
the `.eval.md` frontmatter and the `report --format yaml` output, with one logical
`EVAL_REPORT_KEY_ORDER` (the depth-first schema walk specified in the superseded
2026-06-02 plan, carried forward verbatim and pinned by a unit test).
This replaces the current `pyyaml.safe_dump(sort_keys=True)` path so YAML output is
uniform and ordered.

### API Changes

- **New:** `pprose eval <doc.md>` (subsumes `report from-metrics` + `score`;
  `--no-score` for the metrics-only stub; `--report`, `--open` composition;
  `--output`/`--output -`).
- **New:** `pprose report <eval.md> --format <list>` (subsumes `render`; absorbs the
  planned structured `show`).
- **New:** `pprose show <artifact>` (open in browser/app; old `render --open`).
- **New:** `pprose validate <eval.md>` (absorbs `report validate` + `compute-derived`
  via `--recompute`).
- **Removed:** `pprose report` subcommands, `pprose score`, `pprose render`,
  `score --render-html` and its `--render-*` flags.
  The `metrics` and `compare` commands stay (flags realigned).
- **New dependency:** `frontmatter-format` (pinned exact version, recorded under the
  first-party exemption in SUPPLY-CHAIN-SECURITY.md, `uv.lock` committed).

## Implementation Plan

One PR. The phases are ordered so each leaves the tree green and testable; keep them
few. Phases 1 and 2 carry forward the substance of the superseded 2026-06-02 plan (its
YAML writer and its structured export / location work), generalized to serve every
format.

### Phase 1: shared report-view + frontmatter-format YAML

- [ ] Add `frontmatter-format` (pinned) to
  [tools/pprose/pyproject.toml](../../../../tools/pprose/pyproject.toml); refresh
  `uv.lock`; record in [SUPPLY-CHAIN-SECURITY.md](../../../../SUPPLY-CHAIN-SECURITY.md).
- [ ] Add `EVAL_REPORT_KEY_ORDER` and migrate `EvalReport.to_yaml()` to
  `frontmatter-format`’s `to_yaml_string` with `custom_key_sort`; keep `to_eval_md`
  emitting frontmatter + body and the round-trip stable.
- [ ] Build the report-view model: one structure carrying groups/dimensions, scores,
  reasons, findings with formatted locations, violations, quant rows, derived ratios,
  rollup, and metadata.
  Move `_format_locations` onto it.
- [ ] Re-express `render_single_doc_rollup` (the `md` renderer and `.eval.md` body) as a
  renderer over the report-view.
  Re-express the HTML `build_payload` to read the same view so findings, locations, and
  quant tables reach the page.

### Phase 2: the new command surface

- [ ] `pprose eval`: new module that runs metrics + scoring + rollups and writes
  `.eval.md`; carry over the relevant `score` / `from-metrics` options; add
  `--no-score`, `--output`/`--output -`, and the `--report` / `--open` composition.
- [ ] `pprose report`: new module rendering the report-view into `--format`
  (md/html/yaml/json, list + `all`), `--detail standard`, and the output-location rule.
- [ ] `pprose show`: open an artifact; render an `.eval.md` to HTML via the `report`
  path first when needed.
- [ ] `pprose validate`: top-level; schema + alignment + `--complete`; `--recompute`
  rewrites derived + body.
- [ ] Rewrite [cli.py](../../../../tools/pprose/src/pprose/cli.py) `COMMANDS` / groups
  to the new surface; remove `report` (subcommands), `score`, `render`, and
  `score --render-html`. Realign `metrics` / `compare` flags to long-only `--output` and
  shared `--format` conventions.

### Phase 3: fixtures, generated mirrors, docs

- [ ] Re-serialize the `.eval.md` fixtures and the comparison golden to the new key
  order; confirm diffs are formatting-only.
- [ ] Regenerate the `_generated/` HTML/JS/CSS mirrors via
  [sync_render_html_styles.py](../../../../tools/pprose/devtools/sync_render_html_styles.py);
  confirm `make generate-check` is clean.
  Surface the finding-location anchors in the rendered panel (the 2026-06-02 Phase 2
  fix), now driven by the shared view.
- [ ] Update README, AGENTS.md, and
  [docs/project/agents-internal-guide.md](../../../../docs/project/agents-internal-guide.md)
  to the eval → report → show surface.

## Testing Strategy

- **Unit:** report-view carries findings, locations, and quant rows for a representative
  report; `md`, `yaml`, `json`, and `mdyaml` each round-trip back to the same
  `EvalReport`; `EVAL_REPORT_KEY_ORDER` is asserted on a fully populated fixture; the
  output-location rule (stdout / single file / multi-format directory) is covered.
- **Parity:** the `md` and `html` renderers, given the same report-view, surface the
  same findings and the same location anchors (the bug this redesign closes).
- **Golden:** the `.eval.md` fixtures and the comparison golden re-serialize with
  formatting-only diffs; an HTML e2e asserts a known location quote and `§` anchor reach
  the rendered page.
- **End-to-end smoke:** `pprose eval doc.md --report all --open` produces every artifact
  and opens the HTML; `pprose report doc.eval.md --format yaml` matches the `.eval.md`
  frontmatter; `pprose validate --recompute` is idempotent.
- **Full gate:** `make generate` + `make lint` + `make test` clean;
  `make generate-check` shows no drift.

## Rollout Plan

Single PR off `main`. Generated mirrors and re-serialized fixtures are committed so a
clean clone works with no build step.
Pre-commit hooks (flowmark + resources-sync + generate-check) gate the merge.
Because there is no backward-compatibility constraint, the old command names are removed
rather than aliased; the README and skills are updated in the same PR so the documented
surface matches the shipped one.

## Open Questions

- Should `pprose show` render an `.eval.md` to a sibling file (discoverable, reusable)
  or a temporary file (no clutter)?
  Leaning sibling, matching `report`’s default naming, with a flag to force temp.
- Does `compare` eventually gain `--format html` through the same report-view, or stay
  Markdown-only? Out of scope here; noted as a natural future extension.
- Is `--no-score` the right name for the metrics-only stub path on `eval`, or should
  staging a draft be a distinct verb?
  Leaning `--no-score` for now (one result command).

## References

- [plan-2026-06-02-eval-output-improvements.md](../done/plan-2026-06-02-eval-output-improvements.md)
  — superseded by this spec; its frontmatter-format writer, structured export, and
  panel-location work are carried forward as Phases 1-3.
- [plan-2026-05-29-static-html-eval-report.md](../done/plan-2026-05-29-static-html-eval-report.md)
  — the render pipeline this builds on.
- [plan-2026-05-31-shared-render-components.md](plan-2026-05-31-shared-render-components.md)
  — the shared-component / sync model the HTML format must respect.
- softschema (`github.com/jlevy/softschema`) — the Markdown-plus-YAML-frontmatter
  convention the `md` and canonical `.eval.md` artifacts follow.
- [SUPPLY-CHAIN-SECURITY.md](../../../../SUPPLY-CHAIN-SECURITY.md) — first-party
  exemption and pinning rules for `frontmatter-format`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
