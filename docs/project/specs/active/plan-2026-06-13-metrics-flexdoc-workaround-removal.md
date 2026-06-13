# Feature: Metrics Regex-to-Flexdoc Workaround Removal

**Date:** 2026-06-13 (last updated 2026-06-13)

**Author:** Joshua Levy with agent assistance

**Status:** Blocked (deferred) as of 2026-06-13. A trial migration found that flexdoc
0.1.0 cannot yet support a clean behavior-preserving swap: empirical testing across the
repo surfaced two flexdoc bugs and several API gaps (see
[Blocked on flexdoc 0.1.0](#blocked-on-flexdoc-010-2026-06-13) below), consolidated
upstream in [jlevy/flexdoc#6](https://github.com/jlevy/flexdoc/issues/6). The regex
implementation stays until a flexdoc release lands the fixes; resume from the
regex-to-API mapping table when it does.

> **Relationship to pp-3hg4.** This spec is the focused, do-it-now subset of the larger
> structural-metrics epic
> [plan-2026-05-25-structural-document-metrics.md](plan-2026-05-25-structural-document-metrics.md)
> (epic `pp-3hg4`). That epic is a **schema rewrite**: new `*_count` field names, a
> heading-outline artifact, prose-only `sentence_count` / `paragraph_count` semantics,
> distribution percentiles, and matching `eval_report.py` / `eval_compare.py` changes.
> **This spec is narrower and behavior-preserving**: keep the current `Metrics` field
> names and values, and only swap each hand-rolled regex for the flexdoc 0.1.0 typed API
> that already produces the same number.
> It exists because the regex workarounds were always meant to be temporary scaffolding
> for a document model that has now landed; the swap makes `metrics.py` smaller and more
> correct without committing to the full schema change.
> See [Relationship to pp-3hg4](#relationship-to-pp-3hg4) for how to track the two
> together.

## Blocked on flexdoc 0.1.0 (2026-06-13)

A trial migration against flexdoc 0.1.0, tested across all 61 Markdown files in the
repo, found the “mechanical, behavior-preserving swap gated by the reproducibility test”
premise does not hold.
Consolidated upstream as [jlevy/flexdoc#6](https://github.com/jlevy/flexdoc/issues/6);
pprose tracking beads are pp-bcrw (this migration, blocked), pp-zbzp (bug 1), and
pp-i23d (bug 2).

- **`collect()` / `node_table()` crash on valid Markdown**
  (`ValueError: layer nesting violated`) on 2 of 61 docs.
  It is the only typed path to inline elements (images, footnote refs, code spans), so
  the inline-node swaps in the mapping table below are blocked.
- **`sections()` / `toc()` silently drop headings** that `blocks()` finds (4 of 61 docs,
  including AGENTS.md), so a typed heading-by-level count is unreliable.
- **`filtered(...).reassemble()` drifts** the link-form and editorial-lint text on 20 of
  49 prose docs (links inside tables vanish; em dashes appear or disappear from
  whitespace normalization), so it cannot feed the regexes this spec keeps
  byte-identical.
- **API gaps:** no heading-level accessor on `Block`; no link-form discriminator or
  reference-definition surfacing (flexdoc#5); no inline-code-stripped prose projection.

The one confirmed improvement: `blocks()` counts tables and code blocks more correctly
than the old regexes (it catches indented and `~~~`-fenced code that `CODE_FENCE_RE`
missed, and stops counting `#` lines inside those blocks as headings).
That is a behavior change, not a no-op, so it also waits for the migration proper rather
than landing piecemeal.

## Overview

[tools/pprose/src/pprose/metrics.py](../../../../pprose/src/pprose/metrics.py) parses
each Markdown document twice.
Word, sentence, paragraph, and line counts already come from flexdoc
(`FlexDoc.from_text(...).size(TextUnit.{words,sentences,paragraphs,lines})`).
**Everything else is hand-rolled regex**: headings (ATX and setext), links by markdown
form, footnotes, images, inline code, ALL-CAPS bracket tags, bare URLs, tables, code
fences, the frontmatter strip, and the editorial lint patterns.

flexdoc 0.1.0 — the standalone document-layer package pprose migrated to from chopdiff
(see [chopdiff-upstream-requests.md](../../chopdiff-upstream-requests.md), now
superseded) — exposes a typed document model that makes most of those regexes
unnecessary: `FlexDoc.frontmatter`, `FlexDoc.filtered(...)`, `FlexDoc.sections()`,
`FlexDoc.blocks()` with `code_info` / `table_info` / `list_info`, and
`FlexDoc.collect(...)` / `FlexDoc.links()` for typed inline nodes.

The goal of this cleanup is a single, smaller, more correct `metrics.py`: replace each
structural regex with the typed API that yields the same count, parse the document once
through flexdoc, and keep only the regexes that flexdoc genuinely does not (and should
not) cover.
The observable output of `pprose metrics` stays the same except where a typed
parse is strictly more correct than the regex it replaces, and those few changes are
caught and blessed by the existing fixture-locked reproducibility test.

This is **not** the pp-3hg4 schema rewrite: no field renames, no new `*_count` fields,
no `eval_report` / `eval_compare` changes, no heading-outline artifact, no distribution
percentiles. Those stay in pp-3hg4.

## Goals

- **Single parse.** Build one `FlexDoc` per document and derive every structural metric
  from it; no separate regex sweep over the raw text for structure.
- **Behavior-preserving.** Keep the existing `Metrics` dataclass field names and (within
  the tolerances documented below) values.
  The fixture-locked `TestB14_ReproducibilityRegression` is the contract: any drift must
  be intentional and blessed.
- **Smaller, more correct `metrics.py`.** Replace `strip_code_and_frontmatter` and the
  structural regexes with flexdoc accessors.
  Drive the lint patterns off flexdoc’s prose-only `filtered(...).reassemble()` text
  instead of the ad-hoc strip.
- **No over-promising.** Keep as regex exactly the things flexdoc does not model:
  link-form breakdown, internal-vs-external URL classification, and the editorial lint
  patterns. State clearly which these are and why.

## Non-Goals

- The pp-3hg4 `*_count` field rename and schema rewrite, the heading-outline artifact,
  prose-only `sentence_count` / `paragraph_count` re-definition, and distribution
  percentiles. Out of scope here; tracked in pp-3hg4.
- `eval_report.py` and `eval_compare.py` changes.
  They read the current field names and this cleanup does not rename anything, so they
  are untouched.
- The planned two-phase linter
  ([plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md](plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md)).
  flexdoc’s exact offsets enable a better linter, but building it is separate work.
- Any new CLI flag, output format, or human-readable layout change.
- Resolving the link-form gap by adopting coarser link counts.
  That is a deliberate decision point (see below), not a default of this cleanup.

## Background

### Current pipeline

`measure()` reads the raw text, runs `strip_code_and_frontmatter` (a `FRONTMATTER_RE`
sub, a `CODE_FENCE_RE` sub, and a `CODE_INLINE_RE` sub) to get a `structural` string,
then runs roughly a dozen independent regexes over that string (and a couple over the
raw text) plus one `FlexDoc.from_text(structural)` parse for the size counts.
The size counts are the only structurally-aware numbers; every other count is a regex
tally.

### What flexdoc 0.1.0 provides (verified against the published 0.1.0 wheel)

These were checked empirically against the shipped wheel, not inferred from docs:

- `FlexDoc.frontmatter` — isolates a leading `---` YAML block; frontmatter is
  auto-excluded from `paragraphs` and all sizes.
  Replaces `FRONTMATTER_RE` stripping.
- `FlexDoc.filtered(include={BlockType...})` — a prose-only sub-document.
  Choosing `{paragraph, list, ordered_list, blockquote, footnote}` gives clean word /
  sentence / paragraph text and a `.reassemble()` string for the lint patterns.
  Replaces `strip_code_and_frontmatter` plus the manual code stripping.
- `FlexDoc.sections()` — a `Section` tree with `.title`, `.level`,
  `.size(unit, subtree=)`, `.blocks()`, and rollups; plus `FlexDoc.toc()` and
  `section_size_tree()`. With `Paragraph.heading_level() -> int | None` and
  `heading_title() -> str` per block, this replaces `HEADING_RE` / `SETEXT_H1_RE` /
  `SETEXT_H2_RE` for the heading counts and lets the generic-heading lint run against
  real heading text.
- `FlexDoc.blocks()` — a structural `Block` tree.
  Each `Block` carries `.type` (`BlockType`), `.code_info` (`CodeInfo`: language,
  line_count), `.table_info` (`TableInfo`: rows, cols, cells, alignments), and
  `.list_info` (`ListInfo`: ordered, start, max_depth, item_count). Replaces
  `CODE_FENCE_RE` and `TABLE_SEP_RE` for counting code blocks and tables, with language
  and table/list substructure available for free.
- `FlexDoc.collect(kinds={NodeKind.X}, recursive=True)` — typed inline nodes with exact
  spans and attrs. Verified for `footnote_ref` (attrs include `label`), `link` (attrs
  `url`, `text`), `image` (attrs `url`, `text`), `code_span` (attrs `content`), and the
  block kinds. **Gotcha (must be honored in code and documented in the docstring):**
  inline collection requires `recursive=True`. `collect(kinds={link}, inline=True)`
  alone returns `[]` because candidates default to root (block) nodes.
- `FlexDoc.links()` — `list[Link(text, url, title, span)]` document-wide, with reference
  links resolved.
- Exact offsets (`Offsets.doc_offset`) on every node, sentence, and paragraph, plus
  `sentence_at_offset` and `paragraph_at_offset`. Not needed for this cleanup, but the
  groundwork for the future linter.

### What flexdoc 0.1.0 does not provide (stays as pprose-side logic)

Stated explicitly so this spec does not over-promise:

- **Link-form breakdown.** flexdoc unifies inline links, autolinks, and reference-use
  links as a single `NodeKind.link` with attrs `{url, text}` and no form discriminator.
  Bare URLs are returned *as* links (GFM autolinking).
  Reference *definitions* (`[id]: url`) are not surfaced at all.
  So `links_inline`, `links_autolink`, `links_reference_use`,
  `links_reference_definitions`, and `bare_urls` cannot be derived from flexdoc today.
  This gap is filed upstream as
  [jlevy/flexdoc#5](https://github.com/jlevy/flexdoc/issues/5) (link-form discriminator
  plus reference-definition surfacing).
- **Internal-vs-external URL classification.** flexdoc gives the URL; the
  external/internal split is a pprose editorial policy.
  `classify_url` stays.
- **Editorial lint patterns.** Banned register, spaced and total em-dash discipline,
  replacement-history phrases, pedantic-marker phrases, and ALL-CAPS bracket tags are
  not document structure.
  They stay as regex but should run against the flexdoc prose-only
  `filtered(...).reassemble()` text rather than the current ad-hoc strip.
  The generic-heading check moves onto real `heading_title()` text.

## Design

### Approach

One focused PR. Rebuild `measure()` around a single `FlexDoc`; replace each structural
regex with its typed equivalent; keep the link-form, URL-classification, and lint
regexes but feed the lint regexes the flexdoc prose-only text.
Re-bless the four reproducibility fixtures if and only if a typed parse produces a more
correct number than the regex it replaced.

### Regex-to-API mapping

Every current behavior in `metrics.py`, the flexdoc 0.1.0 API that replaces it, and the
disposition.
“Replace” = drop the regex for the typed API. “Keep-as-regex” = flexdoc does
not (and should not) model it.
“Blocked on flexdoc#5” = a decision point — keep regex until upstream lands a
discriminator.

| Current metric / regex | flexdoc 0.1.0 API | Disposition | Notes |
| --- | --- | --- | --- |
| `FRONTMATTER_RE` strip | `FlexDoc.frontmatter` (auto-excluded from sizes/paragraphs) | **Replace** | Frontmatter no longer needs stripping before counting; it is already excluded. |
| `strip_code_and_frontmatter` (frontmatter + fences + inline code) | `FlexDoc.filtered(include={paragraph, list, ordered_list, blockquote, footnote}).reassemble()` | **Replace** | Single prose-only text source for the lint patterns; code and frontmatter excluded by construction. |
| `HEADING_RE` (ATX h1-h6) | `Paragraph.heading_level()` / `FlexDoc.sections()` | **Replace** | Per-block heading level from the parser, not `^#{1,6}`. |
| `SETEXT_H1_RE` / `SETEXT_H2_RE` (setext underline) | `Paragraph.heading_level()` / `FlexDoc.sections()` | **Replace** | The parser resolves setext headings; removes the phantom-HR false-positive limitation. |
| `count_headings` totals + by-level dict | walk `heading_level()` over blocks | **Replace** | Same `headings` dict shape; values from typed levels. |
| `INLINE_LINK_RE` (`[t](u)`) | `FlexDoc.collect(kinds={link}, recursive=True)` / `FlexDoc.links()` | **Blocked on flexdoc#5** | flexdoc has no inline-vs-other discriminator; keep regex for the per-form count. |
| `AUTOLINK_RE` (`<http…>`) | (unified into `NodeKind.link`) | **Blocked on flexdoc#5** | No autolink discriminator; bare URLs also arrive as links. Keep regex. |
| `REF_LINK_USE_RE` (`[t][id]`) | (unified into `NodeKind.link`, resolved) | **Blocked on flexdoc#5** | Reference *use* is indistinguishable from inline once resolved. Keep regex. |
| `REF_LINK_DEF_RE` (`[id]: url`) | — (not surfaced) | **Keep-as-regex** | flexdoc does not surface reference *definitions* at all. Keep regex. |
| `BARE_URL_RE` (plain `http(s)://…`) | (returned as `NodeKind.link` via GFM autolinking) | **Keep-as-regex** | flexdoc would count bare URLs as links; the “bare, unwrapped” semantic is pprose-specific. Keep regex. |
| `classify_url` (external vs internal) | `Link.url` provides the URL only | **Keep-as-regex** | URL scheme policy is pprose editorial, not document structure. |
| `links_external` / `links_internal` | derived from the per-form regex + `classify_url` | **Keep-as-regex** | Depends on the per-form regexes above; moves only if flexdoc#5 lands. |
| `IMAGE_RE` (`![t](u)`) | `FlexDoc.collect(kinds={image}, recursive=True)` (attrs `url`, `text`) | **Replace** | Typed image nodes; no `!\[…\]\(…\)` regex. |
| `CODE_INLINE_RE` (inline `` `…` ``) | `FlexDoc.collect(kinds={code_span}, recursive=True)` (attr `content`) | **Replace** | Used both for stripping (now via `filtered`) and as inline-code presence; typed. |
| `FOOTNOTE_REF_RE` (`[^id]`) | `FlexDoc.collect(kinds={footnote_ref}, recursive=True)` (attr `label`) | **Replace** | Typed inline footnote refs. Note the count semantics change below. |
| `FOOTNOTE_DEF_RE` (`^[^id]:`) | `FlexDoc.blocks()` footnote blocks (`BlockType.footnote`) | **Replace** | Footnote definitions are typed footnote blocks. |
| `BRACKET_TAG_RE` (`[ALLCAPS]`) | run regex over `filtered(...).reassemble()` | **Keep-as-regex** | An ALL-CAPS heuristic, not a markdown construct. Keep regex, fed prose-only text. |
| `TABLE_SEP_RE` (separator rows) | `FlexDoc.blocks()` table blocks / `Block.table_info` | **Replace** | Count `BlockType.table`; `table_info` adds rows/cols/cells for free (used by pp-3hg4). |
| `CODE_FENCE_RE` (fenced blocks) | `FlexDoc.blocks()` code blocks / `Block.code_info` | **Replace** | Count `BlockType.code`; `code_info` adds language/line_count for free (used by pp-3hg4). |
| words / sentences / paragraphs / lines | `FlexDoc.from_text(...).size(TextUnit.X)` (already used) | **Already flexdoc** | No change; must not drift. |
| `GENERIC_HEADING_RE` | regex over `heading_title()` text | **Replace (onto typed text)** | Run the generic-word check against real heading titles, not `^#{1,6}\s+…`. |
| `DEFAULT_BANNED_RE` (banned register) | run regex over `filtered(...).reassemble()` | **Keep-as-regex** | Editorial lint, not structure. Fed prose-only text. |
| `SPACED_EM_DASH_RE` (`" — "`) | run regex over `filtered(...).reassemble()` | **Keep-as-regex** | Editorial lint. Fed prose-only text. |
| `EM_DASH_RE` (total em dashes) | run regex over `filtered(...).reassemble()` | **Keep-as-regex** | Editorial lint. Fed prose-only text. |
| `REPLACEMENT_HISTORY_RE` | run regex over `filtered(...).reassemble()` | **Keep-as-regex** | Editorial lint. Fed prose-only text. |
| `PEDANTIC_MARKER_RE` | run regex over `filtered(...).reassemble()` | **Keep-as-regex** | Editorial lint. Fed prose-only text. |

### What stays regex, and why

Three groups stay regex on purpose:

1. **Link-form metrics (`links_inline`, `links_autolink`, `links_reference_use`,
   `links_reference_definitions`, `bare_urls`).** flexdoc collapses all link forms into
   a single typed `link` node with `{url, text}` and surfaces no reference definitions,
   so the form breakdown is not derivable.
   This is the one **decision point**: either keep these regexes (default for this
   cleanup, preserving the current granular output), or accept a coarser single
   `link_count` and drop the breakdown — which should wait until
   [jlevy/flexdoc#5](https://github.com/jlevy/flexdoc/issues/5) lands a form
   discriminator and reference-definition surfacing.
   Recommendation: keep the regexes now; revisit when flexdoc#5 ships.
2. **Internal-vs-external URL classification (`classify_url`, `links_external`,
   `links_internal`).** flexdoc hands back the URL; the scheme-based external/internal
   split is pprose policy.
   Keep.
3. **Editorial lint patterns** (banned register, spaced and total em dashes, replacement
   history, pedantic markers, ALL-CAPS bracket tags).
   These are register and discipline checks, not document structure.
   They stay as regex but switch their input from the ad-hoc
   `strip_code_and_frontmatter` string to flexdoc’s prose-only
   `filtered(...).reassemble()`. The generic-heading check is the one lint that gets
   *more* structural: it runs over real `heading_title()` text instead of an
   `^#{1,6}\s+…` regex.

### Components

- [tools/pprose/src/pprose/metrics.py](../../../../pprose/src/pprose/metrics.py) — the
  only code file changed.
  Rebuild `measure()` around one `FlexDoc`; delete `strip_code_and_frontmatter`,
  `count_headings`, and the replaced structural regex constants (`HEADING_RE`,
  `SETEXT_*_RE`, `IMAGE_RE`, `CODE_INLINE_RE`, `FOOTNOTE_REF_RE`, `FOOTNOTE_DEF_RE`,
  `TABLE_SEP_RE`, `CODE_FENCE_RE`, `FRONTMATTER_RE`, `GENERIC_HEADING_RE` in its current
  form). Keep the link-form, `classify_url`, and lint regexes.
  Update the module docstring’s Known Limitations (several limitations — setext phantom
  HRs, the inline-code strip heuristic — go away).
  Document the `recursive=True` collect gotcha in the docstring.
- Fixtures under `tools/pprose/tests/test_fixtures/practical_prose_metrics/expected/` —
  re-blessed only if a count legitimately changes.
- No changes to `eval_report.py`, `eval_compare.py`, CLI flags, or output formats.

### API Changes

None. `Metrics` field names and the CLI surface are unchanged.
This is an internal implementation swap.

## Implementation Plan

Single phase; the swap is mechanical and gated by the reproducibility test.

### Phase 1: Swap structural regexes for flexdoc typed APIs

- [ ] Build one `FlexDoc` in `measure()`; derive frontmatter exclusion from
  `FlexDoc.frontmatter` and keep the size counts as-is (already flexdoc).
- [ ] Replace heading counting with `heading_level()` / `sections()`; drop `HEADING_RE`,
  `SETEXT_H1_RE`, `SETEXT_H2_RE`, and `count_headings`.
- [ ] Replace images, inline-code, footnote refs, footnote defs, tables, and code fences
  with `collect(...)` / `blocks()` (`code_info`, `table_info` available but not surfaced
  as new fields here).
  Honor `recursive=True` on every inline `collect`.
- [ ] Build the prose-only text once via
  `filtered(include={paragraph, list, ordered_list, blockquote, footnote}).reassemble()`
  and feed it to the banned-register, em-dash, replacement-history, pedantic-marker, and
  bracket-tag regexes.
  Drop `strip_code_and_frontmatter`.
- [ ] Move the generic-heading check onto `heading_title()` text.
- [ ] Keep `INLINE_LINK_RE`, `AUTOLINK_RE`, `REF_LINK_USE_RE`, `REF_LINK_DEF_RE`,
  `BARE_URL_RE`, and `classify_url` for the link-form and external/internal metrics
  (blocked on flexdoc#5). Add a code comment pointing at flexdoc#5.
- [ ] Update the module docstring: rewrite Known Limitations, note which metrics are now
  typed, and document the `recursive=True` collect gotcha.
- [ ] Run the test suite; re-bless reproducibility fixtures only for intentional changes
  (procedure below).

## Testing Strategy

The fixture-locked `TestB14_ReproducibilityRegression`
([tools/pprose/tests/test_metrics.py](../../../../pprose/tests/test_metrics.py)) is the
behavior-parity contract.
It compares the full `Metrics` YAML for four fixtures (`all_headings`, `links_mixed`,
`frontmatter_and_code`, `banned_register`) against pinned expected files and fails
loudly on any drift.

**Expected to stay byte-identical:**

- `words`, `sentences`, `paragraphs`, `lines`, `pages` — already computed via flexdoc;
  this cleanup does not touch the size path, so they must not move.
- The link-form metrics (`links_inline`, `links_autolink`, `links_reference_use`,
  `links_reference_definitions`, `bare_urls`, `links_external`, `links_internal`) —
  their regexes are unchanged; only their input text could differ, and they already ran
  over the stripped `structural` text.
- The lint metrics — same regexes; verify the prose-only `filtered(...).reassemble()`
  text yields identical hits on the fixtures (the existing tests already assert
  code-fenced and inline-code tags/words are excluded, so this is the main thing to
  confirm).

**May intentionally change (re-bless if so):**

- `headings` / `headings_total` if a fixture had a setext edge case that the parser
  resolves differently from `SETEXT_*_RE` (e.g. a phantom-HR case the old regex
  miscounted).
- `footnote_references` — the regex currently matches `[^id]` in *both* references and
  definition lines (see `TestFootnotes`: 3 refs but 6 ref-matches).
  The typed `collect(kinds={footnote_ref})` may count only true inline references.
  If the count changes, this is a *more correct* value — re-bless and update the
  `TestFootnotes` expectation with a comment explaining the typed-vs-regex difference.
- `images` / `code_blocks` / `tables` if the typed parse disagrees with the regex on any
  fixture (it should agree on the current fixtures).

**Re-bless procedure** (from the test docstring): for each changed fixture, regenerate
its expected YAML —

```
uv run pprose metrics \
  tests/test_fixtures/practical_prose_metrics/<fixture>.md --format=yaml \
  > tests/test_fixtures/practical_prose_metrics/expected/<fixture>.yaml
```

— then inspect the diff field-by-field and confirm each change is the typed parse being
more correct (not a regression) before committing.
Update the targeted assertions in `TestP1_4_SetextHeadings`, `TestFootnotes`,
`TestP2_8_TablesAndCodeBlocks`, and the links/bracket-tag tests if their expectations
move, with a comment giving the reason.

**Sanity sweep:** run `pprose metrics` across `docs/`, `runbooks/`, `shortcuts/`, and
`skills/` on `main` and on the branch; confirm the only diffs are the intended
typed-parse corrections, and stash the comparison in the PR body.

## Risks and Edge Cases

- **Setext headings.** The old regex treats any `===` / `---` line under non-empty text
  as a heading, producing phantom h1/h2 under prose followed by a matching HR. The
  parser is correct, so the heading counts can drop on documents that previously
  triggered the false positive.
  Treat any change as a correction, re-bless, and note it.
- **Bare URL vs link semantics.** flexdoc GFM-autolinks bare URLs into `link` nodes, so
  a flexdoc-based bare-URL count would *not* match pprose’s “unwrapped URL” definition.
  This is exactly why `BARE_URL_RE` stays.
  Do not route bare-URL counting through flexdoc.
- **Footnote-reference double counting.** The current regex counts `[^id]` in definition
  lines too; the typed node count likely will not.
  Decide the intended semantic (true inline references is the more defensible one),
  re-bless, and update `TestFootnotes`.
- **List paragraph coarseness.** A tight list is a single `list` / `ordered_list` block
  in the prose view. This cleanup does not change paragraph semantics (that is pp-3hg4),
  but the prose-only `filtered(...)` text must include `list` and `ordered_list` so list
  prose still reaches the lint patterns.
  The `PROSE_KINDS` set is load-bearing.
- **Frontmatter edge cases.** `FlexDoc.frontmatter` isolates a *leading* `---` block;
  confirm a document with no frontmatter, a `* * *` thematic break, or a mid-document
  `---` is handled the same as before (the old `FRONTMATTER_RE` is anchored at `\A`, so
  behavior should match).
- **`recursive=True` gotcha.** Forgetting it on any inline `collect` silently returns
  `[]` and zeroes a metric.
  The reproducibility test catches it on the fixtures, but the docstring note and a code
  comment are the durable guard.

## Relationship to pp-3hg4

This cleanup is a **milestone of the pp-3hg4 epic**, not a competitor to it.
It does the mechanical regex-to-typed-API swap with behavior preserved; pp-3hg4 then
builds the schema rewrite (`*_count` fields, prose-only count re-definition, heading
outline, distributions, `eval_report` / `eval_compare` updates) on top of an
already-typed `metrics.py`. Doing this first shrinks pp-3hg4’s surface and de-risks it:
the schema rewrite no longer has to also remove regexes.

**Recommended tracking (do not create beads from this spec — recommendation only):**

- Link a focused bead to this spec via
  `--spec plan-2026-06-13-metrics-flexdoc-workaround-removal.md`, as a child of epic
  `pp-3hg4`.
- Suggested bead breakdown (one PR, but separable beads if useful):
  1. Headings via `heading_level()` / `sections()`; drop ATX/setext regexes.
  2. Images, inline code, footnote refs/defs, tables, code fences via `collect()` /
     `blocks()`.
  3. Lint patterns onto `filtered(...).reassemble()`; generic-heading onto
     `heading_title()`.
  4. Docstring rewrite, fixture re-bless, sanity sweep.
- File the link-form decision (keep regex vs adopt coarse counts) as a separate bead
  blocked on [jlevy/flexdoc#5](https://github.com/jlevy/flexdoc/issues/5); it should not
  hold up this cleanup.

## Out of Scope

- The `Metrics` `*_count` field rename and the full schema rewrite — pp-3hg4.
- `eval_report.py` density-math and `eval_compare.py` column changes — pp-3hg4 (this
  cleanup renames nothing, so they are untouched).
- The planned two-phase linter — its own spec
  ([plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md](plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md)).
- Surfacing `code_info` / `table_info` / `list_info` substructure as new metric fields —
  the typed objects are available, but exposing them is a pp-3hg4 addition.
- Adopting a coarse single `link_count` — deferred to the flexdoc#5 decision.

## References

- [tools/pprose/src/pprose/metrics.py](../../../../pprose/src/pprose/metrics.py)
- [tools/pprose/tests/test_metrics.py](../../../../pprose/tests/test_metrics.py) —
  `TestB14_ReproducibilityRegression` and the re-bless procedure.
- [plan-2026-05-25-structural-document-metrics.md](plan-2026-05-25-structural-document-metrics.md)
  — the broader pp-3hg4 schema-rewrite epic this cleanup feeds.
- [chopdiff-upstream-requests.md](../../chopdiff-upstream-requests.md) — superseded
  per-capability history; flexdoc 0.1.0 satisfies all five chopdiff requests.
- [jlevy/flexdoc#5](https://github.com/jlevy/flexdoc/issues/5) — link-form discriminator
  and reference-definition surfacing (blocks the link-form metrics’ move off regex).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
