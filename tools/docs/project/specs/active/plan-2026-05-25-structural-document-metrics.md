# Feature: Structural Document Decomposition for pprose Metrics

**Date:** 2026-05-25 (last updated 2026-05-26)

**Author:** Joshua Levy with agent assistance

**Status:** Draft — depends on chopdiff `v0.4.x` (a set of small additive PRs to
`TextDoc` that expose per-block parse results; see
[Chopdiff v0.4.x additions](#chopdiff-v04x-additions-needed)).

## Overview

Replace the regex + plain-text pipeline in
[tools/pprose/src/pprose/metrics.py](../../../../pprose/src/pprose/metrics.py) with a
single Markdown parse that produces a typed structural decomposition of the document,
then derive every quantitative metric from that decomposition rather than from
independent regex sweeps.

**The Markdown parse happens exactly once, in chopdiff.** Chopdiff `v0.3.0` already
parses each block with marko for `Paragraph.block_type`
([text_doc.py:116-133](../../../../../attic/chopdiff/src/chopdiff/docs/text_doc.py#L116-L133)).
The plan is to cache that parse result on `Paragraph` and expose it via additional
cached properties (`heading_level`, `code_language`, `list_info`, `table_info`,
`inlines`) plus a `TextDoc.section_tree()` for the heading hierarchy.
Pprose then becomes a thin serializer: walk the `TextDoc`, read those typed properties,
compute the `Metrics` snapshot, render the CLI output.
No marko import in pprose.
No re-parsing per block.

The work splits cleanly:

- **chopdiff `v0.4.x`** ships the typed accessors and the section-tree helper.
  Each addition is additive, cached on the same per-block marko parse `block_type`
  already does, and small enough to land as a focused PR.
- **pprose** bumps the chopdiff pin to `v0.4.x`, rewrites `Metrics` to the `*_count`
  schema, derives every field from chopdiff’s typed APIs plus pprose’s own lint regexes,
  updates `eval_report.py` / `eval_compare.py` for the field renames, and adjusts the
  tests.

The headline win for evaluation: `sentence_count` and `paragraph_count` become
well-defined prose-only counts that exclude heading text, table cells, and code.
Today those numbers silently include heading text and table content, which inflates
sentence counts for heading-dense or table-dense documents and destabilizes
`words_per_sentence` / `sentences_per_paragraph` density ratios in
[eval_report.py](../../../../pprose/src/pprose/eval_report.py).

There are no external consumers of pprose yet, so the existing `Metrics` field names
(`sentences`, `paragraphs`, `headings_total`, `*_hits`, …) are renamed outright with no
backward-compatibility shims.
Every count field uses the `*_count` convention.

## Goals

- Single Markdown parse end-to-end.
  The parse happens in chopdiff (already true at the block level for `block_type`); the
  parse result is cached and exposed via additional typed accessors.
  No re-parsing in pprose; no `marko` import in pprose.
- `sentence_count` and `paragraph_count` in `Metrics` are prose-only, computed via
  `doc.filtered(include={paragraph, list, blockquote, footnote}).size(TextUnit.{sentences,paragraphs})`.
  The `all_sentence_count` / `all_paragraph_count` variants come from `doc.size(...)`.
- Field naming convention: every count field uses `*_count` (`sentence_count`,
  `paragraph_count`, `heading_count`, `list_item_count`, `table_cell_count`, …). No
  legacy `sentences: int` or `headings_total: int` fields.
- `Metrics.from_text_doc(text_doc, file, ...)` returns a flattened numeric snapshot
  built by walking `TextDoc` once.
  Every count is computed inline; no separate decomposition module.
- Heading outline with per-section rollups, derived from `TextDoc.section_tree()` and
  the per-block sizes chopdiff already exposes.
  Renderable as an indented tree.
- Distribution metrics for prose: P50 / P95 / max words per sentence and per paragraph,
  computed inline from chopdiff’s per-block sentence and paragraph sizes.
- All current regex-based lint metrics (banned register, em-dash discipline, replacement
  history, pedantic markers, generic headings, bracket tags, bare URLs) keep their
  existing semantics but run against text extracted from the prose-only sub-document
  (`text_doc.filtered(include={paragraph, list, blockquote, footnote}).reassemble()`).
- YAML frontmatter handling: chopdiff `v0.4.x` either detects and isolates frontmatter
  natively (preferred) or pprose detects-and-skips the leading block (fallback).
- Pluggable sentence splitter via `TextDoc.from_text(text, sentence_splitter=...)`
  (already supported in chopdiff).
  Default stays `flowmark.split_sentences_regex`. No new CLI flag yet — added when there
  is a second supported splitter worth exposing.

## Non-Goals

- Re-implementing block typing, sentence offsets, sub-doc filtering, or the per-block
  marko parse anywhere in pprose.
  Those live in `chopdiff.TextDoc`.
- Maintaining a parallel typed Block / Inline hierarchy in pprose.
  The typed accessors live on chopdiff’s `Paragraph`.
- Waiting for chopdiff’s larger `BlockDoc` redesign
  ([PR #8](https://github.com/jlevy/chopdiff/pull/8)). The `v0.4.x` additions above give
  us what we need without the BlockDoc rewrite.
- Changing the qualitative rubric, guidelines, or any prompts.
  This is a measurement refactor.
- Rewriting `eval_report.py` density calculations beyond pointing them at the new
  prose-only counts. Density math stays the same.
- Adding any additional sentence splitter as a built-in dependency.
  Flowmark is sufficient; alternatives are noted as future work below.
- Building a custom sentence splitter or improving the flowmark regex itself.
- Changing CLI shape beyond the new output fields.

## Background

### Current pipeline

`metrics.py` today does two unrelated things:

1. **Regex sweeps** against the raw or lightly-stripped Markdown for headings, links,
   footnotes, bracket tags, tables, code blocks, bare URLs, and various lint patterns.
2. **Plain-text counting** via `chopdiff.docs.TextDoc`, after stripping YAML
   frontmatter, fenced code, and inline code via
   [strip_code_and_frontmatter](../../../../pprose/src/pprose/metrics.py#L265).

The plain-text pipeline has no Markdown awareness.
Headings, table cells, blockquote text, list-item text, and paragraph text all flow
through `TextDoc` as one undifferentiated stream.

### What chopdiff v0.3.0 already gives us

Verified by a direct smoke test against [attic/chopdiff](../../../../../attic/chopdiff)
at the v0.3.0 tag on a sample Markdown document covering frontmatter, headings,
paragraphs, a list, a table, a fenced code block, a blockquote, and a footnote
definition:

- `BlockType` enum (paragraph, heading, list, table, code, blockquote, html, footnote)
  and `Paragraph.block_type`, classified by parsing each blank-line block with marko.
- `TextDoc.iter_blocks(include=, exclude=)` and `TextDoc.filtered(include=, exclude=)` —
  block-typed iteration and aggregation.
  `doc.filtered(...).size(TextUnit.sentences)` answers “how many sentences across only
  these block kinds” in one call.
- Exact `Offsets(doc_offset, block_offset)` on every paragraph and sentence; the input
  is not stripped, so offsets round-trip exactly into the source text.
- Heuristic token estimation (`TextUnit.tokens`) with no `tiktoken` / network
  dependency.

Documented v0.3.0 limitations
([BlockType docstring](../../../../../attic/chopdiff/src/chopdiff/docs/text_doc.py#L76-L98)):

- A tight list is one `list` block; a loose list is one block per item with nesting
  flattened. No per-item granularity, but `list_info` (proposed below) will expose it
  from the same per-block marko parse.
- A continuation paragraph inside a list item is classified as `paragraph`.
- A fenced code block containing a blank line can split across blocks.
- Heading level, code language, table sub-structure, and typed inlines are not yet
  exposed; the marko parse result is computed but not retained.

### Chopdiff v0.4.x additions needed

Each item below is small and additive, cached on the same per-block marko parse
`Paragraph.block_type` already does.
The current `_classify_block` parses and discards the result; the refactor caches it so
other properties can read from it.

| Addition | What it returns | Pprose metrics unlocked |
| --- | --- | --- |
| `Paragraph._parsed_element` (private cache) | The marko element from the per-block parse. Refactored from `_classify_block`. | Foundation for every other accessor below. |
| `Paragraph.heading_level: int \| None` | `1..6` for ATX / setext headings, `None` otherwise. | `heading_counts_by_level`, `max_heading_depth`, `heading_level_skip_count`, `heading_outline`. |
| `Paragraph.heading_text: str \| None` | Heading content without the `#` prefix / underline. | `heading_outline.text`. |
| `Paragraph.code_language: str \| None` | The fence info string, e.g. `"python"`, `"bash"`. `None` for unfenced or no info. | `fenced_code_counts_by_language`. |
| `Paragraph.code_line_count: int \| None` | Number of lines in the code body. | `total_code_line_count`. |
| `Paragraph.list_info: ListInfo \| None` | `ListInfo(ordered, start, items, nesting_depth, total_item_count)`. | `list_item_count`, `max_list_nesting_depth`, `ordered_list_count`, `unordered_list_count`, `max_list_item_count`. |
| `Paragraph.table_info: TableInfo \| None` | `TableInfo(header_cells, body_rows, alignments, row_count, column_count)`. | `table_row_count`, `table_cell_count`, `max_table_row_count`, `max_table_column_count`. |
| `Paragraph.inlines: list[Inline]` | Typed walk of marko inline children: `Text`, `Link(url, text, kind: inline\|autolink\|reference_use)`, `Image(url, alt)`, `CodeSpan(text)`, `FootnoteRef(ref_id)`, `LineBreak`. (`Emphasis` / `Strong` flatten to their inner text for now.) | All link / image / footnote-ref / code-span metrics. Replaces every regex-based link / image / footnote sweep in pprose. |
| `TextDoc.section_tree() -> list[Section]` | Ordered list of `Section(heading: Paragraph \| None, level: int, children: list[Paragraph])` covering every block. Sections at the same level are siblings; deeper levels are nested under their parent. Blocks before the first heading go under a synthetic `Section(heading=None, level=0)`. | `heading_outline` (pprose just walks this and adds rollups). |
| `TextDoc.frontmatter: str \| None` (preferred; otherwise pprose detects) | The raw YAML frontmatter if the document begins with one, `None` otherwise. The frontmatter is excluded from `paragraphs`. | Frontmatter never inflates `paragraph_count` or appears in the prose stream. |

Each row is one focused chopdiff PR. The first row (caching the parse result) is the
prerequisite for the rest; the others can land in any order.

### Sentence-splitter landscape (informational)

We are shipping only `flowmark.split_sentences_regex`, with a Python-level plug point.
A short map of the alternatives that exist so the choice is informed, not so we add them
now:

| Splitter | Approach | Dependencies | Notes |
| --- | --- | --- | --- |
| **flowmark.split_sentences_regex** | Hand-tuned regex with conservative end-of-sentence heuristic (≥2-letter run, lowercase final letter, optional trailing quotes/parens; configurable minimum length). | None (pure stdlib `re`). | Current default. Calibrated for the Latin-language analytical-writing style this repo handles. Author maintains it. |
| **pysbd** | Rule-based segmenter. Python port of the Ruby [`pragmatic_segmenter`](https://github.com/diasks2/pragmatic_segmenter), which scored at or near the top of non-neural segmenter benchmarks. | Pure Python; no model download. | Strongest plausible upgrade if we ever want a non-regex rule-based engine. 22 languages. Last meaningful release was several years ago and the project is in low-maintenance mode — would need a current health check before adopting. |
| **spaCy** sentence splitter | Statistical / neural via a loaded language model (`en_core_web_sm` or larger). | Heavy — model download (~50 MB+), pulls in numpy and the spaCy runtime. | Strong on noisy text. Probably overkill for well-edited Markdown. Worth considering only if we also want spaCy for other linguistic features (POS tags, NER). |
| **NLTK Punkt** | Unsupervised sentence tokenizer, pre-trained per language. | NLTK runtime + `nltk.download('punkt')` data step. | The classic. Reasonable baseline, but the data download step is awkward for a `uvx`-style tool. |
| **syntok**, **sentence-splitter** (mediacloud), **blingfire**, **stanza** | Various rule-based or neural. | Varies. | Mentioned only for completeness; none are obvious wins over the above. |

For now: keep the flowmark default, expose the plug point in the Python API, and revisit
if a real document in the corpus shows the splitter making bad calls in a systematic
way.

### Downstream consumers that will change

- `eval_report.py` computes `words_per_sentence`, `words_per_paragraph`, and
  `sentences_per_paragraph` from the size block
  ([eval_report.py:635-642](../../../../pprose/src/pprose/eval_report.py#L635-L642)).
  These switch to the new prose-only numerators and denominators.
- `eval_compare.py` surfaces those derived ratios
  ([eval_compare.py:120-274](../../../../pprose/src/pprose/eval_compare.py#L120-L274)).
  Column lambdas need to read the renamed fields.
- Tests in `tools/pprose/tests/test_metrics.py`, `test_eval_report.py`,
  `test_eval_compare.py`, and `test_cli.py` reference current numbers and field names
  and need updating.

## Design

### Approach

Pprose work is gated on chopdiff `v0.4.x` shipping the additions above.
Once a tagged release exists with at least `Paragraph.heading_level`, `code_language`,
`list_info`, `table_info`, `inlines`, and `TextDoc.section_tree()`, pprose lands as one
focused PR:

1. Bump the `chopdiff` pin in `tools/pprose/pyproject.toml` to the v0.4.x release under
   the supply-chain cool-off rule.
   Refresh `uv.lock`. Verify no pprose call sites use `TextUnit.tiktokens` (renamed to
   `TextUnit.tokens` in v0.3.0).
2. Rewrite `Metrics` in `pprose/metrics.py` to the `*_count` schema (see API Changes
   below). Implement `Metrics.from_text_doc(text_doc, file, ...)` as a single walk over
   the `TextDoc`:
   - Iterate `text_doc.paragraphs`, classifying each by `block_type`.
   - Aggregate counts by kind directly from chopdiff’s typed accessors (`heading_level`,
     `code_language`, `list_info.items`, `table_info.row_count`, etc.).
   - Walk inlines on each prose block and on each heading, classifying links, counting
     images / footnote refs / code spans.
   - Use `text_doc.section_tree()` to build the `HeadingOutline` — a flat ordered list
     of `HeadingEntry` rows with per-section rollups, computed by aggregating sizes over
     each section’s children.
   - Compute sentence-length and paragraph-length distributions (P50 / P95 / max in
     words) by sorting per-sentence and per-paragraph word counts pulled from
     `paragraph.size(TextUnit.words)` and `sentence.size(TextUnit.words)`.
   - Run the existing lint regexes (banned register, em-dash discipline, replacement
     history, pedantic markers, generic headings, bracket tags, bare URLs) against the
     reassembled prose-only sub-document
     (`text_doc.filtered(include=PROSE_KINDS).reassemble()`).
3. Replace `measure()`'s body to build `TextDoc` once and call `Metrics.from_text_doc`.
   Delete the regex-based structural counters and the old `strip_code_and_frontmatter`
   helper.
4. Rewrite `format_human` to render the heading outline as an indented tree with section
   sizes, plus the new list / table / code / distribution sections.
   Update `format_summary_table` column names.
5. Update `eval_report.py` and `eval_compare.py` to read the renamed fields.
6. Update tests and golden fixtures.
   Where a fixture’s expected number changes, document why in the test.
7. Run `pprose metrics` across `docs/`, `runbooks/`, `shortcuts/`, and `skills/`;
   capture the before/after delta for `sentence_count`, `paragraph_count`, and
   `heading_count` in the PR description.

### Components

- [tools/pprose/src/pprose/metrics.py](../../../../pprose/src/pprose/metrics.py) —
  refactored to the `*_count` schema; `Metrics.from_text_doc`. No new pprose modules;
  the outline walk and distribution computation are private helpers inside `metrics.py`.
- [tools/pprose/src/pprose/eval_report.py](../../../../pprose/src/pprose/eval_report.py)
  — minor: field renames; density math unchanged.
- [tools/pprose/src/pprose/eval_compare.py](../../../../pprose/src/pprose/eval_compare.py)
  — minor: column lambdas read new field names.
- [tools/pprose/pyproject.toml](../../../../pprose/pyproject.toml) — bump `chopdiff` pin
  to v0.4.x.
- Tests in `tools/pprose/tests/`.

### Prose inclusion rules

To make the prose-vs-non-prose decision unambiguous, every chopdiff `BlockType` is
classified explicitly:

| chopdiff BlockType | Counted in `paragraph_count`? | Counted in `sentence_count` / `word_count`? | Counted elsewhere |
| --- | --- | --- | --- |
| `paragraph` (excluding frontmatter) | yes (1 per block) | yes | — |
| `list` | yes (1 per block — chopdiff coarseness) | yes | `list_block_count`; `list_item_count` reads `Paragraph.list_info.total_item_count` |
| `blockquote` | yes (1 per block) | yes | `blockquote_count` |
| `footnote` | yes (1 per block) | yes | `footnote_definition_count` |
| `heading` | **no** | **no** | `heading_count`, `heading_counts_by_level` (via `heading_level`), `heading_outline` |
| `table` | **no** | **no** | `table_count` + row / cell counts via `table_info` |
| `code` | **no** | **no** | `fenced_code_count`, `total_code_line_count`, `fenced_code_counts_by_language` (via `code_language` / `code_line_count`) |
| `html` | **no** | **no** | `html_block_count` |

“Prose-bearing” = paragraph + list + blockquote + footnote.
Pprose computes prose-only sums via
`text_doc.filtered(include={paragraph, list, blockquote, footnote}).size(...)`. The
`all_*` variants come from `text_doc.size(...)`.

Frontmatter handling: if chopdiff `v0.4.x` exposes `TextDoc.frontmatter`, pprose reads
it directly and the `paragraphs` list never contains the frontmatter block.
If not, pprose detects the leading block matching `^---\s*\n.*?\n---\s*$` (DOTALL) and
skips it during the walk.

### Heading outline and section rollups

`HeadingOutline` is a flat ordered list of `HeadingEntry` rows, each with the heading
itself (level, text, offset, words) plus rollups for everything under that heading until
the next equal-or-shallower heading.
Built by walking `text_doc.section_tree()` once and aggregating sizes per section.

A consumer can render an outline like:

```
# Title                                    (1450 words, 70 sents, 22 paras)
  ## Background                            (320 words, 16 sents, 5 paras, 1 code block)
  ## Design                                (810 words, 38 sents, 11 paras, 2 tables)
    ### Approach                           (380 words, 18 sents, 5 paras)
    ### API Changes                        (430 words, 20 sents, 6 paras, 2 tables)
  ## Implementation Plan                   (320 words, 16 sents, 6 paras, 1 list)
```

This subsumes “number of headings,” “max depth,” and “section size” into one navigable
artifact.

### API Changes

**No new CLI flags this round.** The `--sentence-splitter` flag is deferred until there
is a second supported splitter.
Existing `--format`, `--words-per-page`, and `--banned-words-file` flags are unchanged.

**`pprose.metrics` — `Metrics` is a flattened numeric snapshot.** All fields are counts
named with `*_count`. The `HeadingEntry` dataclass is a pprose serialization type (the
in-memory `Section` from chopdiff has more structure; `HeadingEntry` is the flat-list
form pprose serializes):

```python
@dataclass(frozen=True)
class HeadingEntry:
    level: int
    text: str
    doc_offset: int
    word_count: int                            # words in this heading itself
    section_word_count: int                    # rollup until next same-or-shallower
    section_sentence_count: int
    section_paragraph_count: int
    section_list_item_count: int
    section_table_count: int
    section_fenced_code_count: int

@dataclass
class Metrics:
    file: str

    # Sizes
    word_count: int
    sentence_count: int                        # prose-only
    paragraph_count: int                       # prose-only
    all_sentence_count: int                    # includes headings, table cells, etc.
    all_paragraph_count: int
    line_count: int
    page_count: float
    token_estimate: int                        # chopdiff TextUnit.tokens estimate

    # Heading structure
    heading_count: int
    heading_counts_by_level: dict[int, int]    # {1: n1, 2: n2, …}
    heading_outline: list[HeadingEntry]        # ordered, with section rollups
    max_heading_depth: int                     # deepest level used (1..6)
    heading_level_skip_count: int              # # of consecutive jumps > 1
    mean_heading_word_count: float

    # Lists
    list_block_count: int                      # chopdiff list blocks
    list_item_count: int                       # via Paragraph.list_info; includes nested
    ordered_list_count: int
    unordered_list_count: int
    max_list_nesting_depth: int                # 1 = top-level only
    max_list_item_count: int                   # size of the largest list

    # Blockquotes
    blockquote_count: int

    # Tables
    table_count: int
    table_row_count: int                       # body rows summed across all tables
    table_cell_count: int                      # body cells summed
    max_table_row_count: int                   # rows in the largest table
    max_table_column_count: int                # cols in the largest table

    # Code
    fenced_code_count: int
    indented_code_count: int
    total_code_line_count: int                 # fenced + indented
    inline_code_span_count: int
    fenced_code_counts_by_language: dict[str, int]    # "" for missing fence info

    # HTML
    html_block_count: int

    # Distributions (prose only)
    sentence_length_p50_words: int
    sentence_length_p95_words: int
    sentence_length_max_words: int
    paragraph_length_p50_words: int
    paragraph_length_p95_words: int
    paragraph_length_max_words: int

    # Links / footnotes (from Paragraph.inlines, not regex)
    external_link_count: int
    internal_link_count: int
    inline_link_count: int
    autolink_count: int
    reference_link_use_count: int
    reference_link_definition_count: int
    image_count: int
    footnote_reference_count: int
    footnote_definition_count: int

    # Bracket tags
    bracket_tag_count: int
    bracket_tag_examples: list[str]

    # Other text-level
    bare_url_count: int

    # Em-dash discipline
    spaced_em_dash_count: int
    em_dash_count: int
    em_dash_density_per_1000_words: float

    # Lint patterns (renamed *_hits → *_count)
    banned_register_count: int
    banned_register_examples: list[str]
    replacement_history_count: int
    replacement_history_examples: list[str]
    pedantic_marker_count: int
    pedantic_marker_examples: list[str]
    generic_heading_count: int
    generic_heading_examples: list[str]

    @classmethod
    def from_text_doc(
        cls,
        text_doc: TextDoc,
        file: str,
        *,
        words_per_page: int = WORDS_PER_PAGE,
        banned_re: re.Pattern[str] | None = None,
    ) -> "Metrics": ...
```

### Renames (no aliases, no backward-compat shims)

| Old field | New field |
| --- | --- |
| `words` | `word_count` |
| `sentences` | `sentence_count` (semantics now prose-only) |
| `paragraphs` | `paragraph_count` (semantics now prose-only) |
| `lines` | `line_count` |
| `pages` | `page_count` |
| `headings` (dict) | `heading_counts_by_level` |
| `headings_total` | `heading_count` |
| `links_external` | `external_link_count` |
| `links_internal` | `internal_link_count` |
| `links_total` | (removed — derivable: `external_link_count + internal_link_count`) |
| `links_inline` | `inline_link_count` |
| `links_autolink` | `autolink_count` |
| `links_reference_use` | `reference_link_use_count` |
| `links_reference_definitions` | `reference_link_definition_count` |
| `images` | `image_count` |
| `footnote_references` | `footnote_reference_count` |
| `footnote_definitions` | `footnote_definition_count` |
| `bracket_tags` | `bracket_tag_count` |
| `bare_urls` | `bare_url_count` |
| `tables` | `table_count` |
| `code_blocks` | `fenced_code_count` |
| `banned_register_hits` | `banned_register_count` |
| `spaced_em_dash_count` | (kept; already `*_count`) |
| `em_dashes_total` | `em_dash_count` |
| `replacement_history_hits` | `replacement_history_count` |
| `pedantic_marker_hits` | `pedantic_marker_count` |
| `generic_heading_hits` | `generic_heading_count` |

## Implementation Plan

### Phase 0: Chopdiff v0.4.x prerequisites (tracked in chopdiff repo)

Each is one focused chopdiff PR. The first (caching) is the prerequisite for the rest;
the others land in any order.

- [ ] **(chopdiff)** Cache the per-block marko parse result on `Paragraph` so other
  cached properties can read from it without re-parsing.
  Internal refactor of `_classify_block`; no public API change yet.
- [ ] **(chopdiff)** `Paragraph.heading_level: int | None` and
  `Paragraph.heading_text: str | None`.
- [ ] **(chopdiff)** `Paragraph.code_language: str | None` and
  `Paragraph.code_line_count: int | None`.
- [ ] **(chopdiff)** `Paragraph.list_info: ListInfo | None` (ordered / start / items /
  nesting_depth / total_item_count).
- [ ] **(chopdiff)** `Paragraph.table_info: TableInfo | None` (header_cells / body_rows
  / alignments / row_count / column_count).
- [ ] **(chopdiff)** `Paragraph.inlines: list[Inline]` typed walk (Text / Link with kind
  / Image / CodeSpan / FootnoteRef / LineBreak).
- [ ] **(chopdiff)** `TextDoc.section_tree() -> list[Section]` derived from heading
  blocks (setext-safe, `#`-in-code-safe via the cached parse).
- [ ] **(chopdiff, optional but preferred)** `TextDoc.frontmatter: str | None` with the
  frontmatter block excluded from `paragraphs`.
- [ ] **(chopdiff)** Cut a `v0.4.0` release with the additions above.

### Phase 1: pprose layer on chopdiff v0.4.x

Blocked on chopdiff `v0.4.0` being released.

- [ ] Bump `chopdiff` pin in `tools/pprose/pyproject.toml` to `v0.4.0` under the
  supply-chain cool-off rule; refresh `uv.lock`. Verify no pprose call sites use
  `TextUnit.tiktokens`.
- [ ] Rewrite `pprose/metrics.py`: replace the `Metrics` dataclass with the new
  `*_count` schema; implement `Metrics.from_text_doc` as a single walk over the
  `TextDoc`. Use `text_doc.section_tree()` to build the heading outline; use
  `Paragraph.list_info` / `table_info` / `code_language` / etc.
  for the typed per-block info; use `Paragraph.inlines` for link / image / footnote-ref
  / code span counts; compute distribution percentiles inline.
  Delete the regex-based structural counters and `strip_code_and_frontmatter`. Keep the
  lint regex constants and run them against the reassembled prose-only sub-document.
- [ ] Rewrite `format_human` in `metrics.py` to render: the heading outline as an
  indented tree with section sizes; new list / table / code / distribution sections; the
  existing lint sections (renamed).
  Update `format_summary_table` column names.
- [ ] Update `eval_report.py` to read `sentence_count` / `paragraph_count` /
  `word_count` from `Metrics`. Update `eval_compare.py` column lambdas similarly.
- [ ] Update `test_metrics.py`, `test_eval_report.py`, `test_eval_compare.py`, and
  `test_cli.py` for the new field names and prose-only semantics.
  Where a fixture’s expected number changes, document why in the test.
  Add coverage for the prose-only vs `all_*` distinction, the heading outline + section
  rollups, the link classification, list-info / table-info counts, and the distribution
  percentiles.
- [ ] Update `metrics.py` module docstring; rewrite the Known Limitations list to
  reflect the new pipeline (most prior limitations go away).
- [ ] Run `pprose metrics` across `docs/`, `runbooks/`, `shortcuts/`, and `skills/` on
  `main` and on this branch; capture the before/after delta for `sentence_count`,
  `paragraph_count`, and `heading_count` in the PR description.

## Testing Strategy

- **Refactored existing tests** in `test_metrics.py` to match new prose-only counts and
  renamed fields. Where a fixture’s expected number changes, the test comment explains
  why.
- **New tests** in `test_metrics.py` covering: heading outline + section rollups,
  prose-only vs `all_*` distinction, link classification (external / internal × inline /
  autolink / reference-use), list / table counts via chopdiff’s `list_info` /
  `table_info`, distribution percentiles on a fixture with known sentence-length spread,
  frontmatter exclusion.
- **Sanity sweep**: run `pprose metrics` on `docs/`, `runbooks/`, `shortcuts/`, and
  `skills/`, and report the before/after delta for sentences and paragraphs.
  Stash the comparison in the PR body.
- **No new live LLM tests.** All work is pure-Python parsing.

## Rollout Plan

- Chopdiff PRs (Phase 0) land first, in their own repo.
  Cut `v0.4.0`.
- Single pprose PR against `main`. No feature flag — the renamed schema and new
  semantics ship together with the chopdiff pin bump.
- Pprose version bump: minor (0.x.y → 0.{x+1}.0) because every machine-readable field
  name in `Metrics` changes.
  Note the rename table in the changelog and PR description.
- Downstream consumers in this repo (eval-report rendering, comparison tables, the CLI’s
  human-readable format) are updated in the same PR. There are no external consumers of
  pprose yet, so no deprecation cycle is needed.

## Open Questions

- Should `paragraph_count` count each list as one paragraph, or count each list-item
  paragraph as one? Current proposal: `paragraph_count` includes one per chopdiff `list`
  block (matching chopdiff’s coarse splitting).
  The `list_item_count` (from `Paragraph.list_info.total_item_count`) is a separate
  field. Confirm — alternative is to use `list_item_count` to expand `paragraph_count`,
  but that mixes granularities and destabilizes density ratios.
- Should headings contribute to `word_count` (the headline word count), or do we want a
  separate `prose_word_count` and `heading_word_count`? Proposal: keep `word_count` as
  the total-words-across-all-non-code-blocks number it is today; split only sentence /
  paragraph counts. Confirm.
- Naming for the “everything” variant of sentence / paragraph counts:
  `all_sentence_count` vs `total_sentence_count` vs `raw_sentence_count`. Current
  proposal: `all_*`.
- Distribution percentiles: should we report `mean_sentence_length_words` alongside P50
  / P95 / max, or rely only on the percentiles?
  Current proposal: percentiles only.
  Mean is sensitive to long-tailed outliers and P50 is more informative for editorial
  review. Confirm.
- `fenced_code_counts_by_language`: how do we key blocks with no language hint?
  Current proposal: `""` (empty string) for missing language; `"text"` is reserved for
  blocks explicitly labelled `` ```text ``. Confirm.
- Should `heading_outline` be included in the `Metrics` dataclass (and hence the YAML /
  JSON output by default), or only available via a dedicated `pprose outline` CLI
  command? Current proposal: include in `Metrics`. It’s structural, bounded by the
  heading count (typically tens of entries), and its presence makes downstream
  visualization trivial.
  Confirm.
- Inline `Emphasis` / `Strong`: flatten to inner text (current proposal) or expose as
  typed inlines? Counting emphasis usage is a plausible future metric; if we want it,
  chopdiff should expose them.
  Punt unless a user asks.

## References

- [tools/pprose/src/pprose/metrics.py](../../../../pprose/src/pprose/metrics.py)
- [tools/pprose/src/pprose/eval_report.py](../../../../pprose/src/pprose/eval_report.py)
- [chopdiff v0.3.0 changelog](https://github.com/jlevy/chopdiff/blob/main/CHANGELOG.md)
- [jlevy/chopdiff#7](https://github.com/jlevy/chopdiff/pull/7) — `BlockType` +
  `iter_blocks` / `filtered` (shipped in v0.3.0)
- [jlevy/chopdiff#9](https://github.com/jlevy/chopdiff/pull/9) — exact offsets + robust
  paragraph splitting (shipped in v0.3.0)
- [jlevy/chopdiff#8](https://github.com/jlevy/chopdiff/pull/8) — `BlockDoc` plan spec
  (longer-term redesign; not on the critical path for this work)
- [attic/chopdiff/src/chopdiff/docs/text_doc.py](../../../../../attic/chopdiff/src/chopdiff/docs/text_doc.py)
- [attic/flowmark/src/flowmark/linewrapping/sentence_split_regex.py](../../../../../attic/flowmark/src/flowmark/linewrapping/sentence_split_regex.py)
- [pysbd (Python Sentence Boundary Disambiguation)](https://github.com/nipunsadvilkar/pySBD)
  — possible future splitter
- [pragmatic_segmenter (Ruby)](https://github.com/diasks2/pragmatic_segmenter) —
  algorithm behind pysbd
