---
title: Eval output improvements — finding locations in the panel, consistent YAML via frontmatter-format, structured export
description: Surface rule-finding location anchors in the interactive HTML panel, migrate EvalReport serialization to frontmatter-format for consistent YAML, and add a structured-export command so the full eval report is available as clean YAML (default) or JSON
author: Joshua Levy (github.com/jlevy) with LLM assistance
---
# Feature: Eval Output Improvements

**Date:** 2026-06-02

**Author:** Joshua Levy

**Status:** Superseded by
[plan-2026-06-03-reporting-cli-redesign.md](../active/plan-2026-06-03-reporting-cli-redesign.md)

> **Superseded.** This plan’s three threads (the `frontmatter-format` YAML writer, the
> whole-report structured export, and the finding-location anchors in the visual output)
> are carried forward, generalized to serve every output format, as phases of the
> reporting CLI redesign.
> Read that spec for the current plan; this doc is kept for the detailed
> `EVAL_REPORT_KEY_ORDER` derivation and background it records.

## Overview

Three related improvements to how a single-document Practical Prose evaluation is
serialized and rendered, all surfaced while running a real end-to-end eval of
[the Open Guide to Equity Compensation](https://github.com/jlevy/equity-compensation-e3)
(82 pages, scored 4.40 / 20 dims):

1. **Finding locations in the panel.** The interactive HTML render
   ([render_html/renderer.py](../../../../tools/pprose/src/pprose/render_html/renderer.py))
   drops the per-occurrence `locations` anchors (the verbatim quote + `§`-section
   pointers) that the scorer attaches to every rule finding.
   The assessment panel shows only the one-line finding description, so the evidence
   that ties a score to specific spots in the document never reaches the reader.

2. **Consistent YAML via frontmatter-format.** `EvalReport` serialization currently uses
   raw `pyyaml.safe_dump` with `sort_keys=True`
   ([eval_report.py](../../../../tools/pprose/src/pprose/eval_report.py)). Adopt
   [frontmatter-format](https://github.com/jlevy/frontmatter-format) (first-party,
   `jlevy` org) as the single consistent writer for both the `.eval.md` frontmatter and
   the standalone structured export, so YAML output is uniform, key-ordered logically,
   and round-trips cleanly.

3. **Structured export.** Add a new top-level `pprose show` command that displays the
   full validated `EvalReport` in any of three formats — **`mdyaml` (default), `yaml`,
   or `json`** — so the eval is consumable by other tools without parsing the Markdown
   body out of an `.eval.md` file.
   `show` is the read-only *display* sibling of `render` (which emits the visual HTML
   form); it is deliberately named generically so it can grow to display other artifact
   kinds later via input auto-detection.

## Goals

- The interactive panel shows, for each scored dimension, its finding(s) **and** the
  location anchors behind them (quote / section / line range), using the same compact
  rendering as the Markdown Violations list.
- All `EvalReport` YAML — the `.eval.md` frontmatter and the new structured export — is
  produced by one `frontmatter-format` code path with a single, logical key order.
- `pprose show <eval.md>` (top-level, read-only) prints the report in any of three
  formats: `mdyaml` (default) — Markdown with YAML frontmatter, the full `.eval.md`
  (structured frontmatter + rendered rollup body); `yaml` — the structured frontmatter
  only (pure YAML, no body); `json` — the same structured data as JSON. The format comes
  from `--format` (default `mdyaml`), or is inferred from the `--output` file extension
  when writing to a file.
- CLI surface follows the `python-cli-patterns` guideline: long flags only (no
  single-letter aliases — `--output`, not `-o`), `--format` for output shape, data to
  stdout and errors to stderr.
- Round-trip is preserved: anything written by the new writer is re-readable by
  `EvalReport.from_eval_md` / `from_yaml` and validates unchanged.
- The supply-chain policy is honored: `frontmatter-format` is pinned to an exact
  version, recorded under the standing first-party exemption in
  [SUPPLY-CHAIN-SECURITY.md](../../../../SUPPLY-CHAIN-SECURITY.md), with `uv.lock`
  committed (frozen install).

## Non-Goals

- No change to the scoring prompt or model behavior.
  In particular, this does **not** make the scorer emit *more* location anchors per
  finding (today it emits ~1 exemplar per finding); exhaustive per-occurrence
  enumeration is a separate future change.
- No change to the rubric, the 20 dimensions, the metrics, or the derived rollups.
- No new render variant or layout; only the existing `interactive` variant’s panel
  content gains the location anchors.
- No redesign of the `.eval.md` on-disk shape (still YAML frontmatter + Markdown body);
  only the YAML *writer* changes.

## Background

While running `pprose score` + `pprose render` on a large external document, the
rendered panel showed “just a few lines under the assessment panel” instead of the
per-occurrence evidence.
Tracing it:

- The scorer **does** attach `locations` to each `RuleFinding` (verified: 14 findings,
  14 anchors; e.g. Depth cites `🚧 Fill in details on QSBS` in `§Federal Taxes`). The
  data is present in the `.eval.md` frontmatter and rendered in the Markdown
  `## Violations` section by
  [eval_render.py](../../../../tools/pprose/src/pprose/eval_render.py)
  (`_format_locations`).
- But the HTML payload builder
  ([render_html/renderer.py](../../../../tools/pprose/src/pprose/render_html/renderer.py),
  the `findings_by_dim` loop) copies only `rule_number`, `verdict`, `description` — it
  omits `locations`. And the consuming component
  ([tip-panels.js](../../../../tools/pprose/src/pprose/render_html/js/_generated/tip-panels.js),
  source at
  [tools/render-components/tip-panels/tip-panels.js](../../../../tools/render-components/tip-panels/tip-panels.js))
  has no slot to render them.
  Confirmed against the generated HTML: finding descriptions appear; `§`-section anchors
  and quote text do not.

Separately, the question “do we have the raw JSON?” exposed that the only structured
output is the `.eval.md` frontmatter (YAML, embedded in a Markdown file) and
`pprose metrics --format json` (quant only).
There is no whole-report structured export.
`frontmatter-format` is the natural fit: it is the author’s own convention for “YAML
metadata on any text file”, it writes YAML consistently (`to_yaml_string` with optional
`key_sort`), and `fmf_write` / `fmf_read` directly model the YAML-frontmatter-plus-body
shape an `.eval.md` already is.

## Design

### Approach

One PR, two phases (Phase 2 is independent of Phase 1 and could land first; kept second
because Phase 1 is the larger, fixture-touching change).
Verify against the equity-compensation eval as the end-to-end smoke test.

### Components

- **`frontmatter-format` dependency.** Add `frontmatter-format==0.3.0` to
  [tools/pprose/pyproject.toml](../../../../tools/pprose/pyproject.toml) `dependencies`
  with a cool-off/first-party comment matching the existing `flowmark` / `pydantic-ai`
  precedent. Refresh `uv.lock`. Add a line to SUPPLY-CHAIN-SECURITY.md’s first-party
  record.

- **`EvalReport` serialization**
  ([eval_report.py](../../../../tools/pprose/src/pprose/eval_report.py)). Replace the
  `pyyaml.safe_dump` body of `to_yaml()` with `frontmatter-format`’s `to_yaml_string`,
  passing `key_sort=custom_key_sort(EVAL_REPORT_KEY_ORDER)` (a single module-level
  ordered list, mapped out under *Deterministic key ordering* below) rather than today’s
  alphabetical sort. `from_yaml` / `from_eval_md` / `_parse_frontmatter` read paths can
  stay on the existing parse or move to `fmf_read` / `from_yaml_string`; choose
  whichever keeps the round-trip stable and the validator unaffected.
  `to_eval_md` keeps emitting `---`-delimited frontmatter + body, preserving the current
  on-disk format.

- **`pprose show` command** — a new top-level command (its own module, e.g.
  `pprose/show.py`, registered in [cli.py](../../../../tools/pprose/src/pprose/cli.py)’s
  `COMMANDS` under the `Evaluate` group next to `render`). It loads + validates the
  input as an `EvalReport`, then prints one of three formats:
  - `mdyaml` (**default**) — the full `.eval.md`: structured YAML frontmatter + the
    rendered Markdown rollup body, via `to_eval_md` (which composes the
    `frontmatter-format` frontmatter with `render_single_doc_rollup`). This is the same
    artifact `from-metrics` / `score` write, reproduced from the validated model.
  - `yaml` — the structured frontmatter only (pure YAML, no Markdown body), via the
    `to_yaml` path.
  - `json` — the structured data as JSON (`model_dump(mode="json", exclude_none=True)` →
    `json.dumps(indent=2, ensure_ascii=False)`).

  Flags follow `python-cli-patterns` (long flags only, no single-letter aliases):
  `--format mdyaml|yaml|json` (default `mdyaml`) and `--output <path>` (default:
  stdout). When `--output` is given and `--format` is not, the format is inferred from
  the file extension (`.json` → json, `.yaml`/`.yml` → yaml, `.md` → mdyaml); an
  explicit `--format` always wins.
  Read-only; never mutates the input.
  Input-kind auto-detection is scoped to eval reports for now, with the dispatch left
  open so `show` can display other artifact kinds (e.g. a plain document’s metrics)
  later.

- **HTML panel finding locations**
  ([render_html/renderer.py](../../../../tools/pprose/src/pprose/render_html/renderer.py)
  + [tools/render-components/tip-panels/](../../../../tools/render-components/tip-panels/)).
    Add `locations` to each finding dict in the payload, formatted as a compact string
    with the same precedence as `eval_render._format_locations` (quote → section → line
    range → note). Update `tip-panels.js` to render the location string under each
    finding `<li>` (muted/secondary style, defined in `tip-panels.css`). Regenerate the
    `_generated/` mirrors with
    [sync_render_html_styles.py](../../../../tools/pprose/devtools/sync_render_html_styles.py).
    Reuse or lift `_format_locations` so the Markdown and HTML renderings stay
    identical.

### Deterministic key ordering

The order is one flat, module-level list `EVAL_REPORT_KEY_ORDER` passed to
`custom_key_sort`. `frontmatter-format` applies the resulting sort to **every** mapping
in the tree (listed keys first in list order; any unlisted key falls to natural /
alphabetical order — deterministic), so a single list governs all nesting levels.
The list is the depth-first walk of the schema below; it is fixed in code, not derived
from model declaration order, so reordering Pydantic fields never silently changes
output.

```
# top level
artifact, quant, qual, qual_reasons, rule_findings, derived, metadata, display

# artifact
label, path, commit_sha, scope_class

# quant → blocks, then each block's fields
size,    words, sentences, paragraphs, lines, pages_275wpp, bytes_kb
headings, h1, h2, h3, h4, h5, h6, total
structural, tables, code_blocks, images
links,   external, internal, inline, reference, autolink, bare_urls
provenance, bracket_tags, footnote_refs, footnote_defs
lint,    banned_register_hits
bracket_tag_examples

# qual AND qual_reasons share these group + dimension keys
purpose,   suitability, scope, breadth, depth
expression, clarity, coherence, concision
form,      organization, consistency, formatting
reasoning, discipline, soundness, precision, parsimony
grounding, verifiability, factuality, relevance
judgment,  calibration, fairness, robustness

# rule_findings[] → each finding, then each location
dimension, rule_number, verdict, description, locations
quote, section, line_start, line_end, note

# derived
density, words_per_sentence, words_per_paragraph, sentences_per_paragraph,
         tables_per_1k_words, tables_per_page, tags_per_1k_words, tags_per_page,
         links_per_1k_words, links_per_page
structure, h4_share_of_headings
rubric_rollup, purpose_mean, expression_mean, form_mean, reasoning_mean,
         grounding_mean, judgment_mean, overall_mean, assessed_dimensions,
         na_dimensions, err_dimensions
tally, bull, bear, neutral

# metadata
eval_date, evaluator, status, method, notes, rubric_version, model, model_id,
command, prompt_sha256, rubric_sha256, guidelines_sha256, artifact_sha256,
sdk_version, cache_stats
```

The single cross-context key is `total` (`headings` wants it last; `links` wants it
first). Listing it once, after `h6` and before the `links` leaf keys
(`external …bare_urls`), satisfies both: in `headings` it sorts after `h1..h6`; in
`links` its lower index sorts it ahead of `external`. No other key appears in two
mappings with a conflicting position.
Raw sub-dicts not in the schema (`metadata.cache_stats` inner keys, the `display`
table-style metadata) are unlisted and therefore natural-ordered — still deterministic.
A unit test asserts this exact order on a fully-populated fixture so it stays pinned.

### API Changes

- **New:** `pprose show <eval.md> [--format mdyaml|yaml|json] [--output <path>]`
  (top-level, read-only; default `mdyaml` — Markdown with YAML frontmatter; format
  inferred from `--output` extension when `--format` is omitted).
- **Changed (output formatting only):** `.eval.md` frontmatter key order becomes logical
  instead of alphabetical, and YAML quoting/scalar style follows `frontmatter-format`
  conventions. Semantically identical; re-reading any report yields the same
  `EvalReport`.
- **New dependency:** `frontmatter-format==0.3.0`.

## Implementation Plan

### Phase 1: frontmatter-format adoption + structured export

- [ ] Add `frontmatter-format==0.3.0` to `pyproject.toml` with cool-off/first-party
  comment; `uv sync` to refresh `uv.lock`; record in SUPPLY-CHAIN-SECURITY.md.
- [ ] Add the `EVAL_REPORT_KEY_ORDER` constant (per *Deterministic key ordering*) and
  migrate `EvalReport.to_yaml()` to `frontmatter-format`’s `to_yaml_string` with
  `key_sort=custom_key_sort(EVAL_REPORT_KEY_ORDER)`; keep `include_table_styles` intact.
- [ ] Confirm `to_eval_md` / `from_eval_md` / `from_yaml` round-trip is stable and the
  validator still recomputes `derived` correctly.
- [ ] Add top-level `pprose show` command (new module + `cli.py` registration under
  `Evaluate`) with `--format mdyaml|yaml|json` (default `mdyaml`; `mdyaml` via
  `to_eval_md`, `yaml` via `to_yaml`, `json` via `model_dump`) and `--output <path>`
  (long flags only, no `-o`; format inferred from extension when `--format` omitted).
- [ ] Re-serialize the 9 `.eval.md` fixtures under `tools/pprose/tests/fixtures/` and
  update any golden comparison output (`expected-comparison.md`, expected YAML) to the
  new key order. Confirm the diffs are formatting-only.
- [ ] Update / add unit tests: round-trip stability, `pprose show` mdyaml + yaml + json
  output (each parses back to the same `EvalReport`), key-order assertion.

### Phase 2: finding locations in the interactive panel

- [ ] Thread `locations` (compact-formatted, shared with `_format_locations`) into the
  finding payload in `render_html/renderer.py`.
- [ ] Render the location string under each finding in `tip-panels.js`; style it in
  `tip-panels.css`.
- [ ] Regenerate `_generated/` mirrors via `sync_render_html_styles.py`; confirm
  `make generate-check` is clean.
- [ ] Extend the HTML render tests (`test_render_html.py` / `test_rendered_html_e2e.py`)
  to assert a known location anchor reaches the rendered output.

## Testing Strategy

- **Unit:** round-trip (`from_eval_md(to_eval_md(r))` equals `r`) on a representative
  report; `pprose show` `mdyaml`, `yaml`, and `json` each parse back to the same object
  (mdyaml via `from_eval_md`, yaml via `from_yaml`, json via `model_validate`); logical
  key order is asserted; panel payload contains `locations`.
- **Golden:** the 9 fixture `.eval.md` files and the comparison golden re-serialize with
  formatting-only diffs (no semantic change); HTML e2e asserts a specific location quote
  / `§` anchor is present in the rendered page.
- **End-to-end smoke:** re-run `pprose render` on the equity-compensation `.eval.md`
  produced earlier and visually confirm the panel now shows location anchors; run
  `pprose show` and diff the YAML against the frontmatter.
- **Full gate:** `make generate` + `make lint` + `make test` clean;
  `make generate-check` confirms no generated-file drift.

## Rollout Plan

Single PR off `main`. Generated `_generated/` mirrors and re-serialized fixtures are
committed (consumers work after a clean clone with no build step).
The pre-commit hooks (flowmark + resources-sync + generate-check) gate the merge.
No migration needed for existing `.eval.md` files in the wild — they still parse; they
only re-serialize into the new key order the next time they are written.

## Open Questions

- ~~Should `pprose show` emit structured-only or the full `.eval.md`?~~ **Resolved:**
  support both, plus JSON. `pprose show` takes `--format mdyaml|yaml|json`, defaulting
  to `mdyaml` (Markdown with YAML frontmatter — the full `.eval.md`); `yaml` is the pure
  structured frontmatter; `json` is the structured data as JSON.
- ~~Nest the export under `report`, or make it top-level?~~ **Resolved:** top-level
  `pprose show`, a read-only *display* sibling of `render`, named generically so it can
  display other artifact kinds later.
  Flags follow `python-cli-patterns` (long flags only: `--format`, `--output`; no
  single-letter aliases).
- Do read paths (`from_yaml`) also move to `frontmatter-format`, or only the write path?
  Decide by whichever keeps the round-trip stable with least churn.
- ~~Is a logical key order worth the fixture churn vs.
  keeping alphabetical?~~ **Resolved:** yes — use the fixed, deterministic
  `EVAL_REPORT_KEY_ORDER` mapped under *Deterministic key ordering*, pinned by a unit
  test.

## References

- [plan-2026-05-29-static-html-eval-report.md](plan-2026-05-29-static-html-eval-report.md)
  — the render pipeline this builds on.
- [plan-2026-05-31-shared-render-components.md](../active/plan-2026-05-31-shared-render-components.md)
  — the shared-component / sync model the panel fix must respect.
- [frontmatter-format](https://github.com/jlevy/frontmatter-format) — checked out at
  `attic/frontmatter-format` (v0.3.0); `to_yaml_string`, `custom_key_sort`, `fmf_write`.
- [SUPPLY-CHAIN-SECURITY.md](../../../../SUPPLY-CHAIN-SECURITY.md) — first-party
  exemption and pinning rules.
- Source sites: `render_html/renderer.py` (`findings_by_dim` loop),
  `render_html/js/_generated/tip-panels.js` (assessment finding `<li>`),
  `eval_report.py` (`to_yaml` / `to_eval_md`), `eval_render.py` (`_format_locations`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
