# Handoff: metrics regex -> flexdoc workaround removal (2026-06-13)

> **Status update (2026-06-13): BLOCKED on flexdoc 0.1.0; migration deferred.** A trial
> migration found flexdoc 0.1.0 is not yet a clean drop-in: `collect()`/`node_table()`
> crash on valid Markdown (blocking typed inline-element access), `sections()`/`toc()`
> drop headings that `blocks()` finds, and `filtered(...).reassemble()` drifts the
> link/lint text on real docs.
> All consolidated upstream as
> [jlevy/flexdoc#6](https://github.com/jlevy/flexdoc/issues/6); see the spec’s
> [Blocked on flexdoc 0.1.0](../specs/active/plan-2026-06-13-metrics-flexdoc-workaround-removal.md#blocked-on-flexdoc-010-2026-06-13)
> section. The regex implementation stays until a flexdoc release lands the fixes.
> The guidance below applies once it does.

**Task:** Implement the behavior-preserving cleanup that replaces the hand-rolled regex
parsing in pprose’s metrics with flexdoc 0.1.0’s typed document model.
pprose has already migrated off chopdiff onto flexdoc; this is the follow-on “drop the
now-unnecessary workarounds” work.

**Spec (read first):**
[docs/project/specs/active/plan-2026-06-13-metrics-flexdoc-workaround-removal.md](../specs/active/plan-2026-06-13-metrics-flexdoc-workaround-removal.md)
— has the full regex -> flexdoc-API mapping table, the “what stays regex and why”
section, the parity/testing contract, and the risk list.
The broader schema rewrite it is a subset of is
[plan-2026-05-25-structural-document-metrics.md](../specs/active/plan-2026-05-25-structural-document-metrics.md)
(epic `pp-3hg4`); **do not** pull the `*_count` rename / `eval_report` changes /
distribution percentiles into this cleanup — those stay in pp-3hg4.

**Beads:** Epic `pp-3hg4` (open).
The five cleanup items map to existing beads `pp-9cmv` (code_info), `pp-eaa2`
(table_info), `pp-tg93` (list_info), `pp-4hku` (frontmatter), `pp-aat4` (footnote_ref) —
originally filed as chopdiff upstream requests, now all satisfied by flexdoc 0.1.0, so
they convert to workaround-removal against a dependency we already ship.
Create/relabel beads under `pp-3hg4` as needed; synced.

**Branch / PR:** The migration lives on `post-release-cleanup` (from `main`), in **PR
#28** (<https://github.com/jlevy/practical-prose/pull/28>), CI green, MERGEABLE/CLEAN.
Start this cleanup on a **fresh branch off `main` once #28 merges** — it is independent
of the release-prep changes still in flight on that branch (a `DISCOVERY_VERSION` 0.1.1
-> 0.2.0 bump for the 0.2.0 tag).

**Git:** Only `tools/pprose/src/pprose/metrics.py` is touched by this work.
Don’t refactor the `Metrics` dataclass field names (that’s pp-3hg4).

## Context — verified flexdoc 0.1.0 facts (empirically checked against the published wheel)

`metrics.py` today imports `from flexdoc import FlexDoc, TextUnit` and uses **only**
`FlexDoc.from_text(strip_code_and_frontmatter(raw)).size(TextUnit.{words,sentences,paragraphs,lines})`.
Everything else is regex.
The replacements:

- **Frontmatter:** `FlexDoc.frontmatter` (auto-excluded from `paragraphs`/sizes)
  replaces `FRONTMATTER_RE`. Drop `strip_code_and_frontmatter`; build prose-only text
  once with
  `doc.filtered(include={BlockType.paragraph, list, ordered_list, blockquote, footnote}).reassemble()`.
- **Headings:** `doc.sections()` / `Paragraph.heading_level()` / `heading_title()`
  replace `HEADING_RE` + the setext regexes.
  Run the generic-heading check on real `heading_title()` text.
- **Blocks:** `doc.blocks()` -> `Block.type` + `Block.code_info` (language, line_count),
  `Block.table_info` (rows, cols, cells, alignments), `Block.list_info` (ordered, start,
  max_depth, item_count). Replaces `CODE_FENCE_RE`, `TABLE_SEP_RE`.
- **Inline:** `doc.collect(kinds={NodeKind.X}, recursive=True)` for `image`,
  `code_span`, `footnote_ref` (attrs include `label`), and `link`. **GOTCHA:** inline
  collection needs `recursive=True`; `collect(kinds={link}, inline=True)` alone returns
  `[]` because candidates default to block roots.
  Footnote definitions are `BlockType.footnote` via `blocks()`.

**Two findings to act on:**
1. **`FOOTNOTE_REF_RE` double-counts** `[^id]` on definition lines (the current test
   expects 6 ref matches for 3 real refs).
   The typed `collect({footnote_ref})` returns the correct smaller count, so
   `TestFootnotes` + the footnote fixture in `TestB14` must be **re-blessed** (this is
   an intended, more-correct change, not a regression).
2. **Link-form breakdown stays regex.** flexdoc collapses inline/autolink/bare/reference
   links into one `NodeKind.link` with no form attribute, returns bare URLs as links,
   and does not surface `[id]: url` definitions.
   So
   `links_inline / links_autolink / links_reference_use / links_reference_definitions / bare_urls`
   and `classify_url` (internal vs external) **keep their regexes**. This gap is filed
   upstream as **[jlevy/flexdoc#5](https://github.com/jlevy/flexdoc/issues/5)**; revisit
   if it lands.

**Stays regex regardless** (editorial lint patterns, not document structure): banned
register, spaced/total em-dash discipline, replacement-history phrases, pedantic
markers, ALL-CAPS bracket tags.
Run them over the flexdoc prose-only `filtered(...).reassemble()` text instead of the
old ad-hoc strip.

## Parity contract / testing

`tools/pprose/tests/test_metrics.py` :: `TestB14_ReproducibilityRegression` is the
guard. Words/sentences/paragraphs/lines already come from flexdoc, so they must **not**
drift.
Headings (setext phantom-HR edge) and footnote refs (the double-count fix) **may**
change; bless intentionally and inspect the diff.
Re-bless one fixture with:

```
cd tools/pprose && uv run pprose metrics \
  tests/test_fixtures/practical_prose_metrics/<fixture>.md --format=yaml \
  > tests/test_fixtures/practical_prose_metrics/expected/<fixture>.yaml
```

Run `uv run pytest` (full suite was 326 green before this work) and
`uv run basedpyright src/pprose/metrics.py`.

## References / setup

- flexdoc source for API spelunking: `attic/flexdoc/` (gitignored local checkout of
  0.1.0). Key files: `src/flexdoc/docs/flex_doc.py`, `block_tree.py`, `block_info.py`,
  `collect.py`, `node.py` (NodeKind enum), `links.py`. `docs/usage.md` and
  `docs/flexdoc-spec.md` for the model.
- flexdoc is already a pinned dep (`flexdoc==0.1.0` in `tools/pprose/pyproject.toml`);
  no setup needed beyond `uv sync`.
- The superseded design history (per-capability) is in
  [docs/project/chopdiff-upstream-requests.md](../chopdiff-upstream-requests.md).
