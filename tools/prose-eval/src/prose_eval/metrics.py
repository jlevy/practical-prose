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
  - Tables: count of markdown tables (detected via separator rows)
  - Code blocks: count of fenced code blocks in the raw document
  - Banned-register hits: prose occurrences of strong-register / advocacy-register
    words from the canonical common-doc-guidelines §4.2 list referenced by
    practical-prose-guidelines.md E1 Clarity rule 4 (e.g. incontrovertibly, monumental,
    paradigm-shifting). Override the default list with --banned-words-file.
  - Em-dash discipline: count of spaced em dashes (" — " — a common agent failure
    mode prohibited by practical-prose-guidelines.md E5 rule 7) and total em-dash
    density per 1000 words.
  - Replacement-history hits: prose occurrences of phrases that narrate change
    ("previously named", "formerly", "under the new layout", "this design was changed",
    "now uses"). E3 Concision rule 5 — flags only, since some genres legitimately
    document history.
  - Pedantic-marker hits: prose occurrences of canonicality declarations and
    word-choice / reading-order justifications ("the canonical X", "we use the term Y
    because", "start with section"). E1 Clarity rule 6.
  - Generic-heading hits: ATX headings whose entire text is a single generic word
    ("Overview", "Background", "Notes", "Details", "Misc"). E4 Organization rule 9 —
    flags only, since these can be appropriate at a section's outermost level.
  - Words, sentences, paragraphs, lines (prose-only — YAML frontmatter, fenced code
    blocks, and inline code are stripped before counting; sentence splitting via flowmark
    heuristic through chopdiff)
  - Pages, computed at 275 words/page (configurable via --words-per-page)

Word/sentence/paragraph counts use chopdiff's TextDoc, which uses
flowmark.split_sentences_regex for sentence boundaries.

Known limitations:
  - HTML links (<a href="...">) are not counted — markdown-syntax links only.
  - Reference-link definitions require a URL-shaped target (https://, /, ./, ../);
    fragment-only targets like `[id]: #anchor` are not counted.
  - Bracket-tag matching is a heuristic (ALL-CAPS inside []), not a parser.
  - Setext heading detection (`Title\n===` for h1, `Title\n---` for h2) treats any
    `===` or `---` line under non-empty text as a heading. A horizontal rule of
    matching characters under regular prose will count as a phantom h1/h2; the repo
    style uses `* * *` for HRs to avoid this.
  - Banned-register matching is a literal word-boundary check; mentions and use
    are not distinguished (a doc that quotes "monumental" as an example of a banned
    word still gets a hit). Inspect the examples list to triage.
  - Replacement-history, pedantic-marker, and generic-heading detectors are flags,
    not violations. Some genres (migration guides, postmortems, glossaries) legitimately
    use these patterns; the reviewer judges genre exception.

Usage:
  prose-metrics path/to/document.md
  prose-metrics path/to/document.md --format=yaml
  prose-metrics *.md            # multiple files, summary table
  prose-metrics doc.md --words-per-page 250
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml
from chopdiff.docs import TextDoc, TextUnit

WORDS_PER_PAGE = 275

HEADING_RE = re.compile(r"^(#{1,6})\s+\S", re.MULTILINE)
SETEXT_H1_RE = re.compile(r"^[^\n]+\n={3,}\s*$", re.MULTILINE)
SETEXT_H2_RE = re.compile(r"^[^\n]+\n-{3,}\s*$", re.MULTILINE)
INLINE_LINK_RE = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\n]+)\)")
IMAGE_RE = re.compile(r"!\[([^\]\n]*)\]\(([^)\n]+)\)")
AUTOLINK_RE = re.compile(r"<(https?://[^>\s]+)>")
REF_LINK_DEF_RE = re.compile(
    r"^\[([^\]^\n][^\]\n]*)\]:\s*((?:https?://|/|\.\.?/)\S+)", re.MULTILINE
)
REF_LINK_USE_RE = re.compile(r"(?<!!)\[([^\]\n]+)\]\[([^\]\n]+)\]")
FOOTNOTE_REF_RE = re.compile(r"\[\^([^\]\n]+)\]")
FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]\n]+)\]:", re.MULTILINE)
BRACKET_TAG_RE = re.compile(r"\[([A-Z][A-Z0-9_ -]{1,30})\]")

BARE_URL_RE = re.compile(r"(?<![(<\[])https?://[^\s)>\]]+")
TABLE_SEP_RE = re.compile(r"^\|[\s:|-]+\|\s*$", re.MULTILINE)
CODE_FENCE_RE = re.compile(r"^```[\s\S]*?^```", re.MULTILINE)
CODE_INLINE_RE = re.compile(r"`[^`\n]+`")
FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)

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
GENERIC_HEADING_RE = re.compile(
    r"^#{1,6}\s+(?:" + "|".join(re.escape(w) for w in GENERIC_HEADING_WORDS) + r")\s*$",
    re.MULTILINE | re.IGNORECASE,
)

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
    """Classify a link target as 'external' or 'internal'.

    External: targets a network resource (http(s), ftp, mailto, tel).
    Internal: relative paths, absolute paths, anchors, or anything else not
    requiring network access — i.e., references that resolve within the
    repository or document.
    """
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


def strip_code_and_frontmatter(text: str) -> str:
    text = FRONTMATTER_RE.sub("", text)
    text = CODE_FENCE_RE.sub("", text)
    text = CODE_INLINE_RE.sub("", text)
    return text


def count_headings(text: str) -> dict[str, int]:
    counts = {f"h{i}": 0 for i in range(1, 7)}
    for m in HEADING_RE.finditer(text):
        counts[f"h{len(m.group(1))}"] += 1
    counts["h1"] += len(SETEXT_H1_RE.findall(text))
    counts["h2"] += len(SETEXT_H2_RE.findall(text))
    return counts


def measure(
    file_path: Path,
    words_per_page: int = WORDS_PER_PAGE,
    banned_re: re.Pattern[str] | None = None,
) -> Metrics:
    raw = file_path.read_text(encoding="utf-8")
    structural = strip_code_and_frontmatter(raw)
    banned_re = banned_re if banned_re is not None else DEFAULT_BANNED_RE

    headings = count_headings(structural)

    inline_links = INLINE_LINK_RE.findall(structural)
    images = IMAGE_RE.findall(structural)
    autolinks = AUTOLINK_RE.findall(structural)
    ref_defs = REF_LINK_DEF_RE.findall(structural)
    ref_uses = REF_LINK_USE_RE.findall(structural)
    footnote_refs = FOOTNOTE_REF_RE.findall(structural)
    footnote_defs = FOOTNOTE_DEF_RE.findall(structural)

    ref_def_url_by_id = {ref_id.strip().lower(): url for ref_id, url in ref_defs}
    inline_classes = [classify_url(url) for _, url in inline_links]
    autolink_classes = ["external"] * len(autolinks)
    ref_use_classes = [
        classify_url(ref_def_url_by_id.get(ref_id.strip().lower(), "")) for _, ref_id in ref_uses
    ]
    all_link_classes = inline_classes + autolink_classes + ref_use_classes
    links_external = sum(1 for c in all_link_classes if c == "external")
    links_internal = sum(1 for c in all_link_classes if c == "internal")

    bracket_tag_matches = BRACKET_TAG_RE.findall(structural)
    tag_examples = sorted(set(bracket_tag_matches))[:10]

    bare_urls = BARE_URL_RE.findall(structural)
    tables = len(TABLE_SEP_RE.findall(raw))
    code_blocks = len(CODE_FENCE_RE.findall(raw))

    banned_matches = banned_re.findall(structural)
    banned_examples = sorted({m.lower() for m in banned_matches})[:10]

    spaced_em_dashes = SPACED_EM_DASH_RE.findall(structural)
    em_dashes_total = len(EM_DASH_RE.findall(structural))

    replacement_history_matches = REPLACEMENT_HISTORY_RE.findall(structural)
    replacement_history_examples = sorted({m.lower() for m in replacement_history_matches})[:10]

    pedantic_marker_matches = PEDANTIC_MARKER_RE.findall(structural)
    pedantic_marker_examples = sorted({m.lower() for m in pedantic_marker_matches})[:10]

    generic_heading_matches = GENERIC_HEADING_RE.findall(structural)
    generic_heading_examples = sorted({m.strip() for m in generic_heading_matches})[:10]

    doc = TextDoc.from_text(structural)
    words = doc.size(TextUnit.words)
    sentences = doc.size(TextUnit.sentences)
    paragraphs = doc.size(TextUnit.paragraphs)
    lines = doc.size(TextUnit.lines)
    pages = round(words / words_per_page, 1)
    em_dash_density = round(em_dashes_total * 1000.0 / words, 2) if words else 0.0

    return Metrics(
        file=str(file_path),
        headings=headings,
        headings_total=sum(headings.values()),
        links_external=links_external,
        links_internal=links_internal,
        links_total=len(inline_links) + len(autolinks) + len(ref_uses),
        links_inline=len(inline_links),
        links_autolink=len(autolinks),
        links_reference_use=len(ref_uses),
        links_reference_definitions=len(ref_defs),
        images=len(images),
        footnote_references=len(footnote_refs),
        footnote_definitions=len(footnote_defs),
        bracket_tags=len(bracket_tag_matches),
        bracket_tag_examples=tag_examples,
        bare_urls=len(bare_urls),
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
        generic_heading_hits=len(generic_heading_matches),
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

Lint (E5 Consistency rule 7 — em-dash discipline):
  spaced em " — " {m.spaced_em_dash_count:>4}    (common agent failure mode; prefer "—" or other punctuation)
  em dashes total {m.em_dashes_total:>4}
  density /1k wds {m.em_dash_density_per_1000_words:>4.2f}

Lint (E3 Concision rule 5 — replacement history; flag only, genre-dependent):
  rh hits         {m.replacement_history_hits:>4}
  examples        {rh_examples}

Lint (E1 Clarity rule 6 — pedantic/pedagogical markers; flag only):
  pedantic hits   {m.pedantic_marker_hits:>4}
  examples        {pm_examples}

Lint (E4 Organization rule 9 — generic templated headings; flag only):
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
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
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
