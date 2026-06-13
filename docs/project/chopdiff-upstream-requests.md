---
title: chopdiff upstream feature requests (from pprose metrics work)
description: The chopdiff API gaps pprose still works around after the 0.3.1 upgrade, filed as issues jlevy/chopdiff#18-#22 for its next release.
date: 2026-06-02
last_updated: 2026-06-10
status: active
---
# chopdiff Upstream Feature Requests

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

All five are now filed upstream as jlevy/chopdiff#18-#22 (2026-06-10). These are tracked
under the structural-metrics epic (`pp-3hg4`) with the `upstream-chopdiff` label.
The pprose-side work (`pp-pd8t` and friends) proceeds on the 0.3.1 workarounds and is
**not** blocked on any of the above.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
