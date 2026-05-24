---
title: Practical Prose Rubric
description: Descriptive 1-5 rubric for scoring a practical writing artifact across the 20 dimensions defined in practical-prose-guidelines.md, with NA and ERR sentinels for dimensions outside the alignment scope.
date: 2026-05-23
status: active
---
# Practical Prose Rubric

Version: v0.1 (rubric: `pp20v2`, last update 2026-05-24)\
Joshua Levy (github.com/jlevy)

A descriptive 1-5 rubric for assessing practical writing artifacts (articles, blog
posts, research reports, design docs, specs, technical papers, decision memos) across
the 20 dimensions defined in
[practical-prose-guidelines.md](practical-prose-guidelines.md).

The rubric is **descriptive** (what a score looks like); the guidelines are
**prescriptive** (what to write).
Use the guidelines to author; use the rubric to assess.

The doc-type list above is a descriptive framing of what this rubric applies to.
The eval tooling has a separate, narrower tag (`artifact.scope_class`, set via
`--scope-class` on `eval_report.py from-metrics`) for density-threshold flagging:
`status`, `memo`, `brief`, `deep_research`, `design_doc`. See
[practical-prose-eval-single.runbook.md](../runbooks/practical-prose-eval-single.runbook.md)
for the scope-class table and when to set each value.

## Alignment with the guidelines

The rubric and [practical-prose-guidelines.md](practical-prose-guidelines.md) define the
same 20 dimensions in the same six groups, using the same names and section numbers
(P1-J3). They are designed as a tight bidirectional map:

- A document scoring **5** on a dimension has no material unaddressed rule violations
  for the artifact’s purpose, audience, genre, and risk level.
  Minor justified deviations are allowed when documented and reader-serving (see
  *Justified Deviations* below).
  “Follow every rule exactly” is the source aspiration; “no material unaddressed
  violations” is the scoring test that keeps the rubric workable on real documents.
- Any clear material rule violation drops the score below 5. The score-4 anchor (one or
  two minor isolated slips) is where most “almost-5” documents land; minor defects do
  not collapse a dimension to 1.
- **5** = no material unaddressed rule violations for the artifact’s purpose, audience,
  genre, and risk level.
- **4** = one or two minor rule slips, isolated.
- **3** = multiple slips, or one severe slip that affects the document’s central claims.
- **2** = frequent slips on key claims.
- **1** = the dimension fails on most relevant content.
- **NA** = not applicable.
  The dimension does not engage with this artifact at all.
  For example, Calibration on a document that makes no probability or forecast claims.
- **ERR** = the scorer could not assess this dimension.
  A *process* failure, never a quality verdict on the document.
  Use when the rubric cannot be applied for a procedural reason (the artifact is
  truncated, an upstream tool failed, the assigned model refused, etc.). See the
  decision tree below.

Numeric scores are always 1-5: there is no 0. One meaning per value — numeric scores are
*quality*, ERR is *process*, NA is *out of scope* — keeps the scoring prompt, the
per-dim anchors, and the rollup all aligned, and stops a single 0 from being read as
both a low quality verdict and a silent excluded-from-mean sentinel.
As a side benefit, numeric scores are always truthy, so `if score: ...` cannot
accidentally treat an unscored dimension as a quality-zero swing.

When you score below 5, cite the specific guideline rule that was missed in the
parenthetical reason.
If you cannot tie a low score to a missed rule, either the rubric is missing test
coverage or the score is wrong.

**Reader outcome governs local rule compliance.** The rubric checks whether the document
follows the guidelines, but the guidelines exist to help readers understand, decide, do,
verify, or maintain something, not to be followed for their own sake.
A document that scores high on every dimension but fails its actual reader is not a good
document. When local rule compliance and reader outcome conflict, reader outcome wins,
and the deviation is documented (see *Justified deviations* below).
The rubric is a strong instrument for catching avoidable defects; it is not a substitute
for asking whether the document worked.

### Decision tree: NA, ERR, or 1-5?

This decision tree is binding.
Apply the questions in order and stop at the first “yes”.
The same artifact under the same rubric must reach the same answer; if two reviewers
reach different answers, one of them has skipped a step.

1. **Does the artifact engage the dimension’s subject matter at all?** Engagement means
   the artifact contains content the dimension is designed to score: verifiable claims
   (Verifiability), cited sources (Factuality), inferential reasoning (Discipline),
   probability claims (Calibration), oppositional framings (Fairness), interpretive
   judgments (Robustness), and so on.
   - **No.** → consult the per-dim NA anchor.
     If the per-dim anchor’s NA condition fits, score **NA**. If the per-dim anchor
     instead says the artifact’s task class was *expected* to engage and didn’t (e.g., a
     decision memo with no fairness content), score per the **1-anchor** of that
     dimension and cite the missing-coverage rule.
     **Do not invent a “should-have” judgment that the per-dim NA anchor does not
     authorize.** Reasons must quote or paraphrase the per-dim NA anchor when scoring
     NA.
   - **Yes.** → continue.

2. **Apply the 1-5 anchors for the dimension** below.
   For any score 1-4, cite at least one guideline rule the document missed.
   - The “attempted but materially missing” case (e.g., sources cited but unreachable;
     fewer than three sentences of reasoning; declared intent without content) is a
     score of **1** with a citation of the missed rule.
     It is not ERR: the document engaged the dimension and the rubric’s 1-anchor fits.

3. **Score ERR only if the scorer cannot apply the rubric for a procedural reason.** The
   artifact is truncated, an upstream tool failed, the assigned model refused or
   returned malformed output, the dimension was added after the eval was run, and so on.
   Reasons must name the procedural cause; never use ERR to register a quality
   complaint. Re-running the eval is the right fix; if the document is genuinely beyond
   the rubric, the answer is NA, not ERR.

**Tiebreaks:**

- **NA and 5 are mutually exclusive.** A dimension cannot score both NA and 5 on the
  same artifact. NA means the artifact does not engage the dimension; 5 means the
  artifact engages it and satisfies the rubric.
  If the artifact contains no content the per-dim 1-5 anchors describe, it is NA, not
  5\. ("No problems found because there’s nothing to check" → NA. “No problems found
  because everything checks out” → 5.)
- **NA and ERR are not interchangeable.** NA is a verdict *about the document* (it does
  not engage this dimension); ERR is a verdict *about the eval process* (the scorer
  could not assess). Prefer NA when in doubt; ERR is rare and is a signal to re-run the
  eval rather than to publish the result.
- **NA vs 1-4 is decided by the per-dim NA anchor, not by the reviewer’s intuition.**
  Each per-dim NA anchor specifies the conditions under which “should have but didn’t”
  still warrants NA vs a low score.
  Apply the per-dim anchor, do not improvise.

NA must be reserved for dimensions the artifact’s task genuinely does not require.
When aggregating, both NA and ERR dimensions are excluded from any mean (counted
separately in `na_dimensions` and `err_dimensions`) rather than treated as zero, so that
lightweight artifacts are not penalized for not needing every dimension and unscored
dimensions do not silently distort the rollup.

### Cross-dimension cascades

A few dimensions are defined in terms of another (the *prereq*): you can’t score the
dependent dimension without scoring the prereq first.
The cascade rule is uniform — NA carries NA, ERR carries ERR, and 1-5 carries 1-5:

| Prereq → Dependent | NA cascade | ERR cascade | 1-5 prereq |
| --- | --- | --- | --- |
| Verifiability → Factuality | Factuality NA | Factuality ERR | Factuality scored 1-5 on the same claim set Verifiability scored |
| Suitability → Relevance | Relevance NA | Relevance ERR | Relevance scored 1-5 against the stated purpose |
| Soundness → Parsimony | Parsimony NA | Parsimony ERR | Parsimony scored 1-5 on whatever sound chains remain |

Read this as: when a prereq lands on a sentinel (NA or ERR), the dependent dimension
inherits the same sentinel.
A *low* prereq score (1 or 2) is not a cascade trigger — the dependent dimension is
still scored on its own anchors, and the reason may cite the upstream weakness.
Cascades exist because the dependent dimension’s question literally cannot be asked
without its prereq’s basis (no verifiable claims → nothing to fact-check; no stated
purpose → no target for relevance; no sound chain → no chain to be parsimonious about).

## Justified Deviations

A deviation from a guideline rule is **justified** when following the rule would hurt
the intended reader’s ability to understand, decide, do, verify, or maintain the work,
and the deviation is documented so any reviewer can see the trade-off.
Document three things, in the document itself or in adjacent review notes:

1. **The rule set aside.** Cite the guideline section and rule number.
2. **The reader outcome served.** What can the reader now do that rule-following would
   have made harder?
3. **The risk introduced.** What is given up by accepting the deviation (clarity,
   inspectability, consistency, future-proofing)?

A justified, documented deviation should not lower the score for that dimension.
An undocumented deviation should be scored as an ordinary rule miss.

The burden is on the writer or reviewer to argue that the deviation serves the reader.
This rule keeps the rubric from drifting into checklist literalism; most rule violations
are not justified.

## Dimensions

| # | Group | Dimension | Question |
| ---: | --- | --- | --- |
| 1 | Purpose | Suitability | Does the document give the reader what they need, in the form the task requires? |
| 2 |  | Scope | Is the scope stated, and does it fit the actual scope of the work? |
| 3 |  | Breadth | Are the relevant areas within scope covered? |
| 4 |  | Depth | Are the important areas developed enough? |
| 5 | Expression | Clarity | Does the writing read well? |
| 6 |  | Coherence | Do the ideas progress smoothly? |
| 7 |  | Concision | Does every section earn its place? |
| 8 | Form | Organization | Are sections, headings, sequence, tables, figures, links, and cross-references arranged for navigation? |
| 9 |  | Consistency | Does the document follow the chosen style guide or house style consistently? |
| 10 |  | Formatting | Is the document visually and syntactically clean in its medium? |
| 11 | Grounding | Verifiability | Are claims traceable to sources or calculations? |
| 12 |  | Factuality | Do cited sources support the claims as asserted? |
| 13 |  | Relevance | Do sources, citations, and reasoning chains bear on the document’s stated purpose? |
| 14 | Reasoning | Discipline | Are observation, judgment, interpretation, and implication worked through in order, with each higher rung supported by the prior? |
| 15 |  | Soundness | Do claims follow from evidence through valid mechanisms? |
| 16 |  | Precision | Are claims and terms specified at the right granularity? |
| 17 |  | Parsimony | Is each load-bearing reasoning chain the cleanest, simplest sound argument possible for its conclusion? |
| 18 | Judgment | Calibration | Does claim strength match evidence strength? |
| 19 |  | Fairness | Are opposing positions argued at proportional evidentiary depth? |
| 20 |  | Robustness | Do key claims survive plausible alternative interpretations? |

## How to score

For each dimension, assign either an integer 1-5, `NA`, or `ERR`, plus a brief
parenthetical reason.

- Score the dimensions independently.
  Do not aggregate to a single number unless the use case calls for it (and then state
  the weighting).
- If two adjacent anchors both fit, pick the lower score and name the defect that keeps
  the document from the higher anchor.
  Use **3** only when strengths and failures are materially mixed across the dimension
  (some sections satisfy a high anchor, others fail a low one), not for any “between”
  case.
- For any score below 5, cite at least one specific guideline rule the document missed.
- For any score-5, no violation should be cite-able for that dimension.

### How the strict alignment rule interacts with the score-4 anchor

The strict rule says: any single clear violation of a guideline rule drops the score
*below* 5. That rule is essential to the rubric’s bidirectional map with the guidelines
and is not negotiable.
It does **not** say minor slips collapse the score to
1. The score-4 anchor catches exactly the “one or two minor isolated slips” case;
   multiple slips or one severe slip that affects the document’s central claims push to
   3 or lower. Read the strict rule and the score-4 anchor together: the strict rule is
   the ceiling, the anchors below describe what the document actually looks like.

### Primary vs secondary dimension for overlapping defects

Some defects can be cited under more than one dimension.
To keep reports comparable between reviewers, cite under the **primary** dimension; a
brief cross-reference in the reason note is enough for the secondary dimension.
Suggested primary assignments:

| Defect | Primary | Secondary |
| --- | --- | --- |
| Vague language in ordinary prose ("very," “quickly”) | E1 Clarity | — |
| Vague magnitude in a scoped factual claim ("rapid growth") | P4 Depth | E1 Clarity |
| Vague countable / category name where specific term exists ("the company") | R3 Precision | E1 Clarity |
| Trite phrasing or banned-register hit | E1 Clarity | — |
| Canonicality declaration or word-choice / naming justification ("this is the canonical X"; “we use the term Y because…”) | E1 Clarity | E3 Concision |
| Replacement-history narration in a non-history genre ("previously named X"; “under the new layout”) | E3 Concision | E1 Clarity |
| Generic templated heading as sole section signal ("Overview," “Background,” “Notes”) | F1 Organization | E1 Clarity |
| Heading-level skip, table that should be prose, broken link | F1 Organization | — |
| Inconsistent dialect, casing, or parallel-list syntax | F2 Consistency | E1 Clarity |
| Spaced em-dash overuse (" — “ instead of ”—") | F2 Consistency | E1 Clarity |
| Malformed Markdown table, broken footnote anchor, misplaced footer | F3 Formatting | F1 Organization |
| Duplicated table / list content across sections | E3 Concision | F1 Organization |
| Undeclared or drifting scope on a multi-topic document | P2 Scope | P3 Breadth |
| Missing case class within declared scope (e.g., risk type omitted) | P3 Breadth | J2 Fairness |
| Thin development of a section the document’s purpose depends on | P4 Depth | P1 Suitability |
| Missing inline citation for a quantitative claim | G1 Verifiability | F3 Formatting |
| Number in prose doesn’t match source (silent rounding) | G2 Factuality | G1 Verifiability |
| Cited source doesn’t support the claim as asserted | G2 Factuality | G1 Verifiability |
| Mixed observation and interpretation in one sentence | R1 Discipline | R2 Soundness |
| Probability claim without base-rate anchor | J1 Calibration | R2 Soundness |
| One-sided argument with no counter-evidence engaged | J2 Fairness | J1 Calibration |
| Key claim brittle under a different reasonable interpretive lens | J3 Robustness | J2 Fairness |

### Output format

`SCORE (REASON)`, matching the regex `(NA|ERR|[1-5]) \(.*?\)`. Cite line numbers,
section names, or quoted phrases in the reason where relevant.
Examples:

```
4 (Clear, correct prose throughout; one paragraph at L412-418 has trite phrasing,
"the agentic thesis fully crystallizes", and could be tightened.)

3 (Mix of [VERIFIED] tags with primary sources and unverifiable claims around §1.10
competitive landscape; Vercel CEO benchmark quote at L820 has no tweet ID;
W3Techs market-share at L815 has no URL.)

5 (Bull / base / bear cases at §2.8 each have 3 named primitives and numerical thresholds;
risk register at §2.10 spans 5 classes; opposing positions argued at proportional
depth.)

NA (No probability, forecast, confidence, or uncertainty claims are made; the task is a
file-organization audit that does not call for calibration.)
```

## Score anchors by dimension

### Purpose

#### P1. Suitability

Does the document give the reader what they need, in the form the task requires?
A document can be clear, factual, and balanced and still fail Suitability if the reader
cannot extract the needed output, if the purpose was not named, or if the output shape
does not fit the task (a decision memo with no recommendation, an audit without
findings).

- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing or no task statable.
- **1:** Task implicit and undeclared; reader cannot tell what the document is for.
  Output shape does not match task shape.
- **2:** Task gestured at but not stated; the headline answer or instruction is buried
  so deeply that a skim does not surface it.
- **3:** Task stated, output recoverable with effort.
  Some tangential sections remain.
- **4:** Score-5 mostly satisfied with one or two minor slips: task stated but output
  recoverable only by reading the full body, or one section that doesn’t serve the task.
- **5:** The document names the question, decision, workflow, plan, or audience need it
  serves. The main answer is recoverable from a skim of intro plus section headings.
  Tangential sections are folded, moved to an appendix, or dropped.
  Output shape matches task shape (decision memo → recommendation, audit → findings,
  spec → milestones). When partially answered, open questions, deferrals, or blockers are
  named explicitly.

#### P2. Scope

Is the scope of the document stated, and does the declared scope match the actual scope
of the work? Scope is upstream of P3 Breadth and P4 Depth: a document with no declared
scope cannot be evaluated for whether it covers everything relevant.

- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing.
- **1:** Scope undeclared throughout; reader cannot tell what is in or out of scope.
  Body drifts across multiple topics with no boundary stated.
- **2:** Scope gestured at but vague (broad headers, no concrete boundary), and the body
  drifts beyond what the opening implies.
- **3:** Scope stated, but the body drifts into adjacent topics without flagging the
  drift, or the declared scope is broader than what the body actually covers.
- **4:** Score-5 mostly satisfied with one or two minor slips: one short tangent that
  falls outside the declared scope and is not flagged, or a scope statement that is
  precise but buried below the lede.
- **5:** Scope explicitly declared at the opening (one system, time window, workflow, or
  decision). Declared scope matches the body throughout.
  Out-of-scope questions surfaced during the work are named as out-of-scope and either
  deferred explicitly or absorbed via an updated scope statement.

#### P3. Breadth

Are the relevant areas within the declared scope covered?
Breadth is the *what is covered* question: relevant case classes, prior work, and
standard sources are present within scope.
The *how thoroughly* question is scored under P4 Depth.

- **NA:** Not applicable.
  The document is a single-fact note (a one-line status, a numeric reading) where there
  is no class structure to cover.
- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing or scope undeclared (score the latter under P2).
- **1:** Major case classes within scope are absent (risk inventory limited to a single
  class; no prior-work coverage; obvious affected areas omitted).
- **2:** Notable missing classes.
  One or two relevant areas within scope are absent and not flagged as deferred.
- **3:** Workable breadth.
  Most relevant case classes covered; one or two minor classes missing without an
  explanation.
- **4:** Score-5 mostly satisfied with one or two minor slips: one case class missing
  from a risk inventory, or one obvious precedent uncited.
- **5:** All relevant case classes within scope are present.
  Risk inventories span the classes the domain calls for.
  Relevant prior work and standard sources cited.
  Out-of-scope omissions are flagged as such.

#### P4. Depth

Are the important parts of the document developed to the level of detail, specificity,
evidence, and explanation the task requires?
Section depth matches section importance.

- **NA:** Not applicable.
  The document is a pure index, table of contents, or pointer-only artifact where depth
  is not the relevant question.
- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing or fragmentary.
- **1:** Key sections thin.
  Vague magnitude words ("rapid," “large”) used without quantification throughout.
  Endpoints cited where the full series carries the information.
- **2:** Notable depth gaps on key sections.
  Counts cited without names; key claims supported by single endpoints rather than
  series; one or two tangential sections deeper than the central one.
- **3:** Workable depth.
  Most magnitude words quantified; some endpoints replaced with full series; section
  depth roughly tracks importance.
- **4:** Score-5 mostly satisfied with one or two minor slips: one tangential section
  with more depth than a key section, or one count without named instances.
- **5:** Vague magnitude words quantified or removed.
  Endpoints replaced with full series where trajectory matters.
  Counts paired with named instances where space permits.
  Section depth matches section importance.
  Key claims developed at the depth the stakes require.

### Expression

#### E1. Clarity

Sentence-level readability: spelling, grammar, register, word choice.
Errors covered by spell-checkers, Grammarly, Vale, and the language-use parts of AP /
CMS. Concision is scored separately under E3; copyediting consistency (dialect,
parallel-list syntax, citation style) is scored under F2 Consistency; markup validity is
scored under F3 Formatting.

- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing or fragmentary.
- **1:** Numerous spelling, punctuation, grammatical errors; sentences hard to follow.
- **2:** Errors but understandable.
- **3:** Typical business-email quality; few errors; may contain a few typos.
- **4:** Clear, correct language with flaws: trite phrases, gratuitous big words,
  occasional banned-register hits, parallel-structure padding ("It’s not X, it’s Y"
  without a real contrast), or sentences that are unnecessarily dense.
- **5:** Publication-ready grammar and clarity, with no material defects.
  Words chosen for precision; banned-register words (the canonical common-doc-guidelines
  §4.2 list) and parallel-structure padding absent or earned (per E1 rules 4 and 5); no
  pedantic, pedagogical, or self-referential prose: no canonicality declarations,
  word-choice justifications, or reading-order instructions (per rule 6). Suitable for
  high editorial standard publication; minor justified deviations are acceptable when
  documented and reader-serving.

#### E2. Coherence

Prose-level flow of ideas: paragraph cohesion, transitions, whether ideas progress
smoothly sentence to sentence.
Does not cover logical coherence (R2 Soundness) or arrangement of sections and visual
elements (F1 Organization).

- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing or fewer than 3 sentences.
- **1:** Incoherent; no clear topic or thread.
- **2:** Weak coherence or incomplete draft.
- **3:** Adequate; generally possible to follow.
- **4:** Strong coherence with clear gaps: a few stub transitions, paragraphs that mix
  observation and recommendation, one or two ideas that arrive without setup.
- **5:** Seamless prose flow.
  Each paragraph has one job; first sentences preview the job so a skim of openers
  conveys the spine; transitions bridge cleanly between paragraphs and sections; the
  document progresses without backtracking.

#### E3. Concision

The writing carries only the content the task requires.
Padding, repetition, and decorative content fail concision even when each sentence is
clear.

- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing.
- **1:** Heavy padding; multiple paragraphs say the same thing; tables with stub data;
  sections that don’t serve the task.
- **2:** Notable redundancy; some sections add little marginal information.
- **3:** Some redundancy; a couple of sections could be tighter.
- **4:** Mostly tight; one or two paragraphs could be cut without loss of information,
  or one stray replacement-history passage in a non-history genre.
- **5:** Every section, paragraph, and sentence earns its place.
  Cuts would lose information about the subject.
  Frontmatter carries metadata only; visual elements appear only where their shape fits
  the data (though *whether* their shape fits is scored under F1 Organization).
  No replacement history outside genres that require it (per E3 rule 5): the document
  describes the present state, not what it replaced.

### Form

Arrangement, style discipline, and markup: the document as a structured artifact rather
than as prose. Distinct from Expression (sentence- and paragraph-level language), these
three dimensions descend from the Maintainable principle — they govern how a reader
navigates and how the document survives editing.

#### F1. Organization

Sections, headings, sequence, tables, figures, lists, links, and cross-references:
arrangement of the document.
Visual elements are not required (a tight prose document can score 5), but when present
they should be arranged well.
Markup validity is scored under F3 Formatting; style consistency is scored under F2.

- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing or fragmentary.
- **1:** No discernible organization.
  Flat wall of text or chaotic heading hierarchy; sections in random order; tables,
  figures, or links broken, malformed, or misplaced.
- **2:** Some organization but inconsistent.
  Heading levels skip (h1 → h3); tables included that should be prose; figures with no
  captions; sections not arranged for the task (recommendation buried in a memo).
- **3:** Workable organization.
  Sections grouped sensibly and roughly in task-shape order; tables and figures where
  they help; minor issues in hierarchy, captioning, or placement.
- **4:** Score-5 mostly satisfied with one or two minor slips: a table that should be
  prose, a figure missing a caption, a link to a non-stable URL, a cross-reference that
  doesn’t name what it points to.
- **5:** Heading hierarchy logically nested with no skipped levels.
  Sections sized appropriately for their content and arranged in the order the task
  requires. Headings cleave to the subject (per F1 rule 9): no generic templated headings
  ("Overview," “Background,” “Notes,” “Details”) standing alone as the only signal of
  section contents. Every table earns its tabular shape (parallel rows with a fixed
  schema) and is placed near its referencing prose; every figure has a caption
  explaining what it shows; links target stable anchors and resolve; cross-references
  name what they point to ("see §2.8 (named cruxes)" over “see §2.8”); visual elements
  deployed where they help, absent where prose is clearer.

#### F2. Consistency

Does the document follow the chosen style guide or house style consistently across
syntax, terminology, capitalization, punctuation, spelling, dates, numbers, units,
citations, and register?
Distinct from E1 Clarity (sentence-level readability) and F3 Formatting (markup
validity).

- **NA:** Not applicable.
  The document is too short or fragmentary for a style guide to apply (a single line, a
  log entry).
- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing or fragmentary.
- **1:** Style chaotic.
  Multiple dialects mixed; capitalization inconsistent across acronyms and proper nouns;
  lists shift between noun-phrase and imperative forms; register swings between formal
  and casual without reason.
- **2:** Frequent inconsistency on key style points.
  Date formats inconsistent within a section; acronym casing varies; citation styles
  mixed.
- **3:** Workable consistency.
  Dialect and casing mostly consistent; one or two parallel-list violations; one or two
  register slips.
- **4:** Score-5 mostly satisfied with one or two minor slips: one acronym styled
  inconsistently, or one citation in a different style.
- **5:** Spelling dialect, capitalization, punctuation, hyphenation, and number/date
  formats consistent throughout.
  Product names, acronyms, technical terms styled consistently.
  Lists and headings use parallel syntax.
  Citation style consistent.
  Register holds. Domain-specific banned words and house-style conventions followed.
  Em dashes used sparingly and in American style (no surrounding spaces), per F2 rule 7;
  spaced em-dash overuse is absent.

#### F3. Formatting

Is the document’s markup and visual presentation clean, valid, and compatible with the
chosen medium? Most rules under this dimension are deterministically lintable.
Distinct from F1 Organization (arrangement) and F2 Consistency (editorial polish).

- **NA:** Not applicable.
  The document is plain text with no markup, or a format where formatting concerns are
  outside scope.
- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing or fragmentary.
- **1:** Markup broken throughout.
  Tables unrendered; code fences unclosed; frontmatter malformed; links non-functional.
- **2:** Several markup defects.
  One or two unrendered tables; mixed indentation; trailing whitespace; missing footer
  or frontmatter where required.
- **3:** Mostly clean markup.
  One or two minor defects; emphasis conventions inconsistent in a few places.
- **4:** Score-5 mostly satisfied with one or two minor slips: a single malformed
  footnote anchor, one inconsistent code-fence language tag, or whitespace drift in one
  section.
- **5:** Markdown / HTML / document markup renders correctly throughout.
  Lists, tables, code fences, block quotes, links, images, footnotes, and frontmatter
  are syntactically valid.
  Whitespace, indentation, and line breaks consistent.
  Emphasis formatting follows convention.
  Required headers, metadata, and footers present and correctly placed.
  No raw-source artifacts in the rendered output.

### Grounding

#### G1. Verifiability

Are claims traceable to specific sources, observations, calculations, or explicit
assumptions? A document scores high when a competent reader could check claims from what
the document provides, before any external lookup.
Verifiability is text-internal; Factuality (G2) is the source-aware check that the audit
would actually pass.
The strictness of the primary-source bar scales with stakes: research reports, audits,
and decision memos require primary sources for every quantitative claim; lightweight
operational notes only require sources for material claims.

- **NA:** Not applicable.
  The document makes no **verifiable assertions**; that is, no statements that are
  truth-apt and checkable in principle.
  A statement is truth-apt when a competent reader could in principle determine whether
  it is true by consulting sources, observations, or calculations.

  Statements that do **not** engage Verifiability (and therefore do not, by themselves,
  prevent NA):
  1. Definitions ("an X is a Y that does Z").
  2. Stated intent or aim ("this document aims to...").
  3. Performative declarations ("we adopt the following...").
  4. Self-referential or navigational content ("section 3 covers...").
  5. Hypothetical, normative, or imperative statements ("if X, then do Y"; “writers
     should...”).
  6. Aesthetic or evaluative judgments offered as opinion ("this approach is elegant").

  Statements that **do** engage Verifiability (and therefore preclude NA):
  1. Empirical assertions about the external world ("X happens more than Y").
  2. Quantitative claims with a stated or implied magnitude ("12% of...", “more
     than...”, “in greater volume than”).
  3. Historical or causal claims about events, entities, or mechanisms.
  4. Comparative judgments about external entities offered as fact rather than opinion
     ("X is faster than Y").
  5. Attributions to specific people, works, or institutions ("as noted by X").

  Rule: if the artifact contains **any** statement of the second kind, Verifiability is
  engaged and the score is 1-5, not NA. An artifact that *makes* such claims without
  sourcing them is **not NA**; it scores 1-4 per the anchors below.
  Reserve NA for artifacts whose entire content consists of statements of the first
  kind.

- **ERR:** Cannot assess (process failure; re-run the eval).
  Reserve for genuine procedural failures — the document is truncated mid-claim, an
  upstream tool failed, the assigned model refused to score this dimension.
  If the document makes verifiable assertions and simply omits sources, that is a
  quality verdict (score 1-4 with rule citations), not ERR.

- **1:** Material claims are vague enough that no source could confirm or refute them,
  *and* unsourced. Quantitative claims with no source pointers; confidence tags absent or
  used without sources.
  The document cannot be audited from what it provides.

- **2:** Claims have stated referents but specificity is poor (vague magnitude words
  like “rapid” or “many” attached to scoped factual claims; “the Q4 transcript” with no
  date or section). Derived facts assert without showing the calculation.

- **3:** Most quantitative claims have a primary source pointer, but several are vague
  enough that finding the exact passage takes work.
  Confidence tags used but not consistently paired with source pointers.

- **4:** Score-5 mostly satisfied with one or two minor slips: a single quantitative
  claim without a source, or one `[VERIFIED]` tag without naming what was verified.

- **5:** Every verifiable claim in the document is *easily verifiable*: stated
  specifically enough to be checkable, and traceable to evidence the reader can reach at
  appropriate effort for the document’s stakes.
  Quantitative and high- stakes claims have specific pointers (URL, document ID, page or
  section number, commit SHA). Lower-stakes material claims state their basis (a named
  primary observation, a clearly attributed source, or an inline derivation).
  Confidence tags pair with source pointers; derived facts show the calculation inline
  (`[DERIVED: 89.6 / 614.5 = 14.6%]`).

  Calibrated uncertainty does not lower the score.
  A claim explicitly marked as speculative, unverified, or estimated, with its basis
  named, is treated as satisfying the dimension because the document is being honest
  about what is known.
  The point is that the reader can tell the epistemic status of every claim, not that
  every claim is resolved.

  Note: Verifiability 5 measures the document’s *help* in checking claims, not whether
  the checks would pass; that is Factuality (G2).

#### G2. Factuality

Do the document’s verifiable claims hold up when checked against the world, at the
asserted strength, for the asserted entity, date, and scope?
**Verifiability (G1)** is text-internal: does the document let the reader audit?
**Factuality** is world-aware: does the audit pass?
Scoring Factuality requires the reviewer to attempt corroboration: by following the
document’s cited sources where present; by consulting authoritative external sources
where citations are absent; and by recording when a claim cannot be confirmed or refuted
from available evidence at appropriate effort.

**Truth means: the assertion strength matches the available evidence.** A claim asserted
as certain when the evidence is uncertain is a Factuality defect.
A claim asserted as speculative or hypothetical, *with the speculative status explicit
and the basis named*, is **factually correct** even if the underlying proposition cannot
be checked, because the document is telling the reader the truth about what is known.
Calibrated uncertainty is not a Factuality defect; uncalibrated certainty is.

A claim that cannot be corroborated and is *asserted as fact without hedging* is a
Factuality defect, not a “cannot-assess” exemption: the document has failed to match
assertion strength to evidence.
The score reflects this.
See J1 Calibration for the broader treatment of claim-strength matching.

**Reviewer access limits are a separate concern from document defects.** A claim may be
theoretically verifiable but unreachable in the current scoring context (a paywalled
article, a private dataset, a closed-source repo, or a primary source in a language the
reviewer cannot read).
In such cases, the reviewer should:

1. Note in the reason which specific claim(s) could not be corroborated, and the access
   limit that prevented it.
2. Distinguish *document failures* (the doc made an unhedged claim with no basis or
   unreachable evidence) from *reviewer limits* (the doc provided reasonable pointers,
   but the pointers happen to be inaccessible to this reviewer).
3. Score document failures per the anchors below.
   Treat reviewer limits as neutral on Factuality: if the document did its part (cited a
   primary source, stated the basis, or acknowledged the limit explicitly), the claim
   does not count against Factuality.
   The score reason names the access limit so a later reviewer with access can complete
   the audit.

The rubric’s Factuality score is about the document’s truth-discipline, not about the
reviewer’s reach. Mark claims that cannot be checked in this round; do not silently
penalize the document for them.

- **NA:** Not applicable.
  The document makes no verifiable assertions at all (see G1 Verifiability NA for the
  engagement test). Factuality engages on the same set of claims Verifiability engages
  on, so Factuality follows Verifiability’s NA verdict (see *Cross-dimension cascades*
  in the rubric front matter).

- **ERR:** Cannot assess (process failure; re-run the eval).
  Either the document attempts at least one verifiable assertion but the claim is
  fragmentary or truncated (a partial sentence, an unfinished paragraph, or a `[TODO]`
  marker) leaving no claim to corroborate, **or** Verifiability itself is ERR and the
  cascade applies (Factuality ERR follows Verifiability ERR). Rare.
  If the document’s claims are fully stated, score 1-5 even if corroboration is
  incomplete (per the rule above).

- **1:** Major claims are contradicted by reasonable corroboration: cited sources do not
  contain the cited content, or external lookup finds the claim is false.
  Hallucinated or invented sources, authors, or document IDs, or invented claims:
  anything that reads as a fact but is detached from a source or supporting logic (a
  fabricated statistic, an invented specific) counts here even when no source is cited.
  Multiple claims that the reviewer cannot corroborate or refute despite reasonable
  effort, with no acknowledgement in the document that they are uncorroborated.

- **2:** Several claims overstate, paraphrase past the source, or cannot be corroborated
  at the asserted strength.
  Numbers in prose don’t match cited sources without disclosure; entity, date, or scope
  mismatches between claim and source.

- **3:** Most claims are corroborated, but with notable strength mismatches, paraphrase
  drift, or one or two claims that the reviewer can neither confirm nor refute, without
  the document flagging them as uncorroborated.

- **4:** Score-5 mostly satisfied with one or two minor slips: one undisclosed rounding,
  one entity/date mismatch, or one claim flagged as uncorroborated without enough basis
  stated.

- **5:** Every verifiable claim is corroborated, ideally by a cited source the reviewer
  can reach, otherwise by authoritative external evidence accessible at appropriate
  effort. Numbers in prose match cited or corroborating sources, or disclose rounding,
  aggregation, unit conversion, or derivation explicitly.
  Entity, date, and scope of claims match the supporting evidence.
  No hallucinated or invented sources or claims: every reference resolves to a real
  artifact that contains the cited content, and no assertion reads as a fact while
  detached from a source or supporting logic.
  Where a claim cannot be corroborated from available evidence, the document
  acknowledges this explicitly (e.g., “we have not been able to verify this”) and states
  the basis on which the claim is made anyway.

#### G3. Relevance

Do sources, citations, and intermediate reasoning chains bear on the document’s stated
purpose? Relevance sits in **Grounding** alongside Verifiability (G1) and Factuality
(G2): Verifiability asks whether claims trace to sources; Factuality asks whether those
sources support the claims; Relevance asks whether the supported claims matter for the
document’s purpose.
A document can score 5 on Verifiability and Factuality and still fail
Relevance by anchoring its evidence to tangential material.

Relevance is distinct from P2 Scope (which declares the document’s boundary) and E3
Concision (which is prose-level economy): Relevance tests whether the content *inside*
the declared scope earns its place against the purpose, at the level of sources and
sections rather than words and paragraphs.

- **NA:** Not applicable.
  Either the document makes no inferential claims and cites no sources (pure reference
  data, raw measurements, a glossary, or a structured form — no audit trail to evaluate
  for relevance), **or** Suitability is NA and the cascade applies (Relevance NA follows
  Suitability NA; see *Cross-dimension cascades* in the rubric front matter).

- **ERR:** Cannot assess (process failure; re-run the eval).
  Either a procedural failure prevents scoring (truncated artifact, tool failure),
  **or** Suitability is ERR and the cascade applies (Relevance ERR follows Suitability
  ERR — without a known purpose, the relevance question has no target).
  A low Suitability score (1-2) is not an ERR trigger; in that case Relevance is still
  scored 1-5 against whatever purpose the document does state, and the reason may cite
  the upstream Suitability weakness.

- **1:** Half or more of the cited sources or reasoning chains are irrelevant to the
  document’s conclusions or purpose.
  Headline claims rest on tangential evidence, or major sections do work toward goals
  the document never declared.

- **2:** A significant fraction of cited sources or reasoning points are ancillary or
  extraneous to the purpose; load-bearing claims would survive cutting them.

- **3:** Workable; the headline claims rest on relevant evidence, but several sources or
  sections don’t fully earn their place against the purpose.
  A reader who skims to the recommendations does not pick up tangents, but a careful
  reader sees padding.

- **4:** Score-5 mostly satisfied with one or two minor slips: a few sources or notes
  are a bit of a stretch (cited for completeness, or surfacing as digressions) but
  remain loosely relevant.
  Background sections, when present, are signalled as background.

- **5:** Every cited source and every line of reasoning is relevant to the document’s
  purpose; nothing can be removed without lowering the quality of the work.
  Performative citations are absent.
  Digressions, where present, are explicitly marked so the reader can skip without
  losing the main thread.

### Reasoning

#### R1. Discipline

Climbing the ladder of inference rung by rung in order (observation → judgment →
interpretation → implication), with each higher rung supported by the rung below.
Implications rest on sound interpretations, which rest on sound judgments, which rest on
sound observations.
Each rung is named on its own terms; none is skipped, none is blended
into its neighbor. Sister of Soundness (R2): Soundness asks whether each step is itself
valid; Discipline asks whether the rungs are climbed in order and exist as distinct
rungs at all.

- **NA:** Not applicable.
  Discipline tests whether the document moves rung by rung up the ladder (observation →
  judgment → interpretation → implication).
  The dimension is engaged when the document moves between *any two* rungs at all,
  including a single observation that leads to a single implication.

  Signals that **do** engage the dimension (any one suffices):
  1. A claim drawn from an earlier observation in the same document ("X happened,
     therefore Y").
  2. A judgment, conclusion, or implication stated in the document’s own voice (not
     quoted from a source).
  3. A causal, evaluative, or predictive statement about something the document has just
     described.
  4. Connectives that signal reasoning: “therefore”, “so”, “this means”, “as a result”,
     “hence”, “it follows that”.

  Reserve NA for artifacts whose entire content is a pure reference table, a fact-only
  roster, a literal log excerpt, a definition list, or other content that states facts
  without reasoning *from* them.
  If the artifact reasons anywhere (even one sentence) score 1-5.

- **ERR:** Cannot assess (process failure; re-run the eval).
  The artifact attempts inferential reasoning but provides too little to score it: fewer
  than three sentences of reasoning, or reasoning truncated mid-argument.

- **1:** Rungs systematically blended; observations, judgments, and implications fused
  inside single clauses throughout.
  Reader cannot tell which sub-claim carries evidence.

- **2:** Rungs collapsed in key claims.
  Frequent leaps from observation directly to implication with the intermediate judgment
  and interpretation skipped or buried.

- **3:** Rungs distinguished in some sections but blended in others.
  Several key claims fuse observation and interpretation in one sentence; citation
  legitimacy from the observation rung leaks onto the implication rung.

- **4:** Score-5 mostly satisfied with one or two minor slips: one sentence that bundles
  observation and judgment, or an implication asserted without the interpretation rung
  explicitly named.

- **5:** Each key claim sits on a single, identifiable rung.
  No rung skipped on the way to a conclusion; transitions between rungs signaled ("from
  this we judge…", “which we interpret as…”, “which implies…”). Each rung carries its
  own evidence, and citations are tied to the rung they support, not transferred upward.
  For audits, evals, and high-stakes analysis, rung tags (`[observed]`, `[judged]`,
  `[interpreted]`, `[implied]`) used; in polished prose, the rung separation holds
  without tags.

#### R2. Soundness

Logical organization, well-defined terms, mechanisms named where causation is asserted,
visible chain from evidence to claim.
Focuses on the document’s logical structure; multiple-perspective consideration is
scored under J2 Fairness.

- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing or fewer than 3 sentences.
- **1:** Sloppy reasoning; imprecise statements; key terms undefined; arguments rest on
  unstated premises.
- **2:** Logical gaps or unclear terms; mechanism not named where causation is asserted;
  premises the argument depends on slipped in as background.
- **3:** Generally logical but could be more precise.
  Some claims asserted rather than argued; counter-evidence in the document not engaged;
  one or two premises implicit rather than named.
- **4:** Well-structured with mostly clear reasoning.
  Mechanisms named where causation is asserted.
  Internal consistency holds.
  Most premises are surfaced.
- **5:** Scientifically precise and logical.
  Mechanisms named, key terms defined, premises explicitly surfaced (inline
  `[ASSUMING: ...]` or a “Key assumptions” block), internal consistency tight (same
  number / fact / claim stated identically across sections), counter-evidence in the
  document engaged, asserted claims either argued or marked as assertions subject to
  falsifiable conditions.

#### R3. Precision

Claims and terms specified at the right granularity for the domain and audience.
Generic vocabulary in place of available specific vocabulary is imprecision, even when
the generic phrasing is true.
Distinct from E1 Clarity (register / readability) and P3 Breadth and P4 Depth (scope
completeness, section development): Precision scores granularity *within* each claim.

- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing or fewer than 3 sentences.
- **1:** Generic vocabulary throughout; entities referred to by category nouns ("the
  company," “the model,” “the regulation”); umbrella terms used where the
  sub-distinction matters; vague placeholders ("several," “various,” “many”) for items
  the doc could count or name.
- **2:** Frequent imprecision on key claims.
  Mix of proper and category names; quantitative claims at coarser resolution than the
  source supports or finer resolution than the measurement supports.
- **3:** Workable precision; key claims mostly use specific terms but several umbrella
  terms remain where the sub-distinction matters; one or two vague countables.
- **4:** Score-5 mostly satisfied with one or two minor slips: a single category-name
  reference, one quantitative claim with mismatched precision, or one umbrella term
  where the sub-distinction matters.
- **5:** Most specific term the audience can parse used throughout; domain entities
  referred to by proper name (versioned model names, statute sections, filing IDs,
  product names); umbrella terms avoided where sub-distinctions matter (capex vs
  maintenance / growth; users vs MAU / DAU / paid; latency vs p50 / p99); quantitative
  precision matches measurement precision; no vague placeholders for countable items
  (either counted: “12”, or named: “AWS, Azure, GCP, OCI”).

#### R4. Parsimony

Is each load-bearing reasoning chain the cleanest, simplest sound argument possible for
its conclusion? Length is not the metric; minimality given the per-step warrants in use
is. A long chain of strong deductive steps (a formal proof, a multi-step regulatory
cross-walk) is parsimonious when no shorter chain of the same warrant strength exists; a
short chain of weak inductive gestures is non-parsimonious when it elides intermediates
the conclusion requires.

Parsimony presupposes Soundness (R2). When a step is unsound, a longer sound chain would
do less damage to the conclusion, so the chain as written cannot be the most
parsimonious sound argument.
The Soundness → Parsimony cascade (see the rubric front matter) carries NA and ERR
through cleanly; a low Soundness score (1-2) still leaves Parsimony scorable 1-5 on
whatever sound chains remain.

Parsimony differs from E3 Concision (prose-level economy: words and paragraphs), from G3
Relevance (whether each source or section is on-task), from R1 Discipline (whether the
rungs are climbed in order), and from R2 Soundness (whether each step is valid).
Parsimony asks specifically: given the warrants in use, is the chain shape the minimum
sufficient?

- **NA:** Not applicable.
  Either the document makes no inferential claims (pure reference data, raw
  measurements, a glossary, or a structured form — no reasoning chain whose minimality
  could be evaluated), **or** Soundness is NA and the cascade applies (Parsimony NA
  follows Soundness NA; see *Cross-dimension cascades* in the rubric front matter).

- **ERR:** Cannot assess (process failure; re-run the eval).
  Either a procedural failure prevents scoring, **or** Soundness is ERR and the cascade
  applies (Parsimony ERR follows Soundness ERR — Parsimony is defined as the cleanest
  *sound* chain, so an unscored Soundness leaves nothing to be parsimonious about).
  A low Soundness score (1-2) is not an ERR trigger; in that case Parsimony is still
  scored 1-5 on whatever sound chains remain, and the reason may cite the upstream
  Soundness weakness.

- **1:** Obviously extraneous elements throughout the chains of reasoning: citable facts
  re-derived where the citation would have served the same purpose, weaker warrants
  substituted where stronger ones were available, or non-load-bearing rungs piled into
  chains that the conclusion does not require.
  The argument bears little resemblance to a minimum sufficient sound chain.

- **2:** Obviously extraneous elements in multiple load-bearing chains, or on the chains
  that carry headline claims.
  Substantial padding, weaker-warrant substitution where direct evidence existed, or
  re-derivation that adds neither inspectability nor confidence.

- **3:** Workable; the chains are roughly the right shape and the headline claims
  survive a minimum-sufficiency test, but several arguments could be tightened without
  loss of soundness or precision.

- **4:** A few arguments could be simplified but maintain the same level of soundness
  and precision; otherwise tight.
  A single re-derivation that could have been a citation without loss of inspectability,
  one chain using inductive language where a deductive step is available, or one
  redundant rung in an otherwise-tight chain.

- **5:** Every line of inference or argument appears to be the most clean and simple
  argument possible to a sound conclusion.
  Long chains appear only where the warrant strengths in use require them; short chains
  appear only where per-step warrants are strong enough to support them.
  No rung is extraneous; re-derivations are present only where they add inspectability,
  confidence, or pedagogy that a citation would not; no weaker warrant is substituted
  where a stronger one was available.

### Judgment

#### J1. Calibration

Claim strength must match evidence strength in both directions.
Overconfidence (strong claims on thin evidence) and underconfidence (hedging on solid
evidence) both fail.
Calibration carries the conclusion in practical writing that makes probability or
forecast claims.

- **NA:** Not applicable.
  The document makes no probability, forecast, confidence, or uncertainty claims, and
  the task does not require them.
- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing.
- **1:** Strong claims with no supporting evidence; probabilities asserted with no
  anchor; ranges absent where data warrants.
- **2:** Some calibration; probabilities anchored loosely; several probability claims
  overstate or understate the underlying data.
- **3:** Multiple calibration failures: probabilities asserted without base-rate
  anchors, small-sample shrinkage absent, or triangulation method missing on key
  estimates.
- **4:** Score-5 mostly satisfied with one or two minor slips: pre-event priors present
  but a single triangulated estimate doesn’t show its method, or shrinkage is implicit
  but the small-sample base is acknowledged elsewhere.
- **5:** Every probability claim cites its base rate or marks itself subjective;
  Bayesian shrinkage from small samples made explicit; ranges used where data supports
  them; triangulated estimates show the triangulation method; pre-event committed priors
  written before research and revisited post-research; deltas quantified; scenario
  probabilities sum to 100% and are checked.

#### J2. Fairness

Are opposing positions (a case for and a case against, or any oppositional framings)
argued at depth proportional to their plausibility, materiality, and strength?
Hidden asymmetry is a fairness failure; declared asymmetry (one side genuinely weaker
and the document says why) is not.

- **NA:** Not applicable.
  The document surfaces no oppositional framings and the task does not require them (a
  procedural runbook, a non-controversial reference).
- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing.
- **1:** One-sided argument with no counter-evidence engaged; one-sided framings of
  two-sided facts; risk inventory absent or weighted to a single class.
- **2:** Counter-evidence mentioned but not seriously engaged; the case for is anchored
  in numbers and the case against is anchored in scenarios (or vice versa) without
  explanation.
- **3:** Multiple fairness failures: notable depth asymmetry between opposing positions
  with no explanation, counterintuitive findings skewed without acknowledgement,
  falsification conditions absent or confused with confirmation conditions, or a risk
  inventory underweighted on multiple classes.
- **4:** Score-5 mostly satisfied with one or two minor slips: opposing-case depth
  proportional with one asymmetry acknowledged but not fully justified; counterintuitive
  findings present but the favor / challenge / neutral count not made explicit; risk
  inventory missing one class.
- **5:** Opposing positions engaged at depth proportional to their plausibility and
  strength; any asymmetry is declared and justified.
  Inverses of one-sided framings explicitly flagged.
  Risk inventory spans the relevant classes for the domain (technical, competitive,
  macro, regulatory, precedent-based).
  Falsification conditions named for each central claim, not substituted with
  confirmation conditions.
  Counterintuitive findings audited for confirmation bias (count of findings favoring,
  challenging, and neutral on the central claim).

#### J3. Robustness

Do key claims survive plausible alternative interpretations of the same evidence?
Calibration (J1) asks whether claim strength matches evidence strength; Fairness (J2)
asks whether opposing positions are argued at proportional depth.
Robustness asks the further question: granting the evidence and the framing, would a
*different reasonable lens* on the same evidence change the claim?

- **NA:** Not applicable.
  The document makes no interpretive judgments (a pure reference, a literal log).
- **ERR:** Cannot assess (process failure; re-run the eval).
  Content missing.
- **1:** Single interpretive lens applied without acknowledgement; alternative readings
  not considered; key claims presented as if the framing were obvious.
- **2:** Alternative interpretation noted in passing but not engaged.
  Claim would flip under a reasonable alternative lens; no acknowledgement.
- **3:** Multiple interpretive lenses surfaced but tested unevenly.
  Most-threatening alternative not engaged at the same depth as the chosen reading.
- **4:** Score-5 mostly satisfied with one or two minor slips: most-threatening
  alternative engaged but lens-flip implications not fully surfaced; sensitivity to
  interpretive frame acknowledged but not quantified relative to data sensitivity.
- **5:** Interpretive lens stated explicitly when evidence admits multiple readings; key
  claims tested against the most-threatening alternative interpretation at comparable
  depth; lens-dependent claims surfaced as findings rather than elided; sensitivity to
  interpretive frame stated alongside sensitivity to data perturbations.

## Contextual modifier: Tone / Reader Respect

The 20 dimensions above are the scored axes.
For human-facing documents, one further quality is worth checking but is not scored as a
dimension because it invites subjective evaluation:

> **Tone / Reader Respect:** The document avoids unnecessary coldness, blame,
> condescension, or opacity when written for humans.
> For agent-facing documents, this reduces to directness, explicit context, and absence
> of performative fluff.

This is a check, not a score.
The general standard guideline’s “Be engaging and warm” rule in
[common-doc-guidelines.md](common-doc-guidelines.md) is the canonical home for tone
guidance.
Cite a Tone / Reader Respect concern in an eval’s qualitative section, not as a
dimension score.

## Audit passes for high-stakes evals

For high-stakes evaluations, four narrower audit passes outperform one broad pass.
Each pass has a different cognitive load and a different tool stack; the
[practical-prose-eval-single.runbook.md](../runbooks/practical-prose-eval-single.runbook.md)
operationalizes them.

| Pass | Scope | Primary dimensions | Stack |
| --- | --- | --- | --- |
| Lint | Surface defects | F1 Organization, F2 Consistency, F3 Formatting, E1 Clarity (banned-register and vague-word checks) | `practical_prose_metrics.py`, linters, deterministic checks |
| Claim audit | Every quantitative claim against its cited source | G1 Verifiability, G2 Factuality | Source lookups, calculation re-runs |
| Reasoning audit | Mechanisms, assumptions, counter-evidence, alternative lenses | R1 Discipline, R2 Soundness, J2 Fairness, J3 Robustness | Subject-matter expert or fresh-context agent |
| Purpose audit | Output shape vs task shape; scope; skim-recoverability | P1 Suitability, P2 Scope, P3 Breadth, P4 Depth | Reader simulation; subject-matter expert |

The pass separation is **required** for high-stakes documents (audits, decision memos,
external research, security advisories), **recommended** for standard internal docs, and
**optional** for low-stakes drafts and operational notes where a single review pass fits
the risk. Where the discipline applies, do not combine passes; running them in parallel
by the same agent in the same context loses the cognitive separation that the four-pass
structure depends on.

## Failure-Mode Questions

Before the four-pass audit, high-stakes documents should be checked against the
claim-type-specific failure-mode questions below.
Each asks what would make this *kind* of claim wrong.
Documents that have not asked these questions tend to surface their fragility only after
the reader has acted on them.

| Claim type | Failure-mode question |
| --- | --- |
| Factual claim | What source would disconfirm this? |
| Quantitative claim | Are units, dates, scope, and rounding correct? |
| Causal claim | What mechanism connects cause and effect, and what would we expect to see if it were wrong? |
| Forecast | What base rate or precedent anchors it? |
| Recommendation | What assumption would reverse it? |
| Summary | What important nuance did compression remove? |
| Fairness claim | Would a serious opponent recognize their view in this characterization? |
| AI-generated claim | Was this verified, inferred from a source, or merely generated fluently? |

Cross-references to the guidelines:

- **Factual** and **AI-generated** rows operationalize §11.5 Verifiability ("name what
  would invalidate the claim").
- **Causal** row operationalizes §15.8 Soundness (the counterfactual test).
- **Quantitative** row operationalizes §12.2 Factuality (rounding/aggregation/unit
  conversion disclosure).
- **Forecast** row operationalizes J1 Calibration (base-rate anchoring).
- **Recommendation** row operationalizes §15.3 Soundness (surface unstated assumptions)
  and J3 Robustness (test against alternative interpretive lens).
- **Summary** row operationalizes P1 Suitability and P4 Depth (what the document doesn’t
  do; section depth matches importance).
- **Fairness** row operationalizes J2 Fairness (proportional representation; not equal
  airtime).

These are diagnostic prompts for evaluators, not new rules for writers; the rules they
invoke live in the guidelines.

## Notes

- **Metrics are evidence, not quality.** Quantitative metrics and rubric scores can
  reveal risks, but no metric is a substitute for reader value, factual support, and
  judgment. A document does not become better by adding visible rigor (more tags, more
  citations, more caveats, more structure, more words) unless those additions make the
  claims more inspectable, accurate, useful, or humane.
  Once rules become rubrics, agents and humans both tend to optimize the rubric; this
  clause exists to push back on that drift.
  See the Humane principle in `practical-prose-principles.md` for the underlying
  framing.
- **Self-eval overrates.** When the author scores their own artifact, scores skew high.
  External rubric passes (by a different agent or human) are more reliable for
  high-stakes assessments.
  Record whether the eval is self or external in the report metadata.
- **Scores are reductive.** A single dimension’s score is a summary, not a full review.
  Always pair scores with the parenthetical reason to preserve diagnostic information.
- **Right score depends on context.** A short status update doesn’t need to score 5 on
  P3 Breadth or P4 Depth; a security advisory shouldn’t score low on J1 Calibration even
  when brief. Don’t aggregate dimensions to a single number unless the use case calls for
  it (and then state the weighting).
  When aggregating, `NA` dimensions are excluded from the mean rather than treated as
  zero.

## Versioning

Current revision: **`pp20v2`**. Eval YAMLs produced under it set
`metadata.rubric_version: pp20v2`. The `from-metrics` subcommand of
`../scripts/eval_report.py` writes this automatically.

The rubric is still under active development; the version tag is the identity stamp for
“what schema this report was scored against,” not a release-stability promise.
Bump it on changes that could shift scores or break loaders:

- Dimension added, removed, renamed, or regrouped.
- Score-anchor language tightened in a way that could move scores.
- Score domain narrowed or widened.

`pp20v2` regrouped the six Form dimensions: the former six-dimension Expression group was
split into Expression (Clarity, Coherence, Concision) and Form (Organization, Consistency,
Formatting). The dimensions and their anchors are unchanged; only the grouping moved.

`../scripts/eval_compare.py` warns when comparing across rubric versions.
On any report whose `rubric_version` is not the current value the eval loader auto-coerces
`score: 0` to `ERR` and relocates the three Form dimensions out of the legacy `expression`
block into a `form` block (dropping the stale derived rollup so it recomputes), so
pre-`pp20v2` reports (legacy `pp20v1`, `20-dim-v1`, `18-dim-v1-stale-baseline`, `15-dim-v1`,
etc.) still load — but they should be re-scored against the current schema before being
reused as calibration baselines.

## Related docs

- [../README.md](../README.md): how the practical-prose layers fit together.
- [practical-prose-guidelines.md](practical-prose-guidelines.md): prescriptive rules for
  the same 20 dimensions.
- [practical-prose-metrics.md](practical-prose-metrics.md): quantitative metrics and
  qualitative checks per dimension; recommended frontmatter schema.
- [practical-prose-principles.md](practical-prose-principles.md): the seven principles
  the dimensions descend from.
- [practical-prose-eval-single.runbook.md](../runbooks/practical-prose-eval-single.runbook.md):
  operational steps for a single-document eval.
- [practical-prose-eval-compare.runbook.md](../runbooks/practical-prose-eval-compare.runbook.md):
  operational steps for comparing N evals.

<!-- This document follows common-doc-guidelines.md.
Review guidelines before editing.
-->
