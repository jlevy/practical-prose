---
title: Practical Prose Rubric
description: Descriptive 0-5 rubric for scoring a practical writing artifact across the 18 dimensions defined in practical-prose-guidelines.md.
date: 2026-05-11
status: active
---
# Practical Prose Rubric

Version: v0.1 (rubric: `18-dim-v1`, last update 2026-05-11)\
Joshua Levy (github.com/jlevy)

A descriptive 0-5 rubric for assessing practical writing artifacts (articles, blog
posts, research reports, design docs, specs, technical papers, decision memos) across
the 18 dimensions defined in
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
same 18 dimensions in the same five groups, using the same names and section numbers
(§1-§18). They are designed as a tight bidirectional map:

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
- **0** = applicable but unassessable (the dimension applies to this artifact, but the
  content needed to score it is missing or fragmentary).
- **NA** = not applicable to this artifact (the dimension does not apply — for example,
  Calibration on a document that makes no probability or forecast claims, or Fairness on
  a document that surfaces no opposing positions).

When you score below 5, cite the specific guideline rule that was missed in the
parenthetical reason.
If you cannot tie a low score to a missed rule, either the rubric is missing test
coverage or the score is wrong.

**Reader outcome governs local rule compliance.** The rubric checks whether the document
follows the guidelines, but the guidelines exist to help readers understand, decide, do,
verify, or maintain something — not to be followed for their own sake.
A document that scores high on every dimension but fails its actual reader is not a good
document. When local rule compliance and reader outcome conflict, reader outcome wins,
and the deviation is documented (see *Justified deviations* below).
The rubric is a strong instrument for catching avoidable defects; it is not a substitute
for asking whether the document worked.

NA must be reserved for dimensions the artifact’s task genuinely does not require.
If a high-stakes document plausibly should engage opposing positions and does not, that
is a low Fairness score, not NA. When aggregating, NA dimensions are excluded from any
mean rather than treated as zero so that lightweight artifacts are not penalized for not
needing every dimension.

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
| 8 |  | Organization | Are sections, headings, sequence, tables, figures, links, and cross-references arranged for navigation? |
| 9 |  | Style Consistency | Does the document follow the chosen style guide or house style consistently? |
| 10 |  | Formatting | Is the document visually and syntactically clean in its medium? |
| 11 | Grounding | Verifiability | Are claims traceable to sources or calculations? |
| 12 |  | Factuality | Do cited sources support the claims as asserted? |
| 13 | Reasoning | Inference Discipline | Are observation, judgment, interpretation, and implication kept distinct? |
| 14 |  | Soundness | Do claims follow from evidence through valid mechanisms? |
| 15 |  | Precision | Are claims and terms specified at the right granularity? |
| 16 | Judgment | Calibration | Does claim strength match evidence strength? |
| 17 |  | Fairness | Are opposing positions argued at proportional evidentiary depth? |
| 18 |  | Robustness | Do key claims survive plausible alternative interpretations? |

## How to score

For each dimension, assign either an integer 0-5 or `NA`, plus a brief parenthetical
reason.

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
| Vague language in ordinary prose ("very," “quickly”) | §5 Clarity | — |
| Vague magnitude in a scoped factual claim ("rapid growth") | §4 Depth | §5 Clarity |
| Vague countable / category name where specific term exists ("the company") | §15 Precision | §5 Clarity |
| Trite phrasing or banned-register hit | §5 Clarity | — |
| Canonicality declaration or word-choice / naming justification ("this is the canonical X"; “we use the term Y because…”) | §5 Clarity | §7 Concision |
| Replacement-history narration in a non-history genre ("previously named X"; “under the new layout”) | §7 Concision | §5 Clarity |
| Generic templated heading as sole section signal ("Overview," “Background,” “Notes”) | §8 Organization | §5 Clarity |
| Heading-level skip, table that should be prose, broken link | §8 Organization | — |
| Inconsistent dialect, casing, or parallel-list syntax | §9 Style Consistency | §5 Clarity |
| Spaced em-dash overuse (" — “ instead of ”—") | §9 Style Consistency | §5 Clarity |
| Malformed Markdown table, broken footnote anchor, misplaced footer | §10 Formatting | §8 Organization |
| Duplicated table / list content across sections | §7 Concision | §8 Organization |
| Undeclared or drifting scope on a multi-topic document | §2 Scope | §3 Breadth |
| Missing case class within declared scope (e.g., risk type omitted) | §3 Breadth | §17 Fairness |
| Thin development of a section the document’s purpose depends on | §4 Depth | §1 Suitability |
| Missing inline citation for a quantitative claim | §11 Verifiability | §10 Formatting |
| Number in prose doesn’t match source (silent rounding) | §12 Factuality | §11 Verifiability |
| Cited source doesn’t support the claim as asserted | §12 Factuality | §11 Verifiability |
| Mixed observation + interpretation in one sentence | §13 Inference Discipline | §14 Soundness |
| Probability claim without base-rate anchor | §16 Calibration | §14 Soundness |
| One-sided argument with no counter-evidence engaged | §17 Fairness | §16 Calibration |
| Key claim brittle under a different reasonable interpretive lens | §18 Robustness | §17 Fairness |

### Output format

`SCORE (REASON)`, matching the regex `(NA|[0-5]) \(.*?\)`. Cite line numbers, section
names, or quoted phrases in the reason where relevant.
Examples:

```
4 (Clear, correct prose throughout; one paragraph at L412-418 has trite phrasing —
"the agentic thesis fully crystallizes" — and could be tightened.)

3 (Mix of [VERIFIED] tags with primary sources and unverifiable claims around §1.10
competitive landscape — Vercel CEO benchmark quote at L820 has no tweet ID;
W3Techs market-share at L815 has no URL.)

5 (Bull / base / bear cases at §2.8 each have 3 named primitives + numerical thresholds;
risk register at §2.10 spans 5 classes; opposing positions argued at proportional
depth.)

NA (No probability, forecast, confidence, or uncertainty claims are made; the task is a
file-organization audit that does not call for calibration.)
```

## Score anchors by dimension

### Purpose

#### §1 Suitability

Does the document give the reader what they need, in the form the task requires?
A document can be clear, factual, and balanced and still fail Suitability if the reader
cannot extract the needed output, if the purpose was not named, or if the output shape
does not fit the task (a decision memo with no recommendation, an audit without
findings).

- **0:** Cannot assess.
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

#### §2 Scope

Is the scope of the document stated, and does the declared scope match the actual scope
of the work? Scope is upstream of §3 Breadth and §4 Depth: a document with no declared
scope cannot be evaluated for whether it covers everything relevant.

- **0:** Cannot assess.
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

#### §3 Breadth

Are the relevant areas within the declared scope covered?
Breadth is the *what is covered* question — relevant case classes, prior work, and
standard sources are present within scope.
The *how thoroughly* question is scored under §4 Depth.

- **NA:** Not applicable.
  The document is a single-fact note (a one-line status, a numeric reading) where there
  is no class structure to cover.
- **0:** Cannot assess.
  Content missing or scope undeclared (score the latter under §2).
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

#### §4 Depth

Are the important parts of the document developed to the level of detail, specificity,
evidence, and explanation the task requires?
Section depth matches section importance.

- **NA:** Not applicable.
  The document is a pure index, table of contents, or pointer-only artifact where depth
  is not the relevant question.
- **0:** Cannot assess.
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

#### §5 Clarity

Sentence-level readability: spelling, grammar, register, word choice.
Errors covered by spell-checkers, Grammarly, Vale, and the language-use parts of AP /
CMS. Concision is scored separately under §7; copyediting consistency (dialect,
parallel-list syntax, citation style) is scored under §9 Style Consistency; markup
validity is scored under §10 Formatting.

- **0:** Cannot assess.
  Content missing or fragmentary.
- **1:** Numerous spelling, punctuation, grammatical errors; sentences hard to follow.
- **2:** Errors but understandable.
- **3:** Typical business-email quality; few errors; may contain a few typos.
- **4:** Clear, correct language with flaws: trite phrases, gratuitous big words,
  occasional banned-register hits, parallel-structure padding ("It’s not X, it’s Y"
  without a real contrast), or sentences that are unnecessarily dense.
- **5:** Publication-ready grammar and clarity, with no material defects.
  Words chosen for precision; banned-register words (the canonical common-doc-guidelines
  §4.2 list) and parallel-structure padding absent or earned (per §5 rules 4 and 5); no
  pedantic, pedagogical, or self-referential prose — no canonicality declarations,
  word-choice justifications, or reading-order instructions (per rule 6). Suitable for
  high editorial standard publication; minor justified deviations are acceptable when
  documented and reader-serving.

#### §6 Coherence

Prose-level flow of ideas: paragraph cohesion, transitions, whether ideas progress
smoothly sentence to sentence.
Does not cover logical coherence (§14 Soundness) or arrangement of sections and visual
elements (§8 Organization).

- **0:** Cannot assess.
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

#### §7 Concision

The writing carries only the content the task requires.
Padding, repetition, and decorative content fail concision even when each sentence is
clear.

- **0:** Cannot assess.
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
  the data (though *whether* their shape fits is scored under §8 Organization).
  No replacement history outside genres that require it (per §7 rule 5): the document
  describes the present state, not what it replaced.

#### §8 Organization

Sections, headings, sequence, tables, figures, lists, links, and cross-references —
arrangement of the document.
Visual elements are not required (a tight prose document can score 5), but when present
they should be arranged well.
Markup validity is scored under §10 Formatting; style consistency is scored under §9.

- **0:** Cannot assess.
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
  requires. Headings cleave to the subject (per §8 rule 9): no generic templated headings
  ("Overview," “Background,” “Notes,” “Details”) standing alone as the only signal of
  section contents. Every table earns its tabular shape (parallel rows with a fixed
  schema) and is placed near its referencing prose; every figure has a caption
  explaining what it shows; links target stable anchors and resolve; cross-references
  name what they point to ("see §2.8 (named cruxes)" over “see §2.8”); visual elements
  deployed where they help, absent where prose is clearer.

#### §9 Style Consistency

Does the document follow the chosen style guide or house style consistently across
syntax, terminology, capitalization, punctuation, spelling, dates, numbers, units,
citations, and register?
Distinct from §5 Clarity (sentence-level readability) and §10 Formatting (markup
validity).

- **NA:** Not applicable.
  The document is too short or fragmentary for a style guide to apply (a single line, a
  log entry).
- **0:** Cannot assess.
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
  Em dashes used sparingly and in American style (no surrounding spaces), per §9 rule 7;
  spaced em-dash overuse is absent.

#### §10 Formatting

Is the document’s markup and visual presentation clean, valid, and compatible with the
chosen medium? Most rules under this dimension are deterministically lintable.
Distinct from §8 Organization (arrangement) and §9 Style Consistency (editorial polish).

- **NA:** Not applicable.
  The document is plain text with no markup, or a format where formatting concerns are
  outside scope.
- **0:** Cannot assess.
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

#### §11 Verifiability

Are claims traceable to specific sources, observations, calculations, or explicit
assumptions? A document scores high when a competent reader could check claims from what
the document provides, before any external lookup.
Verifiability is text-internal; Factuality (§12) is the source-aware check that the
audit would actually pass.
The strictness of the primary-source bar scales with stakes: research reports, audits,
and decision memos require primary sources for every quantitative claim; lightweight
operational notes only require sources for material claims.

- **NA:** Not applicable.
  The document makes no quantitative or verifiable claims (a pure prompt template, an
  outline of intent).
- **0:** Cannot assess.
  Content missing or fewer than one substantive claim.
- **1:** Quantitative claims with no source pointers; confidence tags absent or used
  without sources. The document cannot be audited from what it provides.
- **2:** Some sources cited but specificity is poor ("the Q4 transcript" with no date or
  section). Derived facts assert without showing the calculation.
- **3:** Most quantitative claims have a primary source pointer, but several are vague
  enough that finding the exact passage takes work.
  Confidence tags used but not consistently paired with source pointers.
- **4:** Score-5 mostly satisfied with one or two minor slips: a single quantitative
  claim without a source, or one `[VERIFIED]` tag without naming what was verified.
- **5:** Quantitative claims source-traceable at the stakes-appropriate bar (every
  primary source for high-stakes / external / decision-bearing documents; material
  claims sourced and basis stated for low-stakes notes).
  Citations specific enough to verify (URL, document ID, page or section number, commit
  SHA). Confidence tags pair with source pointers; derived facts show the calculation
  inline (`[DERIVED: 89.6 / 614.5 = 14.6%]`). Unverifiable claims marked rather than
  silently inherited.

#### §12 Factuality

Do cited sources actually support the claim, at the asserted strength, for the asserted
entity, date, and scope?
Verifiability (§11) tests whether the document is auditable; Factuality tests whether
the audit would pass.
Source-aware: scoring requires checking the cited sources, not just inspecting the
document.

- **NA:** Not applicable.
  The document cites no sources because it makes no source-checkable claims.
- **0:** Cannot assess.
  Sources cited but unreachable, or content missing.
- **1:** Major claims contradicted by their cited sources.
  Hallucinated sources or sources that don’t contain the cited content.
- **2:** Several claims overstate or paraphrase past their sources.
  Numbers in prose don’t match cited sources without disclosure; entity, date, or scope
  mismatches.
- **3:** Most claims supported by their sources but with notable strength mismatches or
  paraphrase drift. One or two cases of advocate-quoted-as-neutral or
  commentary-quoted-as-primary.
- **4:** Score-5 mostly satisfied with one or two minor slips: one undisclosed rounding,
  or one entity/date mismatch.
- **5:** Every cited source supports the claim at the asserted strength.
  Numbers in prose match cited sources, or disclose rounding, aggregation, unit
  conversion, or derivation explicitly.
  Entity, date, and scope of citations match the claim.
  Sources represent the cited entity, not its inverse.
  No hallucinated URLs, document IDs, or authors; every reference resolves to a real
  artifact that contains the cited content.

### Reasoning

#### §13 Inference Discipline

Moving rung by rung up the ladder of inference (observation → judgment → interpretation
→ implication). Each rung named on its own terms; none skipped, none blended into its
neighbor. Sister of Soundness (§14): Soundness asks whether the chain holds together;
Inference Discipline asks whether the rungs exist as distinct rungs at all.

- **NA:** Not applicable.
  The document makes no inferential claims (a pure reference table, a literal log
  excerpt).
- **0:** Cannot assess.
  Content missing or fewer than 3 sentences.
- **1:** Rungs systematically blended; observations, judgments, and implications fused
  inside single clauses throughout.
  Reader cannot tell which sub-claim carries evidence.
- **2:** Rungs collapsed in key claims.
  Frequent leaps from observation directly to implication with the intermediate judgment
  and interpretation skipped or buried.
- **3:** Rungs distinguished in some sections but blended in others.
  Several key claims fuse observation + interpretation in one sentence; citation
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

#### §14 Soundness

Logical organization, well-defined terms, mechanisms named where causation is asserted,
visible chain from evidence to claim.
Focuses on the document’s logical structure; multiple-perspective consideration is
scored under §17 Fairness.

- **0:** Cannot assess.
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

#### §15 Precision

Claims and terms specified at the right granularity for the domain and audience.
Generic vocabulary in place of available specific vocabulary is imprecision, even when
the generic phrasing is true.
Distinct from §5 Clarity (register / readability) and §3 Breadth + §4 Depth (scope
completeness, section development): Precision scores granularity *within* each claim.

- **0:** Cannot assess.
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

### Judgment

#### §16 Calibration

Claim strength must match evidence strength in both directions.
Overconfidence (strong claims on thin evidence) and underconfidence (hedging on solid
evidence) both fail.
Calibration carries the conclusion in practical writing that makes probability or
forecast claims.

- **NA:** Not applicable.
  The document makes no probability, forecast, confidence, or uncertainty claims, and
  the task does not require them.
- **0:** Cannot assess.
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

#### §17 Fairness

Are opposing positions (a case for and a case against, or any oppositional framings)
argued at depth proportional to their plausibility, materiality, and strength?
Hidden asymmetry is a fairness failure; declared asymmetry (one side genuinely weaker
and the document says why) is not.

- **NA:** Not applicable.
  The document surfaces no oppositional framings and the task does not require them (a
  procedural runbook, a non-controversial reference).
- **0:** Cannot assess.
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

#### §18 Robustness

Do key claims survive plausible alternative interpretations of the same evidence?
Calibration (§16) asks whether claim strength matches evidence strength; Fairness (§17)
asks whether opposing positions are argued at proportional depth.
Robustness asks the further question: granting the evidence and the framing, would a
*different reasonable lens* on the same evidence change the claim?

- **NA:** Not applicable.
  The document makes no interpretive judgments (a pure reference, a literal log).
- **0:** Cannot assess.
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

The 18 dimensions above are the scored axes.
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
| Lint | Surface defects | §8 Organization, §9 Style Consistency, §10 Formatting, §5 Clarity (banned-register and vague-word checks) | `practical_prose_metrics.py`, linters, deterministic checks |
| Claim audit | Every quantitative claim against its cited source | §11 Verifiability, §12 Factuality | Source lookups, calculation re-runs |
| Reasoning audit | Mechanisms, assumptions, counter-evidence, alternative lenses | §13 Inference Discipline, §14 Soundness, §17 Fairness, §18 Robustness | Subject-matter expert or fresh-context agent |
| Purpose audit | Output shape vs task shape; scope; skim-recoverability | §1 Suitability, §2 Scope, §3 Breadth, §4 Depth | Reader simulation; subject-matter expert |

The pass separation is **required** for high-stakes documents (audits, decision memos,
external research, security advisories), **recommended** for standard internal docs, and
**optional** for low-stakes drafts and operational notes where a single review pass fits
the risk. Where the discipline applies, do not combine passes — running them in parallel
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
- **Causal** row operationalizes §14.8 Soundness (the counterfactual test).
- **Quantitative** row operationalizes §12.2 Factuality (rounding/aggregation/unit
  conversion disclosure).
- **Forecast** row operationalizes §16 Calibration (base-rate anchoring).
- **Recommendation** row operationalizes §14.3 Soundness (surface unstated assumptions)
  and §18 Robustness (test against alternative interpretive lens).
- **Summary** row operationalizes §1 Suitability and §4 Depth (what the document doesn’t
  do; section depth matches importance).
- **Fairness** row operationalizes §17 Fairness (proportional representation; not equal
  airtime).

These are diagnostic prompts for evaluators, not new rules for writers; the rules they
invoke live in the guidelines.

## Notes

- **Metrics are evidence, not quality.** Quantitative metrics and rubric scores can
  reveal risks, but no metric is a substitute for reader value, factual support, and
  judgment. A document does not become better by adding visible rigor — more tags, more
  citations, more caveats, more structure, more words — unless those additions make the
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
  §3 Breadth or §4 Depth; a security advisory shouldn’t score low on §16 Calibration
  even when brief. Don’t aggregate dimensions to a single number unless the use case
  calls for it (and then state the weighting).
  When aggregating, `NA` dimensions are excluded from the mean rather than treated as
  zero.

## Versioning

Current revision: **`18-dim-v1`**. Eval YAMLs produced under it set
`metadata.rubric_version: 18-dim-v1`. The `from-metrics` subcommand of
`../scripts/eval_report.py` writes this automatically.

The previous revision `15-dim-v1` covered 15 dimensions in five groups; `18-dim-v1` adds
three dimensions (Breadth + Depth split from Coverage; Style Consistency; Formatting),
renames Structure → Organization, and introduces the `NA` value distinct from `0`.
Score-anchor language was tightened in several dimensions.

Bump the version on substantive changes:

- New dimension added or removed: bump the dim count (e.g., `18-dim-v1` → `19-dim-v1`).
- Anchor language changed in a way that could shift scores: bump the rev (`18-dim-v1` →
  `18-dim-v2`). The rubric schema in `../scripts/rubric_schema.json` is the canonical
  source for the current version string; bumping the rubric here means bumping `version`
  there too.

`../scripts/eval_compare.py` warns when comparing across rubric versions.
Pinned regression fixtures (`../scripts/fixtures/rev{1,2}-net.eval.yaml`,
`../scripts/fixtures/{guidelines,runbook}-self.eval.yaml`) were scored under `15-dim-v1`
and must be re-scored before they can be reused under `18-dim-v1`.

## Related docs

- [../README.md](../README.md): how the practical-prose layers fit together.
- [practical-prose-guidelines.md](practical-prose-guidelines.md): prescriptive rules for
  the same 18 dimensions.
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
