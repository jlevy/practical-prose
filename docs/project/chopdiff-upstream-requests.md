---
title: chopdiff upstream feature requests (from pprose metrics work)
description: The document-model API gaps pprose worked around on chopdiff 0.3.1, filed as jlevy/chopdiff#18-#22. All five are satisfied by the flexdoc 0.1.0 migration; kept as the design record for the workaround-removal work (epic pp-3hg4).
date: 2026-06-02
last_updated: 2026-06-13
status: superseded
---
# chopdiff Upstream Feature Requests

> **Update (2026-06-13): superseded by the flexdoc migration.** These were
> document-model requests, and that model is now the standalone **flexdoc** package
> (chopdiff’s `TextDoc` became `flexdoc.FlexDoc`). pprose migrated from
> `chopdiff==0.3.1` to `flexdoc==0.1.0` and dropped chopdiff entirely.
> flexdoc 0.1.0 ships **all five** requests below: **#1 `code_info`**, **#2
> `table_info`**, and **#3 `list_info`** are typed metadata on `flexdoc.docs.Block`
> (`block.code_info` / `.table_info` / `.list_info`); **#5 frontmatter isolation** is
> `FlexDoc.frontmatter` (excluded from `paragraphs` and all prose counts); and **#4
> `NodeKind.footnote_ref`** is implemented as a typed inline node, reachable via
> `doc.collect(kinds={NodeKind.footnote_ref}, recursive=True)` (verified against the
> 0.1.0 wheel). No flexdoc requests remain open; the broader pprose use case and a few
> narrower, newly-identified gaps (link-form discriminator, reference-definition
> surfacing) are filed as [jlevy/flexdoc#5](https://github.com/jlevy/flexdoc/issues/5).
> 
> The capabilities exist; pprose has **not yet adopted** them — `metrics.py` still uses
> its own regex workarounds for code/table/list/footnote counts.
> Dropping those in favor of flexdoc’s block and inline APIs is the remaining
> structural-metrics work (epic `pp-3hg4`). The per-request detail below is preserved as
> the design record; mentally substitute `FlexDoc` for `TextDoc` and `Block` for
> `Paragraph`.

After upgrading pprose to **chopdiff 0.3.1**, an audit against the structural-metrics
plan
([plan-2026-05-25-structural-document-metrics.md](specs/active/plan-2026-05-25-structural-document-metrics.md))
found that almost everything once scoped as a “chopdiff v0.4.x addition” already shipped
in 0.3.1 (PRs #12 / #14 / #15): the cached per-block parse (`Paragraph.block_type` is a
`@cached_property`), `Paragraph.heading_level()` / `heading_title()`, typed
`Paragraph.links()` / `TextDoc.links()`, `TextDoc.sections()` with per-section rollups,
and `TextDoc.toc()` / `section_size_tree()`.

The items below are the **remaining gaps**. None block pprose (each has a pprose-side
workaround against the block source text), so these are *optional convenience*
follow-ups for chopdiff.
Filed against [jlevy/chopdiff](https://github.com/jlevy/chopdiff) on 2026-06-10 (issues
#18-#22); if accepted, pprose drops the corresponding workaround.
Each maps to a tbd bead (the `pp-…` id) for tracking on the pprose side.

## Requests

### 1. `Paragraph.code_language` / `Paragraph.code_line_count` (`pp-9cmv`)

- **Filed:** [jlevy/chopdiff#18](https://github.com/jlevy/chopdiff/issues/18)
- **Need:** per fenced-code block, the info-string language and the body line count, so
  pprose can report `fenced_code_counts_by_language` and `total_code_line_count`.
- **Proposed API:** `Paragraph.code_language -> str | None` (the fence info string,
  first token) and `Paragraph.code_line_count -> int` (body lines, excluding the
  fences), valid when `block_type` is `code`.
- **pprose workaround today:** parse the fence line and count body lines from the `code`
  block’s source text.

### 2. Typed `TableInfo` / `Paragraph.table_info` (`pp-eaa2`)

- **Filed:** [jlevy/chopdiff#19](https://github.com/jlevy/chopdiff/issues/19)
- **Need:** per table block, row / cell / column counts and per-column alignments.
- **Proposed API:** `Paragraph.table_info -> TableInfo | None` with `rows: int`,
  `cols: int`, `cells: int`, `alignments: list[Literal["left","center","right",None]]`,
  valid when `block_type` is `table`.
- **pprose workaround today:** count rows/cells from the `table` block’s source lines.

### 3. Typed `ListInfo` / `Paragraph.list_info` (`pp-tg93`)

- **Filed:** [jlevy/chopdiff#20](https://github.com/jlevy/chopdiff/issues/20)
- **Need:** ordered-vs-unordered, start index, nesting depth, and total item count in
  one object.
- **Proposed API:** `Paragraph.list_info -> ListInfo | None` with `ordered: bool`,
  `start: int | None`, `max_depth: int`, `item_count: int`.
- **pprose workaround today:** derive from `block_type` (`list` vs `ordered_list`) plus
  `collect(kinds={list_item})` / `base_blocks()` depths.
  (Lowest priority; the workaround is clean.)

### 4. `NodeKind.footnote_ref` (typed inline footnote reference) (`pp-aat4`)

- **Filed:** [jlevy/chopdiff#21](https://github.com/jlevy/chopdiff/issues/21)
- **Need:** a typed inline node kind for footnote references (`[^1]`), so footnote-ref
  counts come from the same typed inline walk as links/images/code-spans rather than a
  regex.
- **Proposed API:** add `footnote_ref` to `NodeKind`, surfaced via
  `collect(kinds={footnote_ref}, inline=True)`.
- **pprose workaround today:** keep pprose’s footnote-reference regex.

### 5. `TextDoc.frontmatter` (frontmatter isolation) (`pp-4hku`)

- **Filed:** [jlevy/chopdiff#22](https://github.com/jlevy/chopdiff/issues/22)
- **Need:** `from_text` should isolate a leading `---` YAML frontmatter block instead of
  treating it as a `paragraph`, so frontmatter is excluded from `paragraphs` and prose
  counts, and exposed as `TextDoc.frontmatter`.
- **Proposed API:** `TextDoc.frontmatter -> str | None` (raw frontmatter block), with
  the frontmatter excluded from `blocks()` / `paragraphs`.
- **pprose workaround today:** pprose detects-and-skips the leading `---` block itself.
- **Note:** chopdiff already depends on `frontmatter-format` for the DocGraph
  serializer; this would extend that to the `from_text` parse path.

## Status

All five were filed upstream as jlevy/chopdiff#18-#22 (2026-06-10), tracked under the
structural-metrics epic (`pp-3hg4`). The 2026-06-13 migration to **flexdoc 0.1.0**
satisfies **all five**: #1/#2/#3 as `Block.code_info` / `.table_info` / `.list_info`, #5
as `FlexDoc.frontmatter`, and #4 as `NodeKind.footnote_ref` (a typed inline node,
reachable via `doc.collect(kinds={NodeKind.footnote_ref}, recursive=True)`; verified
against 0.1.0). No upstream requests remain; the use case and a few narrower gaps
surfaced during the review (link-form discriminator, reference-definition surfacing) are
filed as [jlevy/flexdoc#5](https://github.com/jlevy/flexdoc/issues/5). The pprose-side
workaround-removal work still proceeds under `pp-3hg4` and is **not** blocked — pprose
now adapts the accessor names to flexdoc’s block model rather than waiting on an
upstream release.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
