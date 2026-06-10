# Practical Prose Guidelines

Version: v0.1 (last update 2026-05-11)\
Joshua Levy (github.com/jlevy) with agent assistance

The *Practical Prose Guidelines* are prescriptive rules for practical documents such as
articles, practical blog posts, research reports, design documents, specifications,
technical papers, and decision memos.

The `practical-prose-rubric.md` document can be used to score documents on these
measures of quality.
Every scoring failure there should map to a specific rule here, and every rule here
should be reviewable by a human or agent.

## Principles

These guidelines extend `pprose guidelines common-doc-guidelines` and
operationalize the seven practical-prose principles defined in
`pprose guidelines practical-prose-principles`: **Purposeful**,
**Truthful**, **Essential**, **Lucid**, **Verifiable**, **Maintainable**, and
**Humane**. The rules below turn those principles into prescriptive guidance for the 18
review dimensions; the companion `pprose guidelines practical-prose-rubric`
defines how to score a document against the same dimensions.

Practical writing serves a purpose.
Anything that adds distance between the reader and that purpose without adding necessary
context, evidence, or maintainability is friction.

## Six Groups, Twenty Dimensions

| Group | Dimension | Question it answers |
| --- | --- | --- |
| **Purpose** | P1. Suitability | Does the document give the reader what they need, in the form the task requires? |
|  | P2. Scope | Is the scope stated, and does it fit the actual scope of the work? |
|  | P3. Breadth | Are the relevant areas within scope covered? |
|  | P4. Depth | Are the important areas developed enough? |
| **Expression** | E1. Clarity | Does the writing read well? |
|  | E2. Coherence | Do the ideas progress smoothly? |
|  | E3. Concision | Does every section earn its place? |
| **Form** | F1. Organization | Are sections, headings, sequence, tables, figures, links, and cross-references arranged for navigation? |
|  | F2. Consistency | Does the document follow the chosen style guide or house style consistently? |
|  | F3. Formatting | Is the document visually and syntactically clean in its medium? |
| **Reasoning** | R1. Discipline | Are observation, judgment, interpretation, and implication worked through in order, with each higher rung supported by the prior? |
|  | R2. Soundness | Do claims follow from evidence through valid mechanisms and explicit assumptions? |
|  | R3. Precision | Are claims and terms specified at the right granularity? |
|  | R4. Parsimony | Is each load-bearing reasoning chain the cleanest, simplest sound argument possible for its conclusion? |
| **Grounding** | G1. Verifiability | Are claims traceable to specific sources, observations, or calculations? |
|  | G2. Factuality | Are the verifiable claims true and supported by cited evidence? |
|  | G3. Relevance | Do sources, citations, and reasoning chains bear on the document’s stated purpose? |
| **Judgment** | J1. Calibration | Does claim strength match evidence strength? |
|  | J2. Fairness | Are opposing positions argued at depth proportional to their plausibility and strength? |
|  | J3. Robustness | Do key claims survive plausible alternative interpretations? |

## In Brief

A good practical document does these things; the prescriptive rules below say how:

1. **States its task.** Names the question, decision, plan, or audience need it serves;
   surfaces the main answer or finding early enough that a skim recovers it (P1, P2).
2. **Covers what is relevant within scope.** Includes the case classes, prior work, and
   standard sources the domain calls for; develops important sections to the depth the
   stakes require (P3, P4).
3. **Reads cleanly.** Concrete words; one-job paragraphs; earned register; visible
   structure; consistent style; valid markup (E1-E3, F1-F3).
4. **Reasons in distinct steps, by the shortest sound path.** Observation, judgment,
   interpretation, and implication kept on separate rungs; mechanisms named where
   causation is asserted; precision matched to measurement; each load-bearing chain the
   minimum sufficient sound argument (R1–R4).
5. **Makes important claims checkable.** Source-traceable, faithful to the cited
   evidence, and tied to the document’s purpose; the strictness of the bar scaled to
   stakes (G1–G3).
6. **Matches confidence to evidence.** Claim strength tracks evidence strength; opposing
   positions argued proportionally; key claims tested against alternative interpretive
   lenses (J1–J3).
7. **Is easy to maintain.** Owner, status, dates, dependencies, and open questions per
   `pprose guidelines common-doc-guidelines`.

The 20 sections below give the prescriptive rules; the companion
`pprose guidelines practical-prose-rubric` provides the descriptive 0-5
scoring anchors. A review-time checklist organized the same way appears at the end of
this document under *Pre-Publish Self-Audit*.

### Relationship to common-doc-guidelines.md

`common-doc-guidelines.md` is the cross-document substrate.
The table below shows how its clauses relate to this layer:

| common-doc-guidelines clause | Where it applies |
| --- | --- |
| P1 Organizing Documentation (rapid orientation, filenames, ownership/audience/cadence) | Cross-document only; not scored by this rubric |
| §2.1 Explain motivations and background | Absorbed under P1 Suitability and the Humane principle |
| §2.2 Give context gradually and efficiently | Absorbed into P1 Suitability rule 7 (summary-then-link) |
| §2.3 Keep details close (docstrings, YAML descriptions) | Cross-artifact co-location; not scored |
| §2.4 Avoid duplication | Absorbed into E3 Concision rule 2 |
| §2.5 Describe present state, not what it replaced | Absorbed into E3 Concision rule 5 (common agent failure mode) |
| §3.1 Be clear and concise | Absorbed into E1 Clarity and E3 Concision |
| §3.2 Be detailed and specific | Absorbed into P4 Depth, G1 Verifiability, R3 Precision |
| §3.3 Headings cleave to subject contours | Absorbed into F1 Organization rule 9 |
| §3.4 Be engaging and warm | Referenced as Tone / Reader Respect contextual modifier in the rubric |
| §4.1 Respect reader’s intelligence | Absorbed under the Humane principle and P1 Suitability / P4 Depth |
| §4.2 Banned extravagant words list | Canonical list lives in common-doc-guidelines; referenced from E1 Clarity rule 4 |
| §4.3 Cut pompousness, meta-commentary, pedantry | Absorbed into E1 Clarity rules 3 and 6 |
| E1 Em-dash discipline | Absorbed into F2 Consistency rule 7 |
| E2 Guideline Footer | Operational marker; not scored by this rubric |

## Purpose Dimensions

### P1. Suitability

*Description:* The document serves the purpose it was written for.
A document can be clear, factual, and balanced and still fail Suitability if the reader
can’t extract the needed output, or if the purpose wasn’t named in the first place.

**Rules:**

1. **State the task.** The document names the question, decision, workflow, plan, or
   audience need it serves.
   If the task is implicit, the reader can’t tell whether the document has done it.

2. **The needed output is recoverable from a skim.** A reader who reads only the
   introduction, summary, or top-level section headings should understand the document’s
   main output. Don’t bury the central answer, instruction, plan, or finding inside §6.4.

3. **Cut sections that don’t serve the stated task.** Sections that are interesting but
   tangential are friction.
   Fold them into a related section, move them to an appendix, or drop them.

4. **Name what the document doesn’t do.** When the task is partially answered, list open
   questions, deferrals, or blockers explicitly.
   The reader should know what they still need before using the document.

5. **Match output shape to task shape.** A decision memo has a recommendation; an audit
   has findings; a plan spec has milestones and constraints; technical documentation has
   concepts, procedures, or references; a post-mortem has corrective actions.
   A document that elides the shape its task demands fails Suitability even when the
   underlying analysis is sound.

6. **Name the reader burden the document removes.** State what cognitive, operational,
   or ethical work the prose performs for its reader.
   A status update removes the burden of asking “where are we?”; a runbook removes the
   burden of remembering an irreversible sequence; an audit removes the burden of
   suspicion. Naming the burden sharpens Suitability beyond “state the task”; documents
   that state a task without naming the burden it removes tend to drift into
   structure-for-its-own-sake.

7. **Open with a summary; link to depth.** Start with the summary a reader can act on,
   then link to deeper material for those who need it.
   A long document whose first screen is preamble or definitions fails this rule even
   when the depth is excellent.
   The shape is summary → link, not chapter → conclusion: the reader who stops after the
   summary should still leave with the document’s main output.
   (Cross-references common-doc-guidelines §2.2 “Give context gradually and
   efficiently.”)

### P2. Scope

*Description:* The document declares its scope, and the declared scope matches the
actual scope of the work.
Scope failures are upstream of Breadth and Depth: a document with no declared scope
cannot be evaluated for whether it covers everything relevant.

**Rules:**

1. **State the scope explicitly.** Name one system, one time window, one workflow, or
   one decision the document covers.
   A reader should be able to tell from the opening what is in scope and what is not.

2. **Declared scope matches actual scope.** The body of the document covers what the
   opening declared. A document that declares a narrow scope but drifts into adjacent
   topics violates Scope even when the drift is interesting.

3. **Flag mid-document scope shifts.** If the work surfaces a question that falls
   outside the declared scope, name it as out-of-scope and either defer it explicitly or
   update the scope statement to include it.

4. **Out-of-scope omissions are not breadth failures.** A document with a narrowly
   declared scope is not penalized under P3 Breadth or P4 Depth for omitting
   out-of-scope material; it is penalized under P2 Scope only if the boundary is
   undeclared or drifts.

5. **Name what the document is not competent to conclude.** Scope says what is in; this
   rule says what the evidence in scope cannot decide.
   A market-sizing brief should say it cannot conclude unit economics; an incident
   postmortem should say what it cannot determine about root cause without further
   telemetry; an audit should say which claims it tested versus accepted on assertion.
   Especially load-bearing for AI-authored prose, where claim creep is easy.

### P3. Breadth

*Description:* Within the boundary set by P2 Scope, the document includes the relevant
facts, cases, contexts, prior work, alternatives, edge cases, and affected areas.
Breadth is the *what is covered* question; Depth (P4) is the *how thoroughly* question.
Both are judged within declared scope: a narrow document with a narrowly stated scope
can score 5 if it covers the relevant material within that scope.

**Rules:**

1. **Breadth is judged against declared scope.** Within the boundary set by P2 Scope,
   all relevant material classes are present.
   Scope declaration itself is scored under P2; this dimension scores whether the
   declared boundary is filled.

2. **Relevant prior work and standard sources are present.** When the domain has an
   established reference, source, or precedent, cite it.
   A document that ignores obvious prior work fails breadth even when its own reasoning
   is sound.

3. **Cover the affected case classes.** Risks of different kinds (technical,
   competitive, macro, regulatory, precedent-based) should each be considered where the
   domain calls for them.
   A treatment that includes one class and silently omits another is a breadth failure
   even when each included item is well-handled.

4. **Out-of-scope omissions are not breadth failures.** A document with a narrowly
   declared scope is not penalized for omitting out-of-scope material; that is scored
   under P2 Scope only if the boundary is undeclared or drifts.

### P4. Depth

*Description:* The important parts of the document are developed to the level of detail,
specificity, evidence, and explanation the task requires.
Depth answers *how thoroughly* once Breadth has answered *what is covered*.

**Rules:**

1. **Section depth matches section importance.** Sections the document’s purpose depends
   on deserve more detail than less important ones.
   If §X carries the document, it should not be thin while tangential §Y is the densest
   section.

2. **Specificity is part of depth.** Citing endpoints when the full series adds
   information is shallow.
   “Throughput rose from 1.2k to 4.8k req/s” shows endpoints; the full series (1.2k,
   1.8k, 2.5k, 3.1k, 4.0k, 4.8k) shows trajectory.

3. **Quantify “small,” “large,” “rapid,” “slow.”** Vague magnitude words in a scoped
   factual claim are depth failures, not just clarity failures.
   (Vague words in ordinary prose without a quantitative claim are scored under E1
   Clarity; vague countables where a specific term exists are scored under R3
   Precision.)

4. **Name the instances when you cite a count.** “13 endpoints affected” should be
   followed by the names when space permits.

5. **Develop key arguments at the level the stakes require.** For high-stakes, external,
   or decision-bearing documents, key claims should be argued at full depth (mechanism,
   evidence, counter-evidence, falsification conditions).
   For low-stakes operational notes, depth proportionate to the operational decision is
   sufficient.

## Expression Dimensions

### E1. Clarity

*Description:* Is the language readable and clear, with good command of language and
correct spelling and grammar?

**Rules:**

1. **Use the most concrete word that fits.** “Compress” is clearer than “experience
   downward pressure.” “Latency rose from 80ms to 105ms at p99” is clearer than “latency
   degraded significantly.”
   “The parser is flaky” is too vague; say what fails, how often, under what conditions,
   and how certain you are about the cause.
   Vague magnitude words ("rapid," “large,” “significant”) should be quantified or
   removed.

2. **Cut unnecessary qualifiers.** “It is important to note that X” is usually better as
   “X.”

3. **Eliminate meta-commentary.** “This section will discuss …” and “As we will see …”
   narrate the document instead of advancing its purpose.
   Exception: standards, rubrics, runbooks, and other process documents may include
   structural commentary (how dimensions map to rules, how to score, when to apply a
   pass) when that commentary is what the document is *for*.

4. **Earn extravagant register; don’t deploy it as emphasis.** The canonical
   banned-register list lives in common-doc-guidelines §4.2 (“incontrovertibly,”
   “emphatically,” “definitively,” “unequivocally,” “massive,” “monumental,” “profound,”
   “transformational,” “seismic,” “paradigm-shifting,” “will revolutionize,”
   “structurally outmaneuvered,” “successfully executing,” “crushing it”). These words
   overstate the evidence and are off-limits as emphasis substitutes.
   Use strong language when it carries information, clarifies a distinction, or
   preserves a hard-won idea, and pair it with the citation that earns it on the same
   line. Honor any domain-specific extension list, including
   `pprose guidelines ai-prose-corrections`, which lists hollow and
   marketing-register fingerprints of unedited LLM output that the §4.2 list doesn’t
   catch. Rhetoric is not decoration when it compresses thought; it is decoration when it
   adds only force.

   Four named voice failures are useful as a self-check: *marketing voice* ("expert tips
   you won’t find anywhere else"), *know-it-all voice* ("follow our advice and you’ll be
   fine"), *it’ll-be-easy voice* ("just learn these 17 tricks"), and *lifeless voice*
   (dry writing with no care in it).
   The first three are register violations under this dimension; the fourth is the Tone
   / Reader Respect check.

5. **Earn rhetorical force; cut symmetry-for-its-own-sake.** Parallel structures (*“It’s
   not X, it’s Y”*; *“Not just X but Y”*; *“X did A, ours does B”*; *“Where X asks A, Y
   asks B”*) are licensed when X is a position someone actually holds and the contrast
   carries meaning, or when the structure improves memory or clarifies a distinction.
   Otherwise, drop the X-half and state Y directly.
   Rhetoric that adds only symmetry, drama, or emphasis substitutes form for substance.

6. **No pedantic, pedagogical, or self-referential prose.** *(Common agent failure
   mode.)* Avoid declarations of canonicality (“this is the canonical X”),
   justifications of word or name choices (“we use the term Y because…”), reading-order
   instructions to the reader (“start with section 2”), and over-definition of obvious
   terms. The doc should *be* clear, not announce its clarity.
   Exception: glossaries, terminology sections, and the same standards/rubrics/runbooks
   carve-out under rule 3 may define terms or describe structure when that is the
   document’s purpose.

### E2. Coherence

*Description:* How well can the reader follow the progression of ideas across the whole
work? This metric reflects only the prose-level flow; it does not include logical
coherence (covered under R2 Soundness) or scaffolding like heading hierarchy, tables,
figures, and links (covered under F1 Organization and F3 Formatting).
Coherence here is about whether ideas progress smoothly when read sentence to sentence.

**Rules:**

1. **Each paragraph has one job.** Long paragraphs that mix observation, interpretation,
   and next steps tax the reader.
   Split into one-job paragraphs.
   The first sentence previews the job; a reader who skims first sentences should still
   understand the spine.

2. **Transitions bridge, not stub.** Adjacent paragraphs and sections should connect.
   When a later section refers back, repeat the prior point verbatim or by clear
   paraphrase. “As shown above” without the point stated is friction.

3. **The document progresses without backtracking.** If a later section reaches a
   conclusion or instruction that contradicts an earlier passage, reconcile or revise
   rather than leaving the contradiction implicit.

4. **Ideas arrive with setup.** Don’t introduce a new construct, framework, or label
   without first establishing what it means and why it matters.

### E3. Concision

*Description:* The writing carries only the content the task requires.
Padding, repetition, and decorative content fail concision even when each sentence is
clear and the document coheres.

**Rules:**

1. **Cut anything that advances no purpose.** If removing a sentence loses no
   information, orientation, or reader-context the document needs, cut it.
   Orienting sentences, analogies, and brief human context don’t always advance a claim
   but can advance understanding; keep them when they earn their place.
   Apply at section, paragraph, and sentence level.

2. **Avoid duplication across sections.** When the same fact appears in §1.3 and §2.1
   and §2.8, audit which section it belongs to and reference it from the others.

3. **Each section earns its place.** A section that doesn’t serve the purpose or stage
   needed evidence or context shouldn’t exist.
   If a template lists a section but its content adds no marginal information, mark it
   deferred or compress to a line.

4. **Frontmatter is for machine-readable fields.** YAML frontmatter holds structured
   metadata downstream code or readers consume (title, status, dates, schema tokens,
   IDs, enums). Don’t put prose-only claims in frontmatter.
   If downstream code needs a value, make it structured frontmatter and explain the
   field in the body where a human reader will encounter it.

5. **Describe the present state, not what it replaced.** *(Common agent failure mode.)*
   Write as if the current design, system, or naming has always existed.
   Replacement history—“this function was previously named X,” “under the new layout,”
   “we used to use Y,” “removed Z”—pollutes the reader’s context with deprecated
   concepts they would otherwise never have to learn.
   Git history is the authoritative record of what was removed; the document is the
   record of what *is*. Exception genres where history is the point: migration guides,
   postmortems, decision records, changelogs, deprecation notices, governance/versioning
   sections, and one-line predecessor pointers where a future reader needs to find a
   predecessor (“see commit `abc123` for the prior shape”). The test is whether the
   history serves the reader’s task or merely records the author’s path.
   (Cross-references common-doc-guidelines §2.5.)

## Form Dimensions

Form covers the document as a structured artifact — arrangement, style discipline, and
markup — as distinct from the sentence- and paragraph-level language of the Expression
dimensions. These three descend from the Maintainable principle.

### F1. Organization

*Description:* The document’s sections, headings, sequence, tables, figures, lists,
links, and cross-references help readers navigate the material.

This dimension is about *arrangement*. Whether the markup renders correctly and follows
medium conventions is F3 Formatting; whether terminology and house style are consistent
is F2 Consistency.

Visual elements aren’t required.
A tightly written prose document with no tables or figures can be excellent.
But when these elements are present, they should be well-arranged.

**Rules:**

1. **Heading hierarchy is logical and consistent.** Don’t skip heading levels (h1 → h3
   without h2). Heading depth should track conceptual depth, not document length.
   Sections should be sized to their content: no h6 for a single sentence; no
   20-paragraph wall under a single h2.

2. **Sections are arranged in the order the task requires.** Decision memos lead with
   the recommendation; audits lead with findings; reference docs let readers jump
   directly to the entry they need.
   Output shape matches task shape (cross-reference P1 Suitability).

3. **Tables earn their tabular shape.** A table is the right shape when items are
   parallel rows with a fixed schema and at least two filled columns of comparable
   density. A 3-row table with one filled column is a sentence in disguise; convert to
   prose. A 12-row table with 8 columns of dense data is the right shape; keep it.

4. **Figures have captions and live next to their reference.** A figure without a
   caption that explains what it shows is friction.
   A figure pages away from the prose that references it forces the reader to scroll
   back and forth.

5. **Lists earn their place.** Lists are right when items are parallel and discrete.
   If list items vary in scope or depth, paragraphs are clearer.

6. **Links target stable anchors.** Prefer permalinks, filename and section anchors, or
   commit-pinned URLs over links that may rot.
   In internal docs, prefer filename-only references when they are unique.

7. **Cross-references resolve and name what they reference.** “See §2.8” requires §2.8
   to exist and contain what the reference suggests.
   Prefer “See §2.8 (named cruxes)” over the bare “See §2.8.” Audit cross-references on
   every revision.

8. **Visual elements earn their place.** Don’t add a table to satisfy a template if the
   content isn’t tabular.
   Don’t add a figure for decoration.
   When tables, figures, code blocks, or diagrams appear, they should carry information
   that prose alone wouldn’t convey as well.

9. **Headings name what the section contains.** *(Common agent failure mode.)* Headings
   should cleave to the true contours of the subject matter; “Overview,” “Background,”
   “Introduction,” “Notes,” “Details,” “Misc,” and “Additional Information” are flagged
   when they are the only signal of a section’s contents.
   Prefer “Why the migration is driven by compliance” over “Background”; prefer “Cache
   eviction trade-offs” over “Notes.”
   Templates that prescribe generic headings should be filled in with subject-specific
   subheadings, not left as-is.
   (Cross-references common-doc-guidelines §3.3.)

### F2. Consistency

*Description:* The document follows the chosen style guide or house style consistently.
A document can be perfectly understandable and still stylistically inconsistent;
conversely, a document can be style-guide compliant but unclear, overlong, or wrong.
Consistency isolates the editorial-polish question from the readability question (E1
Clarity) and the markup-validity question (F3 Formatting).

**Rules:**

1. **Spelling dialect, capitalization, punctuation, hyphenation, and number/date formats
   are consistent.** Pick one convention (American or British English; ISO or US date
   format) and hold it.

2. **Product names, acronyms, technical terms, and entity names are styled
   consistently.** “API” throughout, not “Api” or “api”; “GitHub” not “Github.”
   Acronyms defined on first use, then used consistently.

3. **Lists and headings use parallel syntax where parallelism is expected.** All list
   items as noun phrases, or all as imperative verbs, not mixed.
   Headings consistently in title case or sentence case across a document.

4. **Citation style is consistent.** Choose Chicago, APA, footnote, or a project
   convention and apply it across all citations in the document.

5. **Register does not drift without reason.** A document does not shift between formal
   and casual register, or between technical-paper and blog-post tone, except where the
   genre calls for it (an inline aside, a quoted source).

6. **Domain-specific banned words and house-style conventions are followed.** *(Common
   agent failure mode.)* A `conventions.md` in the doc’s scope (banned-register words,
   confidence-tag conventions, citation-format requirements) is honored consistently.
   Agents tend to reach for register the project has already ruled out—overconfident
   words, overblown adjectives, marketing-style intensifiers—even when the rule list is
   short and in the same repo.
   Treat the project’s banned-word list as binding, not advisory.
   For practical-prose itself, the binding extension is
   `pprose guidelines ai-prose-corrections`, which catalogs LLM-register tells
   and their corrections.

7. **Em-dash discipline.** *(Common agent failure mode.)* Use em dashes only when they
   are the best punctuation for the sentence; prefer full stops, commas, colons, or
   semicolons. When an em dash is used, follow American style: no surrounding spaces
   (“context—like this”), not spaced (“context — like this”). Spaced em-dash overuse
   marks unedited agent prose; the convention applies even when the author finds the
   spaced variant readable.
   (Cross-references common-doc-guidelines E1.)

### F3. Formatting

*Description:* The document’s markup and visual presentation are clean, valid, and
compatible with the chosen medium.
Distinct from F1 Organization (are the parts arranged well) and F2 Consistency (does the
document follow house style consistently).
Formatting is the most deterministic of the three; most rules here are lintable.

**Rules:**

1. **Markdown, HTML, or document markup renders correctly.** No broken table rendering;
   no unclosed code fences; no malformed frontmatter.

2. **Lists, tables, code fences, block quotes, links, images, footnotes, and frontmatter
   are syntactically valid.** Backtick fences match; reference-style links resolve to
   their definitions; footnote anchors round-trip.

3. **Whitespace, indentation, and line breaks are consistent.** Mixed tab/space
   indentation, inconsistent blank-line counts between sections, and stray trailing
   whitespace fail this rule.

4. **Emphasis formatting is used according to convention.** Bold for key terms; italics
   for general emphasis; not the inverse.
   No nested bold-italic for decoration.

5. **Required headers, metadata, and footers are present and correctly placed.** The
   `common-doc-guidelines.md` footer placement (bottom-of-file, HTML-comment-wrapped) is
   honored; frontmatter sits at the top above any other content.

6. **The rendered document has no obvious production defects.** No raw HTML escape
   sequences leaking into prose; no Markdown-source artifacts visible in the rendered
   output; no broken images or missing alt text.

## Reasoning Dimensions

### R1. Discipline

*Description:* The practice of climbing the ladder of inference rung by rung in order
(observation → judgment → interpretation → implication), with each higher rung supported
by the rung below it.
Each rung is named on its own terms; none is skipped, none is blended into its neighbor.
Implications rest on sound interpretations, which rest on sound judgments, which rest on
sound observations.

Discipline is distinct from Soundness (R2). Soundness tests whether each step in the
chain is itself valid; Discipline tests whether the rungs are climbed in order and exist
as distinct rungs at all.
Both can fail independently: a sound chain can still be fused into one sentence or its
rungs can be presented out of order, and a well-ordered chain can still be unsound.

The four rungs, with one example carried through them:

1. **Observation:** what is directly visible in the data ("the error rate on /v2/upload
   rose from 0.4% to 1.7% between Monday and Friday last week").
2. **Judgment:** magnitude or significance assigned to an observation ("this is the
   largest weekly swing on that endpoint in six months").
3. **Interpretation:** meaning attached to the observation plus judgment ("the swing
   coincides with the new release and concentrates on the auth path, not the upload path
   itself").
4. **Implication:** downstream consequence drawn from the interpretation ("we should
   roll back the auth change for /v2/upload until the root cause is found").

(Loosely based on Argyris’s Ladder of Inference, *Action Science* (1985). The four rungs
above are an adaptation for analytical writing.)

**Rules:**

1. **Don’t skip rungs.** A leap from observation to implication ("error rate up → roll
   back the release") hides the judgment and interpretation steps that would have to be
   true. Each rung either appears or is explicitly marked as `[ASSUMING: ...]`.

2. **Don’t blend rungs in one sentence.** “The error rate is spiking sharply on the new
   endpoint, signaling a regression in the auth path” fuses observation ("spiking"),
   judgment ("sharply"), interpretation ("on the new endpoint"), and implication
   ("signaling a regression in the auth path") into one clause, so the reader cannot
   tell which sub-claim carries the evidence.
   Decompose into separate sentences, each with its own rung.

3. **Each rung carries its own evidence.** A citation that supports the observation does
   not transfer up the ladder.
   Argue (or mark as assumption) the judgment, the interpretation, and the implication
   separately, even when each step seems obvious.

4. **Use rung tags in audits, evals, and high-stakes analysis; preserve rung separation
   without tags in polished prose.** For audit work, internal evals, high-stakes
   analysis, or agent-facing drafts, mark key claims with `[observed]`, `[judged]`,
   `[interpreted]`, or `[implied]` so the rung is machine-checkable.
   In polished prose intended for human readers, omit the tags but keep the rungs in
   distinct sentences with transition signals.
   The discipline is what scores; the tags are one way to enforce it.

5. **Mark transitions.** When moving up a rung, signal it ("from this we judge…", “which
   we interpret as…”, “which implies…”). The reader should always know which rung the
   sentence is on.

### R2. Soundness

*Description:* Content is logically organized, with terms and statements well-defined,
reasoning sound, and the chain from evidence to claim visible.
Soundness focuses on the document’s logical structure; the “multiple perspectives
considered” dimension is broken out as Fairness (J2).

**Rules:**

1. **Mechanism > correlation.** “X correlates with Y” is weaker than “X drives Y because
   [named mechanism].” Where you assert causation, name the mechanism.
   Where you can only show correlation, say so.

2. **Don’t bridge “promising signal” to “outcome confirmed.”** A signal is evidence at
   one level (an early indicator, a passing test, a leading metric).
   A claim about the eventual outcome sits at a different level.
   The leap requires intermediate evidence; state the leap as a leap, or substantiate
   the intermediate steps.

3. **Surface unstated assumptions.** If a claim depends on a premise the doc doesn’t
   argue, state it as an assumption rather than slipping it in as background.
   Mark with `[ASSUMING: ...]` inline, or call out a “Key assumptions” block when stakes
   are high. The reader should be able to challenge the claim either by challenging the
   reasoning or by challenging a named assumption, never by uncovering one the writer
   hid.

4. **Engage the strongest counter-evidence.** When asserting risk X, address
   counter-evidence in the same document that argues against X. Ignoring
   counter-evidence in your own document is a soundness failure.

5. **Asserted ≠ argued.** If the claim is complex, either argue for it (with named
   primitives and numerical comparisons) or say it’s an assertion subject to falsifiable
   conditions. Bare assertions of complex claims fail soundness.

6. **Define terms when they carry weight.** A term the document depends on gets a
   definition on first use.

7. **Internal consistency.** The same fact, claim, or number stated identically every
   time it appears. Discrepancies erode all other reasoning.

8. **Counterfactual test for causal and explanatory claims.** For each causal or
   explanatory claim, name what we would expect to see if the explanation were wrong.
   A correlation that survives the counterfactual is stronger than one that doesn’t; a
   mechanism story that predicts only what already happened is unfalsifiable.
   See the *Failure-Mode Questions* table in
   `pprose guidelines practical-prose-rubric` for prompts by claim type.

### R3. Precision

*Description:* Claims and terms are specified at the right granularity for the domain
and audience. Generic vocabulary in place of available specific vocabulary is
imprecision, even when the generic phrasing is true.
Precision is distinct from Clarity (E1, which is about register and readability) and
from Breadth/Depth (P3/P4, which are about scope completeness and section development):
Precision is the granularity *within* each individual claim.

**Rules:**

1. **Use the most specific term the audience can parse.** “Adenocarcinoma” beats
   “cancer” when readers are oncologists; “EGFR-mutant non-small-cell lung
   adenocarcinoma” beats “adenocarcinoma” in a tumor-board memo.
   Match precision to audience expertise: don’t dumb down for experts, don’t jargon-up
   for generalists.

2. **Refer to entities by their proper name.** Use the specific identifier the audience
   would recognize: a versioned model name rather than “the model,” a numbered statute
   rather than “the rule,” a specific instruction-set extension rather than “the SIMD
   extension,” a dated filing rather than “the recent filing.”

3. **Avoid umbrella terms when sub-distinctions matter.** “Capex” hides maintenance vs
   growth; “users” hides MAU vs DAU vs paid; “latency” hides p50 vs p99; “revenue” hides
   recurring vs one-time.
   If the distinction matters to the claim or task, use the precise term.

4. **Quantitative precision matches measurement precision.** “47.3%” implies 0.1%
   resolution; if the source measures to 1%, write “47%.” Spurious precision is a
   factuality failure dressed up as rigor.

5. **No vague placeholders for countables.** Replace “several,” “various,” “a number
   of,” and “many” with either a count (“12”) or named items (“AWS, Azure, GCP, OCI”).
   Vague countables are breadth/depth failures *and* precision failures.

### R4. Parsimony

*Description:* The chain from cited evidence to the document’s headline claims uses the
cleanest, simplest sound argument available.
Length is not the metric; minimality given the per-step warrants in use is.
A long chain of strong deductive steps (a formal proof, a multi-step regulatory
cross-walk) is parsimonious when no shorter chain of the same warrant strength exists; a
short chain of weak inductive gestures is non-parsimonious when it elides intermediates
the conclusion requires.

Parsimony presupposes Soundness (R2): when a step is unsound, a longer sound chain would
do less damage to the conclusion, so the chain as written cannot be the most
parsimonious sound argument.
When Soundness fails materially on the headline claims, Parsimony is scored 0.

Distinguished from neighbors:

- **E3 Concision** is prose-level economy (words, paragraphs, redundant phrasing).
  Parsimony is argument-level economy (rungs in the inferential chain).
- **G3 Relevance** asks whether each source or section is on-task.
  Parsimony asks whether the reasoning *within* an on-task chain uses the minimum sound
  steps.
- **R1 Discipline** asks whether the rungs are climbed in order and named on their own
  terms. Parsimony asks whether the chain is the minimum.
- **R2 Soundness** asks whether each step is valid in itself.
  Parsimony asks whether the chain *shape* is minimum given the per-step warrants.

**Rules:**

1. **Prefer citation over re-derivation when both serve the same purpose.** Where direct
   evidence is available (a published result, a measured value, a settled definition),
   citing it is usually shorter than re-deriving it.
   Re-derivation is warranted when it adds inspectability (showing the math), confidence
   (letting the reader audit the step), or pedagogy (explaining for the audience); it is
   padding when none of those apply and the cited result would do the same work.

2. **Cut non-load-bearing steps.** Each rung in a load-bearing chain should be
   necessary; if removing it leaves the argument intact, remove it.
   Steps that restate the preceding rung in different words, add illustrative color, or
   re-conclude what was already concluded are padding.

3. **Match chain length to warrant strength.** Long chains of strong, deductive steps (a
   formal proof, a derivation from named axioms, a regulatory cross-walk) are
   parsimonious when no shorter chain of the same warrant type exists.
   Short chains of weak, inductive steps are not parsimonious when their brevity was
   achieved by skipping rungs the conclusion requires.

4. **Don’t truncate required intermediates.** Where a claim requires N intermediate
   inferences to reach with the warrants in use, all N must appear.
   A 2-step gesture substituted for a 5-step required chain is a Parsimony failure (and
   typically a Soundness failure as well).

5. **Prefer the most direct warrant available.** Where deduction will work, use
   deduction; where a measurement exists, cite it; where the mechanism is known, name
   it. Substituting a weaker warrant (“X plausibly causes Y”) when a stronger one is
   available (“X causes Y via [mechanism], see [source]”) makes the chain longer than it
   needs to be.

6. **Parsimony applies to load-bearing chains.** Illustrative examples, motivational
   background, and worked-out edge cases are exempt.
   The test runs on the chain from cited evidence to the document’s headline claims, not
   on every inference in the document.

## Grounding Dimensions

### G1. Verifiability

*Description:* Claims are stated specifically enough to be checkable, and traceable to
specific sources, observations, calculations, or explicit assumptions.
A document scores high on Verifiability when a competent reader could check its claims
from what the document provides, before any external lookup.
Verifiability is text-internal: it tests how well the document equips the reader to
audit. **Factuality (G2)** is world-aware: it tests whether the audit, when performed,
passes.

A claim that is too vague to check is a Verifiability defect even when sources are
cited: if “things have grown rapidly” has no quantitative referent, no source can
confirm or refute it.
Specificity is the precondition for source-traceability.

**Rules:**

1. **Claims are stated specifically enough to be checkable.** A claim a reader could in
   principle confirm or refute by consulting sources, observations, or calculations.
   Vague magnitude words ("rapid," “many,” “in greater volume,” “increasingly”) without
   a stated referent or comparison fail this rule even when the underlying assertion
   might be true; the document has not made a checkable claim.
   Score R3 Precision for terminology specificity; this rule covers the claim-level bar.

2. **Quantitative claims are source-traceable; the bar scales with stakes.** For
   high-stakes, external, or decision-bearing documents (research reports, audits,
   decision memos, deep research), every quantitative claim has at least one primary
   source (official documentation, filings, press releases, transcripts, source code,
   datasets, or first-party measurements).
   Secondary sources (news aggregators, blog summaries, third-party analyses) can
   corroborate but don’t substitute.
   For low-stakes operational notes and lightweight status updates, cite the source when
   the number is material; otherwise mark the basis or measurement context (for example,
   “local timing run, n=20” or “Grafana, 7d window”).

3. **Citations are specific enough to verify.** Enough information that a reader can
   find the exact passage: a URL, a document or accession ID, a date, a commit SHA, a
   page or section number.
   “The release notes” is vague; “the v2.4 release notes, §3.2 ('breaking changes')” is
   verifiable. Social-media posts need post IDs.
   Press releases need dates.
   Filings need accession numbers or filing dates.

4. **Confidence tags require a source per claim.** `[VERIFIED]` without naming what was
   verified or against which source is opaque.
   Pair every confidence tag with a specific source pointer.
   For derived facts, show the calculation inline: `[DERIVED: 89.6 / 614.5 = 14.6%]`.

5. **Calibrated uncertainty is not a defect; uncalibrated assertion is.** `[UNVERIFIED]`
   is preferable to silently inheriting an unverifiable claim.
   `[ESTIMATED]` with the triangulation method stated is preferable to a bare point
   estimate. A claim explicitly marked as speculative or unverified, with its basis
   named, does not lower the Verifiability score.
   A claim asserted as fact without the certainty the evidence supports does.
   The point is that the reader knows the claim’s epistemic status, not that every claim
   is fully resolved.

6. **For central claims, name what would invalidate them.** Beyond citing sources, state
   what a skeptical reader should inspect to falsify the claim, and what observation
   would change the conclusion.
   Feynman’s first principle: you must not fool yourself, and you are the easiest person
   to fool. See the *Failure-Mode Questions* table in
   `pprose guidelines practical-prose-rubric` for claim-type-specific
   prompts.

7. **Links serve readers, not only verification.** Beyond citations, two further link
   kinds carry weight in web-published documents: *recommended* links (resources called
   out with context—who made them and why they matter) and *elaborative* links (detail
   or context on a passing mention, needing no setup beyond the inline link).
   Choose each link deliberately and prefer the best available source; a laundry list of
   low-value links dilutes credibility and fails G3 Relevance.

### G2. Factuality

*Description:* The document’s verifiable claims hold up when checked against the world,
at the asserted strength, for the asserted entity, date, and scope.
Verifiability (G1) is text-internal: does the document let the reader audit?
Factuality is world-aware: does the audit, when performed, pass?

Truth here means: **the assertion strength matches the available evidence.** A claim
asserted as certain when the evidence is uncertain is a Factuality defect.
A claim asserted as speculative, with its speculative status explicit and its basis
named, is **factually correct** even if the underlying proposition cannot be checked —
the document is telling the reader the truth about what is known.

Scoring Factuality is corroboration-driven, not citation-driven.
Cited sources are the cleanest mechanism, but a verifiable claim can be corroborated by
authoritative external evidence when no citation is present.
A claim is a Factuality defect when it is *asserted as fact* and *cannot be
corroborated*; it is **not** a defect when it is flagged as uncertain or speculative
with a stated basis.

Reviewer access limits are not document defects.
A claim with a reachable primary source that the reviewer happens to be unable to access
(paywalled, in a language the reviewer doesn’t read, or in a private system) counts as
neutral, not a Factuality slip.
The reason note records the access limit so a later reviewer with access can complete
the audit.

**Rules:**

1. **Verifiable claims are corroborated.** When the document makes a checkable claim,
   that claim is supported either (a) by a cited source the reader can reach, or (b) by
   authoritative external evidence accessible at appropriate effort.
   A claim that cannot be corroborated and is asserted as fact without hedging is a
   defect.

2. **Cited sources support the claim at the asserted strength.** A source that says “X
   is one factor” does not support a claim that “X is the dominant factor.”
   A source about a prior period does not support a claim about a current period without
   an explicit bridge.

3. **Numbers in prose match cited sources, or explicitly disclose rounding, aggregation,
   unit conversion, or derivation.** A measurement of 14.6% in the source can appear as
   “~15%” in prose only if the rounding is signaled (an approximation marker, a stated
   rounding policy, or a parenthetical such as “(14.6% rounded)”). Silent rounding,
   silent aggregation across categories, or silent unit conversion all fail this rule.

4. **Entity, date, and scope of citations match the claim.** Claims about a product
   should cite that product’s own sources, not third-party commentary about it.
   Claims about the current period should cite current-period data, not extrapolations
   from a prior period without an explicit bridge.

5. **Sources represent the cited entity, not its inverse.** An advocate’s note quoted as
   if it were neutral, an opinion piece quoted as if it were a primary source, or a
   commentary quoted as if it were the underlying data all fail accuracy even when the
   citation is technically verifiable.

6. **No hallucinated or invented sources or claims.** Every cited URL, document ID,
   transcript reference, or author resolves to a real artifact that contains the cited
   content. The same bar applies to the claims themselves: anything that reads as a fact
   but is detached from a source or from supporting logic—an invented statistic, a
   fabricated detail, an asserted specific presented as settled—counts against
   Factuality even when no source is cited at all.
   Confidence in this is harder to self-audit than the other rules; pair high-stakes
   citations with quoted excerpts when feasible.

7. **Calibrated uncertainty satisfies Factuality; uncalibrated certainty fails it.**
   When a claim cannot be corroborated from available evidence, the document
   acknowledges this explicitly and states the basis on which the claim is made anyway.
   A speculative claim labelled speculative, with its basis stated, is factually
   correct. An unhedged claim made as if it were settled, where the evidence does not
   settle it, is a Factuality defect, even if the claim happens to be true.

### G3. Relevance

*Description:* Sources, citations, and intermediate reasoning chains relate directly to
the document’s stated purpose.
Material that doesn’t bear on the main task, including tangential sources, performative
citations, and digressive arguments, should be cut or marked as background.
Relevance tests whether each piece of evidence and each section does work toward the
purpose declared in P1 Suitability and P2 Scope.

Distinguished from neighbors:

- **P2 Scope** declares what the document covers; Relevance tests whether the content
  inside that boundary earns its place.
- **E3 Concision** is prose-level economy (words, paragraphs, redundant phrasing).
  Relevance is content-level economy (sources, sections, points).
- **G1 Verifiability** asks whether claims trace to sources.
  Relevance asks whether the traced sources connect to the document’s purpose.
- **G2 Factuality** asks whether sources support the claims made.
  Relevance asks whether those claims matter for what the document is for.
- **R4 Parsimony** asks whether each load-bearing reasoning chain uses the minimum sound
  argument. Relevance asks the same question one level up: whether each source and
  section is load-bearing at all.

**Rules:**

1. **Cite only sources that bear on the purpose.** A source supplying tangential context
   can be referenced inline but should not be anchored as evidence for a headline claim.
   Performative citations, where sources are cited to demonstrate diligence rather than
   to support a claim, dilute the audit trail and obscure which sources actually
   load-bear.

2. **Cut sections that don’t load-bear on the task.** Test each section by removing it
   and asking whether any headline conclusion, recommendation, or actionable step
   changes. If nothing material moves, the section is extraneous and belongs in a
   separate background document, a marked appendix, or not at all.

3. **Mark digressions as digressions.** When a section is included for completeness but
   is not load-bearing, signal it with a `Background`, `Related work`, `Aside`, or
   `Historical note` header so the reader can skip without losing the main thread.

4. **Each source passes the one-sentence test.** For every cited source, the writer
   should be able to say in one sentence: *this source supports claim X, which bears on
   purpose Y*. Sources that fail this test are either misused or unnecessary.

5. **Don’t pad bibliographies for performative-rigor reasons.** A long reference list is
   not evidence of thoroughness; it is evidence of thoroughness only when each entry
   earns its place. Cite the sources that load-bear; cut the rest.

## Judgment Dimensions

Calibration matches claim strength to evidence strength.
Fairness engages opposing positions at proportional evidentiary depth.
Robustness tests whether key claims survive alternative interpretations of the same
evidence. All three fail when a directional view crowds out the underlying evidence.

### J1. Calibration

*Description:* The strength of a claim must match the strength of the underlying
evidence in both directions.
Overconfidence (strong claims on thin evidence) and underconfidence (hedging on solid
evidence) both fail calibration.

**Rules:**

1. **Anchor probability claims in empirical base rates.** When asserting “P(X) = N%,”
   cite the empirical base rate for X (in this dataset, in this window, in similar
   setups). If you can’t cite a base rate, mark the probability as “subjective; no
   historical anchor.”

2. **Bayesian shrinkage from small samples should be explicit.** “7/7 in a small sample,
   shrunk to 85%” is more honest than asserting “90%.” Small-sample base rates push
   toward the prior.

3. **Show the work for triangulated estimates.** “5-15% triangulated estimate” is
   incomplete without the triangulation method.
   State what data points contribute.
   Ranges are stronger than point estimates when the data supports a range, weaker when
   they’re hedging on solid evidence.

4. **Pre-event committed priors are the calibration discipline.** When the work involves
   forecasting an event, write the prior *before* the research begins.
   The delta between pre-research and post-research priors quantifies what the research
   added (or confirmed).
   Without this loop, forecasts can’t be calibrated retrospectively.

5. **Scenario probabilities must sum to 100%.** If three scenarios are stated at
   30/50/20, they sum to 100. If they sum to 110% or 90%, recheck.

6. **Confidence without cowardice.** Hedging on strong evidence is a calibration
   failure, symmetric to overconfidence on weak evidence.
   “Possibly,” “might,” and “arguably” are out of place when the evidence supports a
   direct claim; reserve them for genuine uncertainty.
   State what you can defend, anchored in the same base rates and sample sizes that
   discipline overconfident claims; honest force on strong evidence is part of
   calibration, not a violation of it.

### J2. Fairness

*Description:* Opposing positions (a case for and a case against, or any oppositional
framings) are argued at depth proportional to their plausibility, materiality, and
strength. Asymmetric evidentiary weight is a fairness failure when the asymmetry is
hidden; it is not a failure when one position is genuinely weaker and the document
explains why.

Fairness is not equal airtime: it is proportional representation of material positions
according to evidence, relevance, stakes, and the document’s purpose.
The failure mode at one extreme is straw-manning (under-representing a position someone
actually holds); the failure mode at the other is false balance (treating a weak
position as comparable to a strong one without saying so).

**Rules:**

1. **Engage opposing positions at proportional evidentiary depth.** If the case for has
   three named primitives plus numerical comparisons, the case against deserves
   comparable depth (three named mechanisms plus numerical thresholds) unless the
   evidence is genuinely asymmetric.
   When one side receives much less depth, the document explains why (low plausibility,
   low materiality, well-trodden ground).
   Silent asymmetry is the failure; declared asymmetry is not.

2. **Acknowledge inverses of one-sided framings.** “30-40% of the speedup comes from the
   new cache” implicitly says 60-70% comes from elsewhere.
   Flag the inverse explicitly.

3. **Risk inventories cover the relevant classes.** Risks of different kinds (technical,
   competitive, macro, regulatory, precedent-based) should each be considered where the
   domain calls for them.
   A risk inventory weighted heavily toward one class is an incomplete map of the risk
   space.

4. **Audit “counterintuitive” sections for confirmation bias.** When a section asks for
   “non-obvious” findings, the natural pull is toward findings that confirm a prior the
   author already holds.
   Count how many findings favor the central claim, how many challenge it, and how many
   are neutral.

5. **Falsification conditions for each central claim.** “If X happens, the claim fails”
   is a falsification condition.
   “If Y happens, the claim holds” is a confirmation condition.
   Don’t substitute one for the other.

### J3. Robustness

*Description:* Key claims survive plausible alternative interpretations of the same
evidence. Even granting the evidence and the chosen framing, would a *different
reasonable lens on the same evidence* change the key claim?

A well-calibrated, fairly argued claim can still be brittle if it depends on a single
interpretive frame that a competent reader would dispute.

**Rules:**

1. **State the interpretive lens.** When the evidence admits multiple reasonable
   readings, name the lens being used.
   “Reading this slowdown as a memory-pressure signal” is more honest than treating the
   memory interpretation as the obvious read.

2. **Test the claim against the most threatening alternative interpretation.** The
   strongest alternative reading is not a strawman; it is the one a competent skeptic
   would raise. Run the same evidence through it and report whether the claim holds.

3. **Flag interpretation-dependent claims.** When a claim holds under one reasonable
   lens but flips under another, that is a finding, not a footnote.
   Lead with it; do not elide it.

4. **Sensitivity to the interpretive frame should match sensitivity to the data.** If a
   10% data shift would not change the claim but a different reasonable lens would, the
   claim is brittle to interpretation.
   State that explicitly.

5. **Distinguish Robustness from Fairness.** Fairness (J2) engages opposing positions at
   proportional evidentiary depth.
   Robustness asks whether the chosen reading survives a different reading of the same
   evidence the opposing cases share.
   The two are complementary, not redundant.

## Common Pitfalls

1. **Cosmetic vs substantive scrutiny.** Reviewing for banned words is easy; auditing
   arithmetic, probability calibration, and evidence chains requires actual re-checking.
   Self-evals that focus on cosmetic dimensions miss substantive failures.

2. **Anchoring on a source document.** When authoring against an existing reference, the
   natural pull is to summarize the source rather than weigh each fact against primary
   evidence. Surface this when it applies; it shifts factuality and reasoning scores.

3. **Compliance pressure crowding out self-regulation.** When a document has many
   structural requirements, the agent’s cognitive budget tilts toward compliance.
   Move what can be deterministic out of the regulation budget: lint passes, schema
   validators, two-pass authoring.

4. **Probability inflation.** Subjective probabilities tend to be stated with more
   precision than the underlying calibration supports.
   Ranges are more honest than point estimates without anchors.

5. **Confirmation conditions labelled as falsification.** “If X happens, the claim
   holds” is a confirmation condition; the falsification condition is “if not-X happens,
   the claim fails.” The two are not interchangeable.

## Pre-Publish Self-Audit

The dimension sections above are the full checklist.
For a tight self-check before publishing, walk the six groups in order and ask:

- **Purpose (P1-P4):** Is the task declared and the main answer recoverable from a skim?
  Scope explicit and matched by the body; relevant areas covered (Breadth); key sections
  developed at the depth the stakes require (Depth)?
- **Expression (E1-E3):** Any banned-register hit, vague magnitude word,
  meta-commentary, parallel-structure padding?
  Each paragraph has one job?
- **Form (F1-F3):** Heading hierarchy logical and sections arranged for the task?
  Style consistent (dialect, casing, parallel lists)?
  Markup valid and footer/frontmatter in place?
- **Reasoning (R1-R4):** Observation, judgment, interpretation, and implication worked
  through in order, each higher rung supported by the prior?
  Mechanisms named where causation is asserted?
  Domain entities referred to by proper name; quantitative precision matches
  measurement? Load-bearing chains the minimum sufficient sound argument?
- **Grounding (G1-G3):** Every quantitative claim source-traceable to a specific
  citation (with stakes-appropriate strictness)?
  Cited sources support the claim at the asserted strength?
  Sources and sections bear on the document’s purpose?
- **Judgment (J1-J3):** Probability claims anchored in base rates?
  Opposing positions engaged at proportional depth, with any asymmetry declared?
  Key claims tested against the strongest alternative interpretive lens?

If any rule is unclear in the moment, return to its dimension section above.

## Two-Pass Authoring as a Practice

When the document is high-stakes, two-pass authoring is a reliable lever:

1. **Substance pass.** Author writes the claims, structures the reasoning, stages the
   evidence. Focus on facts and reasoning.

2. **Quality-audit pass.** Different agent, fresh context, or same author after a break.
   Audit against these dimensions.
   Catch arithmetic, calibration, citation specificity, balanced treatment, and register
   issues.

Single-pass authoring trying to do both at once produces predictable failures:
arithmetic gets sloppy, citations get vague, language drifts toward register that
overstates the evidence.

For higher-stakes audits, four narrower passes outperform one broad pass; each pass has
a different cognitive load and a different tool stack:

1. **Lint pass.** Headings, links, banned-register words, vague magnitude words, missing
   captions, table shape, frontmatter schema, footer placement.
   Largely deterministic; can be tool-driven.
2. **Claim audit.** Every quantitative claim against its cited source; calculations
   redone; rounding/aggregation/derivation disclosed.
3. **Reasoning audit.** Assumptions surfaced; mechanisms named; counter-evidence
   engaged; robustness against alternative lenses.
4. **Purpose audit.** Output shape vs task shape; scope declared and matched; main
   answer recoverable from a skim; reader task completion.

The pass separation is **required** for high-stakes documents (audits, decision memos,
external research, security advisories), **recommended** for standard internal docs, and
**optional** for low-stakes drafts and operational notes where a single review pass fits
the risk. Where the discipline applies, do not combine passes; running them in parallel
by the same agent in the same context loses the cognitive separation that the four-pass
structure depends on.

## Related Docs

- ../README.md (`pprose about`): how the practical-prose layers fit together.
- `pprose guidelines practical-prose-principles`: the seven principles
  these rules derive from.
- `pprose guidelines practical-prose-rubric`: descriptive 0-5 scoring
  anchors for the same 20 dimensions.
- `pprose guidelines practical-prose-bibliography`: full citations for
  works referenced in these guidelines, with publication details and stable URLs.
- `pprose guidelines practical-prose-metrics`: quantitative metrics and
  recommended frontmatter schema that operationalize these rules.
- `pprose guidelines common-doc-guidelines`: general style, organization, and
  formatting (the substrate these guidelines extend).
- `pprose guidelines ai-prose-corrections`: the binding `conventions.md`-style
  extension that catalogs LLM-register tells and their corrections.
- Domain-specific `conventions.md` files extend these guidelines with domain-specific
  banned-word lists, confidence-tag conventions, and citation-format requirements.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
