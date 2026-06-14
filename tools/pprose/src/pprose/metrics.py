"""
Quantitative metrics for analytical-writing artifacts.

Companion to:
  - docs/practical-prose-rubric.md (qualitative 0-5 scoring)
  - docs/practical-prose-guidelines.md (prescriptive rules)

Counts (all per-document):
  - Headings by depth (h1-h6) and total — ATX (# Heading) and setext (underline) styles
  - Links: external (http(s)/ftp/mailto — outbound citations) vs internal
    (relative paths, anchors — companion-file or in-repo references), plus a
    breakdown by markdown form (inline, autolink, reference-use, reference-definition,
    image)
  - Footnotes: references, definitions
  - Bracket tags: ALL-CAPS bracket tags (e.g. [VERIFIED], [DERIVED]) — heuristic,
    inspect the examples list to distinguish citations from markers like [TBD]/[OPTIONAL]
  - Bare URLs: plain https?:// URLs in prose not wrapped in markdown link syntax
  - Tables: count of markdown tables (from the parser's typed block tree)
  - Code blocks: count of code blocks, fenced or indented (from the typed block tree)
  - Banned-register hits: prose occurrences of strong-register / advocacy-register
    words from the canonical common-doc-guidelines §4.2 list referenced by
    practical-prose-guidelines.md E1 Clarity rule 4 (e.g. incontrovertibly, monumental,
    paradigm-shifting). Override the default list with --banned-words-file.
  - Em-dash discipline: count of spaced em dashes (" — " — a common agent failure
    mode prohibited by practical-prose-guidelines.md F2 rule 7) and total em-dash
    density per 1000 words.
  - Replacement-history hits: prose occurrences of phrases that narrate change
    ("previously named", "formerly", "under the new layout", "this design was changed",
    "now uses"). E3 Concision rule 5 — flags only, since some genres legitimately
    document history.
  - Pedantic-marker hits: prose occurrences of canonicality declarations and
    word-choice / reading-order justifications ("the canonical X", "we use the term Y
    because", "start with section"). E1 Clarity rule 6.
  - Generic-heading hits: headings whose entire title is a single generic word
    ("Overview", "Background", "Notes", "Details", "Misc"). F1 Organization rule 9 —
    flags only, since these can be appropriate at a section's outermost level.
  - Words, sentences, paragraphs, lines (prose-only via flexdoc's `prose_text()`: YAML
    frontmatter, code blocks, and inline code excluded, links/images unwrapped to their
    text, tables kept; sentence splitting via the flowmark heuristic through flexdoc)
  - Pages, computed at 275 words/page (configurable via --words-per-page)

Structural counts (headings, links by form, images, footnotes, tables, code blocks)
come from flexdoc's typed document model, not regex. Size counts (words / sentences /
paragraphs / lines) are computed over the same `FlexDoc.prose_text()` projection the
editorial-lint patterns (bracket tags, banned register, em-dash, replacement-history,
pedantic-marker) run over, so sizes and lint hits share one consistent prose scope.
`prose_text()` drops inline code, unwraps links/images to their text, and excludes
frontmatter and code blocks (tables kept); sentence boundaries use
flowmark.split_sentences_regex through flexdoc.

Known limitations:
  - HTML links (<a href="...">) are not counted — markdown-syntax links only.
  - Bracket-tag matching is a heuristic (ALL-CAPS inside []), not a parser.
  - Banned-register matching is a literal word-boundary check; mentions and use
    are not distinguished (a doc that quotes "monumental" as an example of a banned
    word still gets a hit). Inspect the examples list to triage.
  - Replacement-history, pedantic-marker, and generic-heading detectors are flags,
    not violations. Some genres (migration guides, postmortems, glossaries) legitimately
    use these patterns; the reviewer judges genre exception.

Usage:
  pprose metrics path/to/document.md
  pprose metrics path/to/document.md --format=yaml
  pprose metrics *.md            # multiple files, summary table
  pprose metrics doc.md --words-per-page 250
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml
from flexdoc import BlockType, FlexDoc, NodeKind, TextUnit
from flexdoc.docs import Link, LinkForm

WORDS_PER_PAGE = 275

# ALL-CAPS bracket-tag heuristic (e.g. [VERIFIED], [TBD]); a register marker, not a
# Markdown construct, so it stays a regex run over the prose-only text.
BRACKET_TAG_RE = re.compile(r"\[([A-Z][A-Z0-9_ -]{1,30})\]")

EM_DASH = "—"
SPACED_EM_DASH_RE = re.compile(r" — ")
EM_DASH_RE = re.compile(r"—")

REPLACEMENT_HISTORY_PHRASES = (
    "previously named",
    "previously called",
    "previously known as",
    "formerly named",
    "formerly known",
    "formerly called",
    "now uses",
    "now called",
    "now named",
    "we used to",
    "used to be",
    "used to use",
    "under the new layout",
    "in the new layout",
    "in the old layout",
    "this design was changed",
    "this design has changed",
    "was renamed",
    "has been renamed",
    "has since been renamed",
    "replaces the old",
    "replaced by",
    "replacing the old",
    "migrated from",
)
REPLACEMENT_HISTORY_RE = re.compile(
    r"(?<!\w)(?:" + "|".join(re.escape(p) for p in REPLACEMENT_HISTORY_PHRASES) + r")(?!\w)",
    re.IGNORECASE,
)

PEDANTIC_MARKER_PHRASES = (
    "the canonical",
    "is canonical",
    "is the canonical",
    "the one true",
    "note that we use",
    "we call this",
    "we use the term",
    "we use the word",
    "we chose the term",
    "we chose the name",
    "start with section",
    "read this first",
    "read this section first",
)
PEDANTIC_MARKER_RE = re.compile(
    r"(?<!\w)(?:" + "|".join(re.escape(p) for p in PEDANTIC_MARKER_PHRASES) + r")(?!\w)",
    re.IGNORECASE,
)

GENERIC_HEADING_WORDS = (
    "Overview",
    "Background",
    "Introduction",
    "Notes",
    "Details",
    "Misc",
    "Other",
    "Additional Information",
)
# Matched against real heading titles (from flexdoc's typed headings), not a regex over
# raw `#` lines, so only actual headings are checked.
GENERIC_HEADING_SET = frozenset(w.lower() for w in GENERIC_HEADING_WORDS)

EXTERNAL_SCHEMES = ("http://", "https://", "ftp://", "ftps://", "mailto:", "tel:")

# Default banned-register words. Canonical source:
#   docs/common-doc-guidelines.md §4.2
# Referenced from practical-prose-guidelines.md E1 Clarity rule 4 and applied by the
# `banned-register hits` metric below.
#
# The list combines:
#   - The common-doc-guidelines §4.2 strong-register / advocacy-register set
#     (incontrovertibly, emphatically, definitively, unequivocally, massive,
#     profound, monumental, transformational, paradigm-shifting, etc.).
#   - `dominant` as an advocacy-register extension that recurs in earnings /
#     investment-research drafts; retained as a default because it routinely slips
#     past general-purpose register filters.
#
# Project-specific overrides via --banned-words-file replace the entire list.
# Strong-register words may be earned with a citation; the linter flags occurrences
# and the reviewer decides which are earned.
DEFAULT_BANNED_WORDS = (
    "incontrovertibly",
    "emphatically",
    "definitively",
    "unequivocally",
    "massive",
    "monumental",
    "profound",
    "transformational",
    "seismic",
    "paradigm-shifting",
    "will revolutionize",
    "structurally outmaneuvered",
    "successfully executing",
    "crushing it",
    "dominant",
)


def _compile_banned_words(words: tuple[str, ...]) -> re.Pattern[str]:
    if not words:
        return re.compile(r"(?!.*)")  # never matches
    return re.compile(
        r"(?<!\w)(?:" + "|".join(re.escape(w) for w in words) + r")(?!\w)",
        re.IGNORECASE,
    )


DEFAULT_BANNED_RE = _compile_banned_words(DEFAULT_BANNED_WORDS)


def classify_url(url: str) -> str:
    """Classify a link target as 'external' (network: http(s)/ftp/mailto/tel) or 'internal'."""
    url = url.strip().lower()
    return "external" if url.startswith(EXTERNAL_SCHEMES) else "internal"


@dataclass
class Metrics:
    file: str
    headings: dict[str, int]
    headings_total: int
    links_external: int
    links_internal: int
    links_total: int
    links_inline: int
    links_autolink: int
    links_reference_use: int
    links_reference_definitions: int
    images: int
    footnote_references: int
    footnote_definitions: int
    bracket_tags: int
    bracket_tag_examples: list[str] = field(default_factory=list)
    bare_urls: int = 0
    tables: int = 0
    code_blocks: int = 0
    banned_register_hits: int = 0
    banned_register_examples: list[str] = field(default_factory=list)
    spaced_em_dash_count: int = 0
    em_dashes_total: int = 0
    em_dash_density_per_1000_words: float = 0.0
    replacement_history_hits: int = 0
    replacement_history_examples: list[str] = field(default_factory=list)
    pedantic_marker_hits: int = 0
    pedantic_marker_examples: list[str] = field(default_factory=list)
    generic_heading_hits: int = 0
    generic_heading_examples: list[str] = field(default_factory=list)
    words: int = 0
    sentences: int = 0
    paragraphs: int = 0
    lines: int = 0
    pages: float = 0.0


def measure(
    file_path: Path,
    words_per_page: int = WORDS_PER_PAGE,
    banned_re: re.Pattern[str] | None = None,
) -> Metrics:
    raw = file_path.read_text(encoding="utf-8")
    banned_re = banned_re if banned_re is not None else DEFAULT_BANNED_RE

    # One typed parse drives every structural metric. flexdoc isolates frontmatter as a
    # non-content region, so blocks / links / collected nodes already exclude it.
    doc = FlexDoc.from_text(raw)
    blocks = doc.blocks()

    # Headings by depth (and generic-heading flags) from the typed heading blocks: this
    # excludes `#` lines inside code blocks and resolves setext headings, so there are no
    # phantom-HR or in-code false positives.
    headings = {f"h{i}": 0 for i in range(1, 7)}
    generic_headings: list[str] = []
    for b in blocks:
        if b.type is not BlockType.heading:
            continue
        level = b.heading_level
        if level is not None and 1 <= level <= 6:
            headings[f"h{level}"] += 1
        title = (b.heading_info.title if b.heading_info else "").strip()
        if title.lower() in GENERIC_HEADING_SET:
            generic_headings.append(title)
    generic_heading_examples = sorted(set(generic_headings))[:10]

    # Links by typed form. Reference-use links resolve to their target URL, so the
    # external/internal split is a direct `classify_url` over each counted link.
    by_form: dict[LinkForm, list[Link]] = {}
    for link in doc.links():
        by_form.setdefault(link.link_form, []).append(link)
    inline_links = by_form.get(LinkForm.inline, [])
    autolinks = by_form.get(LinkForm.autolink, [])
    ref_uses = by_form.get(LinkForm.reference, [])
    bare_url_links = by_form.get(LinkForm.bare_url, [])
    ref_defs = doc.links(link_forms={LinkForm.reference_definition})
    images = doc.images()

    counted_links = inline_links + autolinks + ref_uses
    links_external = sum(1 for link in counted_links if classify_url(link.url) == "external")
    links_internal = sum(1 for link in counted_links if classify_url(link.url) == "internal")

    # Block-level structure, typed: catches indented and tilde-fenced code the old regex
    # missed, and counts only real table / footnote-definition blocks.
    tables = sum(1 for b in blocks if b.type is BlockType.table)
    code_blocks = sum(1 for b in blocks if b.type is BlockType.code)
    footnote_definitions = sum(1 for b in blocks if b.type is BlockType.footnote)
    footnote_references = len(doc.collect(kinds={NodeKind.footnote_ref}))

    # Editorial lint runs over the prose-only projection: inline code dropped, links and
    # images unwrapped to their text, frontmatter and code blocks excluded, tables kept.
    prose = doc.prose_text(include_tables=True)
    bracket_tag_matches = BRACKET_TAG_RE.findall(prose)
    tag_examples = sorted(set(bracket_tag_matches))[:10]
    banned_matches = banned_re.findall(prose)
    banned_examples = sorted({m.lower() for m in banned_matches})[:10]
    spaced_em_dashes = SPACED_EM_DASH_RE.findall(prose)
    em_dashes_total = len(EM_DASH_RE.findall(prose))
    replacement_history_matches = REPLACEMENT_HISTORY_RE.findall(prose)
    replacement_history_examples = sorted({m.lower() for m in replacement_history_matches})[:10]
    pedantic_marker_matches = PEDANTIC_MARKER_RE.findall(prose)
    pedantic_marker_examples = sorted({m.lower() for m in pedantic_marker_matches})[:10]

    # Size counts are computed over the same prose-only projection as the lint patterns,
    # so word / sentence / paragraph / line counts and the lint hits share one consistent
    # scope (frontmatter, code blocks, and inline code excluded; links/images unwrapped;
    # tables kept). flexdoc sizes a parsed document, so reparse the prose text.
    size_doc = FlexDoc.from_text(prose)
    words = size_doc.size(TextUnit.words)
    sentences = size_doc.size(TextUnit.sentences)
    paragraphs = size_doc.size(TextUnit.paragraphs)
    lines = size_doc.size(TextUnit.lines)
    pages = round(words / words_per_page, 1)
    em_dash_density = round(em_dashes_total * 1000.0 / words, 2) if words else 0.0

    return Metrics(
        file=str(file_path),
        headings=headings,
        headings_total=sum(headings.values()),
        links_external=links_external,
        links_internal=links_internal,
        links_total=len(counted_links),
        links_inline=len(inline_links),
        links_autolink=len(autolinks),
        links_reference_use=len(ref_uses),
        links_reference_definitions=len(ref_defs),
        images=len(images),
        footnote_references=footnote_references,
        footnote_definitions=footnote_definitions,
        bracket_tags=len(bracket_tag_matches),
        bracket_tag_examples=tag_examples,
        bare_urls=len(bare_url_links),
        tables=tables,
        code_blocks=code_blocks,
        banned_register_hits=len(banned_matches),
        banned_register_examples=banned_examples,
        spaced_em_dash_count=len(spaced_em_dashes),
        em_dashes_total=em_dashes_total,
        em_dash_density_per_1000_words=em_dash_density,
        replacement_history_hits=len(replacement_history_matches),
        replacement_history_examples=replacement_history_examples,
        pedantic_marker_hits=len(pedantic_marker_matches),
        pedantic_marker_examples=pedantic_marker_examples,
        generic_heading_hits=len(generic_headings),
        generic_heading_examples=generic_heading_examples,
        words=words,
        sentences=sentences,
        paragraphs=paragraphs,
        lines=lines,
        pages=pages,
    )


def format_human(m: Metrics) -> str:
    h = m.headings
    examples = ", ".join(f"[{x}]" for x in m.bracket_tag_examples) or "—"
    banned_examples = ", ".join(m.banned_register_examples) or "—"
    rh_examples = ", ".join(m.replacement_history_examples) or "—"
    pm_examples = ", ".join(m.pedantic_marker_examples) or "—"
    gh_examples = ", ".join(m.generic_heading_examples) or "—"
    return f"""\
{m.file}

Size:
  Words           {m.words:>8,}      Sentences       {m.sentences:>8,}
  Paragraphs      {m.paragraphs:>8,}      Lines           {m.lines:>8,}
  Pages (275 wpm) {m.pages:>8.1f}

Headings:
  h1  {h["h1"]:>4}    h2  {h["h2"]:>4}    h3  {h["h3"]:>4}
  h4  {h["h4"]:>4}    h5  {h["h5"]:>4}    h6  {h["h6"]:>4}
  total {m.headings_total:>4}

Links:
  external        {m.links_external:>4}    (http(s)/ftp/mailto — outbound citations)
  internal        {m.links_internal:>4}    (relative paths, anchors — companion-file refs)
  total (non-img) {m.links_total:>4}    (= external + internal = inline + autolink + reference-use)
  inline          {m.links_inline:>4}
  autolink        {m.links_autolink:>4}
  reference-use   {m.links_reference_use:>4}
  ref-definitions {m.links_reference_definitions:>4}    (count of [id]: url lines; not summed into total)
  images          {m.images:>4}

Footnotes:
  references      {m.footnote_references:>4}
  definitions     {m.footnote_definitions:>4}

Bracket tags (ALL-CAPS bracket tags, e.g. [VERIFIED] — inspect examples to distinguish citations from markers):
  count           {m.bracket_tags:>4}
  examples        {examples}

Other:
  bare URLs       {m.bare_urls:>4}
  tables          {m.tables:>4}
  code blocks     {m.code_blocks:>4}

Lint (E1 Clarity rule 4 — banned register from common-doc-guidelines §4.2; may be earned with a citation):
  banned hits     {m.banned_register_hits:>4}
  examples        {banned_examples}

Lint (F2 Consistency rule 7 — em-dash discipline):
  spaced em " — " {m.spaced_em_dash_count:>4}    (common agent failure mode; prefer "—" or other punctuation)
  em dashes total {m.em_dashes_total:>4}
  density /1k wds {m.em_dash_density_per_1000_words:>4.2f}

Lint (E3 Concision rule 5 — replacement history; flag only, genre-dependent):
  rh hits         {m.replacement_history_hits:>4}
  examples        {rh_examples}

Lint (E1 Clarity rule 6 — pedantic/pedagogical markers; flag only):
  pedantic hits   {m.pedantic_marker_hits:>4}
  examples        {pm_examples}

Lint (F1 Organization rule 9 — generic templated headings; flag only):
  generic-hd hits {m.generic_heading_hits:>4}
  examples        {gh_examples}
"""


def format_summary_table(metrics_list: list[Metrics]) -> str:
    if not metrics_list:
        return ""
    rows = []
    rows.append(
        f"{'file':<60} {'words':>7} {'sents':>6} {'paras':>6} {'pages':>6} "
        f"{'h1':>3} {'h2':>3} {'h3':>3} {'h4':>3} "
        f"{'ext':>4} {'int':>4} {'fns':>4} {'btags':>6}"
    )
    rows.append("-" * len(rows[0]))
    for m in metrics_list:
        name = m.file if len(m.file) <= 60 else "..." + m.file[-57:]
        rows.append(
            f"{name:<60} {m.words:>7,} {m.sentences:>6,} {m.paragraphs:>6,} "
            f"{m.pages:>6.1f} {m.headings['h1']:>3} {m.headings['h2']:>3} "
            f"{m.headings['h3']:>3} {m.headings['h4']:>3} "
            f"{m.links_external:>4} {m.links_internal:>4} "
            f"{m.footnote_references:>4} {m.bracket_tags:>6}"
        )
    return "\n".join(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Quantitative metrics for analytical-writing artifacts.",
    )
    parser.add_argument("paths", nargs="+", type=Path, help="Markdown file(s) to measure.")
    parser.add_argument(
        "--format",
        choices=["text", "yaml", "json"],
        default="text",
        help=(
            "Output shape. `text` is the human-readable default. `yaml` is the "
            "preferred machine-readable shape and matches the rest of the eval "
            "tooling's hybrid YAML+Markdown convention. `json` is supported for "
            "interop with non-YAML consumers."
        ),
    )
    parser.add_argument(
        "--words-per-page",
        type=int,
        default=WORDS_PER_PAGE,
        help=f"Words per page for page-count calculation (default: {WORDS_PER_PAGE}).",
    )
    parser.add_argument(
        "--banned-words-file",
        type=Path,
        default=None,
        help="File with banned-register words (one per line, '#' starts a comment). "
        "Replaces the default Clarity Rule 4 list.",
    )
    args = parser.parse_args(argv)

    if args.banned_words_file is not None:
        words = tuple(
            line.split("#", 1)[0].strip()
            for line in args.banned_words_file.read_text(encoding="utf-8").splitlines()
            if line.split("#", 1)[0].strip()
        )
        banned_re = _compile_banned_words(words)
    else:
        banned_re = DEFAULT_BANNED_RE

    metrics_list: list[Metrics] = []
    for p in args.paths:
        if not p.is_file():
            print(f"warning: not a file: {p}", file=sys.stderr)
            continue
        metrics_list.append(measure(p, words_per_page=args.words_per_page, banned_re=banned_re))

    if not metrics_list:
        return 1

    if args.format == "yaml":
        print(
            yaml.safe_dump(
                [asdict(m) for m in metrics_list],
                sort_keys=False,
                allow_unicode=True,
            ),
            end="",
        )
    elif args.format == "json":
        print(json.dumps([asdict(m) for m in metrics_list], indent=2))
    elif len(metrics_list) == 1:
        print(format_human(metrics_list[0]))
    else:
        print(format_summary_table(metrics_list))

    return 0


if __name__ == "__main__":
    sys.exit(main())
