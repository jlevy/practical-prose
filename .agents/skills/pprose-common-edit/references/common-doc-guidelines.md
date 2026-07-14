---
title: Common Documentation Guidelines
description: Brief, general guidelines for humans and agents writing and organizing code, text files, and documentation; the base substrate the practical-prose layers extend.
date: 2026-05-13
status: active
---
# Common Documentation Guidelines

Version: v0.3 (last update 2026-06-12)\
Joshua Levy (github.com/jlevy)

## Purpose

Both agents and humans benefit from accurate, maintained documentation.
These are brief and general guidelines for humans and agents when writing and organizing
code, text files, and documentation.

See the [Practical Prose](https://github.com/jlevy/practical-prose) repository for more
extensive guidelines and context.

## 1. Organizing Documentation

1. **Organize documents for rapid orientation**

   - All context for understanding a project should be efficiently discoverable.
   - Documents should reference other documents whenever relevant.
   - A reader should be able to navigate from an obvious root document to all other
     documents relevant to a given need by following references.

2. **Use self-evident filenames and concise references**

   - For file naming, always follow existing project conventions.
     If conventions are unclear, use the conventions here.
   - Repos and key file folders should have a concise `README.md` as a root document
     that points to other documents.
   - Within the top-level repo or within key folders, a `docs/` folder should be added
     with other key docs and referenced in the `README.md`.
   - Whenever possible give documents brief but unique names.
   - Include a hint of the *topic* as well as *purpose*, such as
     `python-structural-quality-guidelines.md`.
   - Documents that are likely to become less relevant over time should have *dates or
     versions* as well, such as `plan-2026-04-28-browser-realtime-streaming.md`.
   - Unless other rules forbid it, references within documents should be *maximally
     concise* so they are easy to maintain:
     - For URLs, use simple link text with the URL in Markdown format.
     - For other documents, use the simplest unique reference, such as a title or
       filename, that makes the document easy to find.
     - Do not include unnecessary metadata, local paths, or other details readily
       determined from a search.

3. **Divide documents by ownership, audience, and cadence**

   - Documents owned and maintained by different people or teams should usually be
     distinct.
   - Documents meant for different audiences (such as internal versus external, or team
     docs versus sensitive docs) should be kept separate.
   - Documents updated on different cadences (such as ad hoc, every sprint, or yearly)
     should be distinct.
   - Documents with the same ownership, audience, and update cadence should be
     consolidated.

4. **Organize documents for maintainability**

   - Reference or include relevant guidelines for updates.
   - Documents should be organized in a way that is compatible with typical update
     processes.

## 2. Structuring Documents

1. **Explain motivations and background**

   - Assume readers have low context.
   - Highest-level documents or introductory sections should explain *why* as well as
     *what*.
   - A key part of the *why* is explaining why some approaches are taken and their
     benefits compared to alternate approaches or alternate tools.
   - Cite external sources for all content that is best covered externally.

2. **Give context gradually and efficiently**

   - Documents should be as brief as possible while still preserving all relevant
     detail.
   - Add detail incrementally: start with summaries, link to deeper docs.

3. **Keep details close to where they apply**

   - For example, docstrings in code or descriptions within YAML are preferred to
     separate documentation when the content directly relates to code or content in
     those files.

4. **Avoid duplication**

   - Do *not* repeat content in higher-level docs if the details are in referenced
     lower-level docs.
   - For example, if `docs/design.md` is an overview of the design, do not repeat the
     design in `README.md`; reference it instead.

5. **Describe the present state, not what it replaced**

   - By default, write as if the current work or referenced system or design always
     existed. Most readers need to understand what *is*, not what *was*; replacement
     history pollutes their context with deprecated concepts they would otherwise never
     have to learn. When version control like Git is used, its history is the
     authoritative record of what was removed.
   - Agents are especially prone to retaining history notations that are no longer
     relevant ( “this design was changed because of X,” “this function was previously
     named X”, “removed Z”). When in doubt, cut it.
   - Exceptions are allowed when the document’s purpose *includes* history: migration
     guides, postmortems, deprecation notices, decision records, changelogs,
     governance/versioning sections in standards and schemas, and one-line pointers when
     a future reader needs to find a predecessor (for example, “see commit `abc123` for
     the prior shape”). The test is whether the history serves the reader’s task or
     simply records the author’s path.

## 3. Writing Style

Stylistically, emphasize **clarity**, **depth**, **rigor**, and **warmth**.

1. **Be clear and concise**

   - Use direct and simple language.
   - Eliminate unnecessary or extraneous words.
   - Avoid obvious statements.
   - Remove duplication where a document says the same thing in different places.
   - If removing a sentence loses no information about the subject, cut it.

2. **Be detailed and specific**

   - Use data or facts instead of generalizations or adjectives.
   - Avoid vagueness or generalities.
   - Use concrete examples.
   - Cite sources whenever possible.

3. **Be rigorous and logical**

   - Use structure, such as headings, subheadings, and lists, effectively.
   - Keep structure logical and consistent.
   - Make headings specific; cleave to the true contours of the subject matter.

4. **Be engaging and warm**

   - Be friendly in tone, avoiding unnecessary formality unless required by the
     situation (such as in legal documents).
   - Be gracious in acknowledging previous work, even if correcting it.
   - Avoid unnecessary coldness, blame, condescension, or opacity when writing for
     humans. For agent-facing documents, the equivalent is directness, explicit context,
     and absence of performative fluff.

## 4. Effective Communication

1. **Respect the reader’s intelligence**

   - Write for a reader that is *100% intelligent and 100% ignorant*. This respects the
     reader yet provides enough context.
   - Either explain concepts fully and from first principles or point them to where they
     can learn the concept.
   - Never dumb things down, be vague, or skip important technicalities or details.

2. **Calibrate confidence**

   - Never make a confident statement without citations or reasoning that justify the
     confidence.
   - Judgments are allowed but must be calibrated, considering evidence for and against.
   - Do *not* aim to be agreeable; aim to be accurate when certain and explicit about
     uncertainties.
   - Do *not* make sweeping claims or use extravagant language.
     Avoid words like “incontrovertibly,” “emphatically,” “definitively,”
     “unequivocally,” “massive,” “monumental,” “profound,” “transformational,”
     “seismic,” “paradigm-shifting,” “will revolutionize,” “structurally outmaneuvered,”
     “successfully executing,” or “crushing it.”
     `pprose guidelines ai-prose-corrections` extends this list with hollow, mechanical,
     and marketing-register fingerprints of unedited LLM output (the *delve / leverage /
     Furthermore / supercharge* registers); both lists apply.

3. **Cut pompousness, meta-commentary, and unnecessary formality**

   - Avoid “talking about talking,” such as narrating what a doc covers or instructing
     readers on how to read a document.
     Exception: standards, rubrics, runbooks, and other process documents may include
     structural commentary (how dimensions map to rules, how to score, when to apply a
     pass) when that commentary is what the document is *for*.
   - Eliminate common but unnecessary phrases, such as “due to the fact” or “at this
     point in time.” Avoid adverbs and general adjectives, such as “quickly respond” or
     “very good.”
   - Avoid pedantry, such as calling documents “canonical,” or giving justifications for
     word choices. Jargon like “load-bearing” is acceptable when the audience uses it and
     the term is genuinely descriptive (for example, a sentence-craft discussion citing
     Gopen and Swan’s notion of *load-bearing constraints on sentence structure*); avoid
     it as a filler intensifier in ordinary prose.
   - Cut acronyms and jargon unless they serve a clear purpose.
   - When technical terms or jargon are used, define them or reference their definition.

## 5. Formatting

> Block quotes like this should be used for meta-instructions, quotes, and epigraphs.

- **Boldface:** Use boldface for defining **key words** or concepts.
- **Italics:** Use italics for *general emphasis*.
- **Itemized lists:** Use bulleted lists whenever it aids with clarity.
  Do not include full stops on each item for short lists and sentence fragments.
  For lists with multiple sentences on each bullet (like this one), consistently use
  full stops on all items.
- **Inline headings:** Inline headings, where the heading is on the same line as a
  paragraph of text, should be formatted like this, using a boldfaced colon.
  Use this format consistently for inline headings within itemized lists.
- **Em dashes:** Use em dashes *only* when they are the best punctuation for the
  sentence. Prefer full stops, commas, colons, or semicolons as appropriate.
  When you do use em dashes—like this—follow American style, without spaces around the
  em dash.
- **Conjunctions:** Write “and” rather than `+` or `&` in prose, list separators, and
  cross-references. Reserve `+` and `&` for code, identifiers, and proper names where
  they are part of the canonical form (for example, “Strunk & White”).
- **Hyphens:** Follow the Chicago Manual of Style (CMOS 7.85 and its hyphenation table).
  The cases most often handled wrong:
  - Hyphenate a compound modifier before a noun (“open-source tool”) but not after it
    (“the tool is open source”).
  - Never hyphenate an “-ly” adverb plus adjective (“highly cited paper”).
  - Leave familiar open compounds open even as modifiers (“high school student”, “real
    estate broker”).
  - Close up most prefixes (“nonprofit”, “preprocess”, “subset”); hyphenate only before
    a proper noun (“non-Western”) or to avoid misreading (“re-cover” a chair vs.
    “recover”).
  - Do not stack hyphenated modifiers; if a sentence accumulates several, rewrite it.
- **Section headings:** Use Title Case (Chicago Manual of Style rules) for H1 `#` and H2
  `##` headings (as in this document).
  For H3 `###` and H4 `####`, title case is optional but should be applied consistently.

## 6. Guideline Footer

Documents governed by these guidelines should include a footer that says “This document
follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.”
Rules:

- Include this footer in every document, unless it is impractical (for example, in
  auto-generated files).
- Use the exact text above.
  Do not paraphrase, shorten, or change the filename or repository link.
  The filename alone is stable across moves and discoverable by search, and the
  repository link points readers to the source.
- In Markdown or HTML, wrap the footer in HTML comment markers (`<!-- ` and `-->`).
- Place it at the **bottom** of the document, after all content.
  Bottom placement keeps the marker out of the reader’s way and is compatible with any
  document, including those that begin with YAML frontmatter (where a top-of-file HTML
  comment would conflict).
- Use exactly one footer per document.
  When moving or splitting docs, make sure every resulting file ends with the footer and
  no file has more than one.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
