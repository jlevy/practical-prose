# Review: Practical Prose README

## Scope and context

- **Document:** [README.md](../../../README.md), the root document of the Practical
  Prose project, reviewed at the post-v0.1.0 state (Quick Start under the intro, Example
  Evaluations cards, published-package install paths).
- **Purpose:** orient a new reader, motivate the project, and route to the principles,
  guidelines, rubric, skills, and `pprose` tooling.
- **Audience:** three distinct readers — human writers seeking the rules, developers
  evaluating the tooling, and coding agents routed via `AGENTS.md`.
- **Risk level:** low-to-medium.
  A README is not a compliance document, but this one is the public face of a project
  *about* writing quality, so its own defects carry reputational weight.

This review is read-only: no edits were made to the source and no scores are assigned.
It replaces the stale review of 2026-06-06, which predated the current structure.

## Strengths

- **P1 Suitability.** The opening two sentences state the thesis cleanly, and Quick
  Start now sits high enough that a tool-first reader reaches `uvx pprose` by line 60.
- **F1 Organization.** Heading hierarchy is clean, headings cleave to their subjects (no
  generic "Overview"/"Background"), anchors all resolve, and the Layers table gives the
  system a legible architecture.
- **J2 Fairness / J3 Robustness.** The Personal Note concedes the strongest
  counterargument ("I realize trying to codify rules for good writing is difficult to
  impossible") and answers it.
  “Is It Mature? No.” is disarming and builds trust.
- **G1 Verifiability.** The Example Evaluations caption names the grading model, warns
  that scores vary between runs, and links the source texts and the regeneration runbook
  — the README practices the disclosure its own rubric demands.
- **E1 Clarity.** Zero banned-register hits, zero generic headings, zero pedantic
  markers on the deterministic lint.
  “Fluency is cheap. Judgment remains precious.”
  is the kind of line readers will quote.

## Tier 1 — Common edit (formatting and structure)

1. **Spaced em dash** at line 58: “with [uv](…) — no install step required”.
   House style is zero spaced em dashes (common-doc-guidelines, F2 rule 7; the metrics
   pass flags exactly one).
   Recast ("…with uv—no install step required" or use a colon).
2. **Relative date** at line 121: “I’ve only been using it for the last month or two”
   will silently rot. Anchor it absolutely, e.g. “since spring 2026” or “as of v0.1.0
   (June 2026)” — which also lets the section acknowledge the package is now published.

## Tier 2 — Copy edit (Expression and Form)

1. **E1/R3 — “Metrics” word collision** (line 86). “What Is Here?”
   item 2 calls the 20 dimensions “Metrics of writing quality,” but “metrics” elsewhere
   means the deterministic `pprose metrics` signals and the Metrics layer doc.
   The section it links to is titled “Qualitative *Measures* of Writing.”
   Use “Measures” or “Dimensions” here so the three senses of “metrics” stop colliding.
2. **E1 — fuzzy antecedent** (line 47): “we could adapt them to other languages” — the
   nearest plural is “AI translations”; the intended antecedent (the guidelines or
   elements) is two sentences back.
   Name it.
3. **E2/E3 — Quick Start density** (lines 66-74). One paragraph carries five clauses of
   installer mechanics (surfaces, mirror paths, marker-bounded block, idempotency, scope
   flags). The `--project`/`--global`/`--surfaces` sentence is reference material, not
   quick-start material; consider moving it to Tooling and keeping Quick Start to “two
   commands, here’s what install writes, links for the rest.”
4. **E1 — stilted opener** (line 214): “Principles are of value, but when an editor
   evaluates a piece of writing, they look at specific qualities” — tighten ("Editors do
   not evaluate against principles; they look at specific qualities…" or similar).
5. **R3 — “The visualization tool scores any document”** (line 100): the LLM scores; the
   tool renders. “evaluates … and renders the result as a card” is more precise, and
   matches item 4 of “What Is Here?”.

## Tier 3 — Full feedback (substantive — author judgment)

Ordered by severity.

1. **G2 Factuality — “0-5 scoring anchors” is wrong, twice** (lines 242-243 and the
   Rubric row of the Layers table, line 255). The rubric is explicit: “Numeric scores
   are always 1-5: there is no 0,” plus NA/ERR sentinels — and it explains *why* at
   length. The README contradicting its own rubric on the rubric’s most deliberate design
   decision is the single worst defect here: it is exactly the kind of error the project
   teaches readers to catch.
   Fix is one character in two places ("1-5"), but it is a factual claim, so it is filed
   here rather than silently tiered lower.
2. **E3/E2 — three motivational passages make the same argument.** “Clear Writing in the
   Age of Slop” (line 17), the Personal Note (line 128), and “Practical Writing in the
   Age of AI” (line 168) each hit the same beats: slop volume, judgment over fluency,
   and augmentation (Engelbart’s augment-not-replace point appears twice).
   Each passage is good; together they cost roughly two of the README’s ten pages
   re-arguing a point the reader accepted on page one.
   Options: (a) give each a distinct job — problem (Slop), credibility (Personal Note),
   philosophy (Age of AI) — and cut each to that job; or (b) fold “Age of AI” into the
   intro and keep the Personal Note as the only reprise.
   Roughly 15% of total length is recoverable without losing a point.
3. **J2/P1 blind spot — the LLM-as-judge objection is never addressed.** The first
   question a skeptical reader asks of the eval cards is: “isn’t this just an LLM
   grading vibes — and isn’t using LLMs to judge LLM slop circular?”
   The project already has the strongest possible answer, sitting unused in the rubric’s
   Notes: *metrics are evidence, not quality; self-eval overrates; scores are reductive;
   reader outcome governs rule compliance.* A short “What the scores are — and aren’t”
   paragraph under Example Evaluations (three sentences: evidence-not-verdict, run
   variance, designed to catch avoidable defects rather than crown winners) would
   preempt the predictable critique and make the project look more rigorous, not less.
4. **P3 blind spot — no positioning against alternatives.** Readers will silently
   compare this to Vale/textlint/LanguageTool, the Google/Microsoft style guides, and
   “just ask Claude to review my doc.”
   The differentiated answer is genuinely strong and currently implicit: deterministic
   linters stop at Form and surface Expression; style guides are prescriptive but
   unscored; ad-hoc LLM review is uncalibrated and unanchored.
   This system adds the Reasoning/Grounding/Judgment dimensions no linter can check,
   with anchored scores, NA/ERR discipline, and agent-native packaging.
   Three bullets after “What Is Here?”
   would convert that from implicit to stated.
5. **P1 — four maps, one territory.** “Quick Start,” “What Is Here?”, “Where to Start,”
   and “Layers” are all routing content (roughly a quarter of the document).
   Each is individually justified, but a reader meets the *fourth* table of pointers
   before meeting any actual guideline text.
   Consider merging “Where to Start” into “What Is Here?”
   (its bullets are the same items with task framing), or moving it directly after the
   intro and letting “Layers” be the only architectural map.
6. **J3 — a strategic framing left on the table:** both demo documents are human-written
   (1945 essay, Apple legal).
   That quietly proves the rubric measures *writing*, not AI-ness — the strongest
   available rebuttal to “this is just an AI slop detector.”
   One caption sentence ("Note both examples are human-written: the dimensions predate
   AI and apply to any practical prose") would bank the point.
7. **F1 — hero placement (option, not defect).** The eval cards are the README’s most
   concrete, shareable artifact, and they sit below four subsections of motivation.
   GitHub convention favors show-then-tell; promoting Example Evaluations to an H2
   directly after the opening paragraphs (or placing one card beside the intro) would
   hook skimmers earlier.
   Current placement is defensible — flagged as a choice.

## Next steps

- Tiers 1-2 are mechanical: run `pprose-copy-edit` on README.md to apply them (7
  findings), or apply by hand in one short pass.
- Tier 3 items 1 (the 1-5 fix) and 6 (caption sentence) are one-line author calls; items
  2-5 and 7 are structural decisions worth deciding before any further README polish.
- For a scored rubric instead of tiers, use `pprose-eval`; to compare a revision against
  this version, use `pprose-compare`.

* * *

## Proposed drafts (for author review)

Status: the Tier 1, Tier 2, and Tier 3 item 1 fixes were applied to README.md on
2026-06-09 (line references above are to the reviewed revision).
The drafts below cover the remaining Tier 3 items.
Each keeps the README’s existing voice: short declaratives, question-form section
headings, first person where the original uses it, unspaced em dashes.
Nothing below has been applied.

### Draft A — “What the scores are—and aren’t” (Tier 3 items 3 and 6)

Add as a short paragraph directly after the Example Evaluations caption.
The rhetorical move mirrors the Personal Note: concede the objection in the first
sentence, then answer it with the mechanism.

> A fair question: isn’t this just an LLM grading vibes?
> It would be, without anchors.
> Each score is a 1-5 grade against descriptive anchors, and every score below 5 must
> cite the specific guideline rule the document missed—so a grade can be inspected,
> argued with, and re-run.
> Scores still vary somewhat between runs and models; treat them as an editor’s
> marked-up draft: evidence, not a verdict.
> No score substitutes for the question that governs everything else—did the document
> work for its reader?
> Note also that both examples are human-written.
> The dimensions measure writing, not AI-ness; they apply equally to a 1945 essay, a
> legal contract, or yesterday’s research report.

(If this paragraph is added, the caption’s existing “scores depend on the model and vary
slightly between runs” sentence can be dropped to avoid saying it twice.)

### Draft B — “How Is This Different?” (Tier 3 item 4)

Add as a new H3 between “What Is Here?”
and “Example Evaluations”.
The argument: name the alternatives concretely, grant each its strength in one clause,
then land on the fourteen dimensions nothing else covers.

> ### How Is This Different?

> Pieces of this exist elsewhere.
> Style linters like Vale and LanguageTool check spelling, register, and house style
> deterministically—roughly the Expression and Form dimensions, six of the twenty.
> Style guides like Chicago and the Google and Microsoft developer guides are
> prescriptive but unscored: they say what to do, not how a draft measures up.
> And asking a model to “look this over” is fast but unanchored: the feedback shifts
> with every prompt and leaves nothing to argue against.
> 
> The other fourteen dimensions—purpose, reasoning, grounding, and judgment—are where
> practical documents actually fail, and no linter can check them.
> This project covers all twenty with one vocabulary: prescriptive guidelines for
> writing, descriptive anchors for scoring, deterministic metrics where they help,
> packaged so humans and agents apply the same standards.

### Draft C — consolidated “Practical Writing in the Age of AI” (Tier 3 item 2)

Replace the current section body.
The job split: “Age of Slop” keeps the problem, the Personal Note keeps credibility and
the Engelbart close (which currently appears twice; this draft removes the duplicate),
and this section keeps the philosophy—why codify at all.
About 40% shorter; the cut lines are beats already made in the intro.

> ## Practical Writing in the Age of AI

> Technical writers and editors have known for centuries that the best way to validate
> written ideas is disciplined editorial review.
> Evidence can be checked, reasoning can be inspected, uncertainty can be calibrated.
> By enforcing standards for quality writing, we think more clearly.
> 
> What is different now is volume.
> Language is drafted, transformed, summarized, and evaluated by LLMs at a scale no
> human attention can filter or edit.
> Fluency is cheap. Judgment remains precious.
> 
> That is the case for codifying standards: not to replace editorial judgment but to
> make it teachable—to people and to machines.
> You *can* outsource writing and thinking to agents.
> But you can’t outsource your understanding or your judgment.

### Draft D — fold “Where to Start” into “What Is Here?” (Tier 3 item 5)

Append the task-routing list to the end of “What Is Here?”
and delete the standalone “## Where to Start” H2. This removes one of the four maps
without losing a pointer.

> Depending on your task:
> 
> - **Writing a document and want the rules:**
>   [practical-prose-guidelines.md](docs/practical-prose-guidelines.md).
> - **Scoring a document and want the anchors:**
>   [practical-prose-rubric.md](docs/practical-prose-rubric.md).
> - **Running a pre-publish self-audit:**
>   [practical-prose-quick-checklist.md](shortcuts/practical-prose-quick-checklist.md).
> - **Running a formal eval:** the [runbooks/](runbooks/) directory.
> - **Understanding why a rule exists:**
>   [practical-prose-principles.md](docs/practical-prose-principles.md) and
>   [practical-prose-bibliography.md](docs/practical-prose-bibliography.md).
> - **Looking at the tooling:** [tools/pprose/](tools/pprose/), the installable Python
>   package with the metrics, scoring, and report generators.

### Draft E — hero placement (Tier 3 item 7, optional)

If show-then-tell wins: move “Example Evaluations” up to directly follow the two opening
paragraphs of “Clear Writing Aids Clear Thinking”, so the order becomes thesis → cards →
motivation → Scope → Quick Start.
No text changes needed beyond the move; Draft A’s paragraph travels with the section.
This is the highest-variance suggestion—it trades a measured build-up for a faster
hook—so it is listed last and purely as an option.

* * *

## Consolidated revision plan (chunks for review)

This plan merges two work streams into reviewable chunks: the remaining README revisions
(Drafts A-E above) and the incorporation of the Holloway editorial guidance (analysis in
[reviews-holloway-editorial-guidance.md](../reviews-holloway-editorial-guidance.md);
source: `~/wrk/github/editorial-guidance/README.md`, cited below by its line numbers).
Where new content is proposed, the actual text is included — copied whole cloth from the
source where the original wording is the asset — so review happens against real words,
not summaries.

**Chunk status:**

| Chunk | Contents | Depends on | Status |
| --- | --- | --- | --- |
| 1 | README Drafts A-E (above) | — | Drafted; awaiting per-draft approval |
| 2 | New genre doc `docs/writing-practical-guides.md` | — | **Created** — review [the doc itself](../../writing-practical-guides.md) |
| 3 | New runbook `runbooks/practical-guide-groundwork.runbook.md` | — | Frame + verbatim source below |
| 4 | Targeted merges (bibliography, G1 link taxonomy, E1 voices) | — | Exact edits below |
| 5 | README + Layers updates | Chunks 2-3 | Specified below |
| 6 | Housekeeping (resource sync, beads, review-doc moves) | Chunks 2-5 | Checklist below |

Recommended order: approve Chunk 1 items independently (they are README-only); land
Chunk 2, then 3, then 4 (each independently shippable); Chunk 5 only after 2-3 exist so
links resolve; Chunk 6 last.

### Chunk 1 — README Drafts A-E (decision list)

No new text needed; the drafts are above.
Decisions requested:

- **Draft A** (scores-aren’t-verdicts + human-written point): recommend **apply**.
- **Draft B** (How Is This Different?): recommend **apply**, with one addition once
  Chunk 2 lands: a closing line that the guidelines come from editorial practice on
  published guides (the Holloway lineage), not from prompt engineering.
- **Draft C** (consolidated Age of AI): recommend **apply**; the only loss is the
  duplicated Engelbart paragraph, which survives in the Personal Note.
- **Draft D** (fold Where to Start into What Is Here?): recommend **apply**; Chunk 5
  adds one bullet to the folded list for the new genre doc.
- **Draft E** (hero placement): genuinely optional; **author call**, no recommendation.

### Chunk 2 — new doc: `docs/writing-practical-guides.md` (full draft)

Genre supplement layer: builds on the practical-prose layers the way they build on
common-doc-guidelines.
Twelve guidelines (the Holloway twelve, minus “Consider diverse experience” which is
research process and moves to the Chunk 3 runbook, plus “Cover Controversy” which the
source carried unnumbered).
Distinctive source phrasings are preserved verbatim; Holloway product and process
references are removed; every guideline opens with an applicability header.

> **Status (2026-06-09): created as
> [docs/writing-practical-guides.md](../../writing-practical-guides.md) — review the doc
> itself; it is now canonical.** The inline draft below is retained as the draft of
> record but is superseded.
> Deliberate deltas applied at creation, found in the second review pass: (1) all spaced
> em dashes normalized to unspaced per house style (F2 rule 7; the inline draft had
> ~20); (2) “This is emphatically not clickbait” → “This is not clickbait” (the only
> banned-register hit; the quoted negative examples like “our amazing guide unlocks
> secrets!” are mention-not-use and clean per lint); (3) the groundwork-runbook
> references are plain text marked “planned” rather than links, since the runbook lands
> in Chunk 3 — Chunk 5 wires the real links.
> Second-pass lint: 0 spaced em dashes, 0 banned hits, 0 generic headings, 0 pedantic
> markers; all four internal link targets resolve.

Full proposed text:

~~~markdown
# Writing Practical Guides

Version: v0.1 (last update 2026-06-09)\
Joshua Levy (github.com/jlevy)

Guidelines for a specific genre of practical prose: the **comprehensive practical
guide** — a reference work that helps readers navigate a complex topic, built for
recurring use by multiple kinds of readers.
These guidelines extend [practical-prose-guidelines.md](practical-prose-guidelines.md)
the way that document extends
[common-doc-guidelines.md](common-doc-guidelines.md): everything there still applies;
this adds what the guide genre demands.
They distill years of editorial practice developing long-form guides (at Holloway and
before), refined in conversations with editors, writers, and expert reviewers.

These guidelines are deliberately opinionated, and several push writers and editors in
directions they don't typically go.
Not all practical writing is of this type.
Each guideline below opens with an **applies when** note; when the condition does not
hold, the guideline does not apply, and following it anyway can make a document worse.

## What Makes a Guide?

A guide has a single purpose: **to help the reader navigate complexities.**
It aims to be the best single place to start or return to on the topic it covers.

Guide content differs from other nonfiction in several ways:

- **Practical orientation:** it offers helpful guidance, and gives the reader
  foundations to build future knowledge and capabilities.
- **Technical or complex subject matter:** this kind of writing is of greatest value
  when the topic is complex and takes commitment to learn — an abundance of pitfalls,
  confusions, and important details.
- **Ambitious in detail and scope:** the goal is to provide the most credible resource
  available.
- **Built for recurring use:** a guide is like a reference book with a long shelf life,
  not a blog post you forget after a day.
  It continues to be of use to a single person over time as they encounter different
  problems and questions.
- **Built to improve:** on complex topics subject to change, no guide is ever perfect;
  it must be built to improve over time, not published as the fixed work of a single
  author.

A guide is *not*: historical or narrative nonfiction; writing devoted to a single
thesis; writing primarily for entertainment; or celebrity-oriented writing that is
mostly of interest because of *who* is writing.
Nor is it Wikipedia (restricted by policy to consensus facts, where practical or highly
specific guidance is typically not allowed) or a Q&A site (single answers to specific
problems, not a comprehensive, trustworthy overview).

## When These Guidelines Apply

The guide genre presumes four conditions, and each guideline below leans on one or more
of them:

1. **Discretionary readership:** the reader can leave at any time.
2. **Situational variability:** the right action depends on the reader's situation;
   there is often no single correct answer.
3. **Mixed and multi-sided audiences:** readers vary in expertise and may sit on
   different sides of the topic.
4. **Long shelf life:** the work is meant for recurring use and ongoing improvement.

A runbook, a spec, or an internal memo typically fails several of these conditions —
and several guidelines below would harm those documents.
Check the applies-when note before applying any of them.

## The Guidelines

### 1. Make Deep Coverage Accessible

**Applies when:** the audience spans beginner to expert (condition 3).
**Does not apply when:** the audience is uniform (a spec for one team).

Some classic reference books are respected and full of detail, yet hard to read for
anyone who's not an expert.
Other books are engaging but oversimplify and omit details.
A guide aspires to be both deep *and* engaging — technical *and* accessible.
Both big ideas and technical details are essential: ideally, a guide weaves details
together through foundational concepts and broader ideas.
Can both novice and expert learn (different) things quickly?

Specific strategies:

- Start with zero assumptions about what a reader knows, so anyone can start reading
  easily and skip ahead if it's too basic.
- Combine fundamental concepts and brief overviews with deeper technical detail.
  Include highly technical points that are important, even if beginners may find them
  hard to follow (and link to further detail).
- Use section titles that guide the hurried reader to something of interest.
- Emphasize key details right up front, such as surprising but helpful statistics.
- Be specific and give examples in the same place you state a general principle.
- Emphasize holistic, clear overviews or diagrams that make something complex more
  understandable. What kind of diagram would impress both a beginner and an expert?
- Emphasize confusions, overlooked suggestions, pitfalls, and misunderstandings that
  are common.
- Use technical terminology whenever appropriate, but always define the terms clearly.
- Give helpful or illuminating historical background that many may not be aware of.

### 2. Earn the Respect of Experts First

**Applies when:** the work is a public reference whose authority matters (conditions 1
and 4). **Does not apply when:** the readership is known and credibility is
established (internal docs).

The authority of any reference rests on the opinion of experts.
Even elementary material can and should be explained in a way experts consider
credible. Accuracy, precision, and clarity in their estimation is the first goal;
accessibility comes next, but never when it compromises credibility among experts.

Two things make writing credible to experts:

- **Technical vigilance:** be accurate, precise, logical, and clear — and explicit when
  there is uncertainty or controversy.
  On this there is no compromise.
- **Stylistic clarity:** experts are remarkably sensitive to secondary signals — not
  focusing on details, overlooking exceptions, not conveying context, over-marketing,
  or over-generalizing.

It's easy to slip into marketing-speak ("our amazing guide unlocks secrets!") or gloss
over confusing nuances ("just remember these five tricks!").
Be ambitious enough to aim for comprehensibility and credibility, but stay humble: if
the topic is complex enough to deserve a guide, the guide is imperfect and improving.

### 3. Start From the Beginning

**Applies when:** readers arrive with widely varying foundations (condition 3).
**Does not apply when:** shared context is guaranteed (a team runbook can start in the
middle — that is what its context section is for).

A common mistake for a knowledgeable writer is to "start in the middle": writing at the
level they're most comfortable with, without relating that knowledge to the topic's
foundations or broader context.
It's easiest to write for someone with similar expertise to yourself — the
[curse of knowledge](https://en.wikipedia.org/wiki/Curse_of_knowledge).

So when outlining and writing a reference work, start from the beginning: foundations,
background, readers' motivations, and the significance of the subject, working toward
more advanced ideas with details inserted liberally.
Watch for the definition failures that signal middle-starting:

- Concepts so common they seem obvious but are in fact complex, left undefined.
  (What is *capital*, anyway? What is a company? Is currency the same as money?)
- Circular definitions, where A depends on B and B depends on A.
- Definitions out of order, where A depends on C but C isn't defined — like talking
  about investors before stock, or blockchain blocks before hashing.

(Starting in the middle is fine when assembling your own notes — just backfill the
foundations during groundwork and outlining; see
[the groundwork runbook](../runbooks/practical-guide-groundwork.runbook.md).)

### 4. Imagine Readers That Are "100% Intelligent and 100% Ignorant"

**Applies when:** always within the guide genre; this is its central heuristic.
**Does not apply when:** the genre itself doesn't (expert-to-expert documents may
assume shared knowledge).

Imagine your readers start out **100% intelligent and 100% ignorant**. In reality most
people already know something, but the assumption has important advantages:

- It reminds you to start from the beginning without assuming too much knowledge.
- People with varied knowledge can start early and skim forward, filling gaps; beginners
  can see everything they don't yet know.
- It avoids "writing down" to beginners — condescension, or over-simplifying important
  details out of fear they will confuse a novice.

**Embrace essential complexity.** Details matter.
As Einstein [possibly said](https://quoteinvestigator.com/2011/05/13/einstein-simple/),
"Everything should be made as simple as possible but no simpler."
It's tempting to hide messy or confusing details from readers, but do not underestimate
people's ability to manage information when it is supplied well.

**If you respect the reader, the reader will respect you.** The ability to learn has
little to do with past exposure to a topic.
Writing with clarity and intelligence makes readers feel capable; if they have to push
themselves a little to keep up, that's often just fine, particularly for important and
complex material.

### 5. Cover the Facts That Are Helpful

**Applies when:** curating scope for any guide (condition 2).
**Does not apply when:** the document type fixes the content (a reference table).

The priority is to be **helpful, not only factual**. Guides cover many facts, and may
include foundational sections devoted to facts — but the ultimate goal is to serve the
reader helpfully, and that determines which facts are relevant.
**Actionable knowledge rests on factual knowledge**: cover the foundations and context
that will support future learning.
Having a firm grasp of the mathematics of compound interest is not essential for every
investment decision, but it helps in so many situations that learning it early pays off.

### 6. Give Frameworks, Not Answers

**Applies when:** guidance is advisory and the right action is situational (condition
2). **Does not apply when:** the correct action is determinate — procedures, runbooks,
compliance steps. There, prescribe plainly; a framework where an instruction belongs is
evasion.

Many readers come with a question and expect an answer.
But for harder questions, simple answers are usually not what people need.
If you go to a lawyer and ask whether your new company should be a C Corp or an LLC, or
ask a doctor friend if you need back surgery, the expert will not just give you an
answer. On complex and important decisions, experts turn around and ask *you* the right
questions, to understand the real elements of the problem — then help you decide what's
right for your situation.

The most helpful guidance on important decisions is neither too assertive (fully
prescriptive, just telling you what to do) nor too passive (waiting for you to make
decisions you're not informed enough to make well).
It is only a mild over-generalization to say **"experts don't answer questions."** Like
the best experts, guides should **give people the frameworks to make their own
decisions.**

(Contrast search engines and AI assistants, which aim to give answers.
"Capital of Poland" has one; "Should my business be an LLC?" does not.)

### 7. Cover Controversy

**Applies when:** informed opinion genuinely varies on material questions.
**Does not apply when:** apparent "controversy" is consensus plus misconception — then
state the consensus and dispel the misconception.

When there is broad agreement, give recommendations.
When there is controversy, give an overview of key perspectives, reference the key
people or resources on different sides, and give rationale and context:

- Key points on different sides of an issue, with key citations.
- If there is broad agreement on some parts, give recommendations on those parts.
- Include the facts and frameworks the reader needs to make informed decisions.
  Often, experts can agree on a clearly articulated framework for making a decision
  even when they don't agree on a single recommendation.

### 8. Help People See What They Don't Know

**Applies when:** readers cannot yet name what they're missing (conditions 2 and 3).
**Does not apply when:** the reader's question is fully formed and specific.

One of the most helpful things you can share is a sense for what someone doesn't
know — indeed, what they didn't even know to look for.
The first goal of a guide is to give those new to a subject the broad outlines of what
they don't know.
The table of contents and section names should be a strong indication of scope and show
readers quickly what they are unfamiliar with and what they can hope to learn.
This is the beginning of fluency — and one reason great books are so helpful: an author
has spent years deciding what to cover.

Concrete forms: a table of contents with a surprising but helpful section; an
infographic that goes broader and deeper than most online visuals so even an expert
learns something; inclusion of dangers and pitfalls, not just facts and
recommendations; listing and dispelling common misconceptions.

### 9. Link or Cite Pretty Much Everything

**Applies when:** publishing for the open web with discretionary readers (condition 1).
**Does not apply when:** the document must be self-contained (printed matter, sealed
specs) — there, inline the essentials.

It's easy to write without adding links, but far more helpful to do the work of finding
the links that will help the reader.
Readers often don't know they want more information; a well-chosen link lets them
discover something unexpected and helpful.
Linking also gives credit where it's due.

Three kinds of links, in descending order of prominence:

- **Recommended links:** resources that are useful, widely known, or well-regarded,
  called out in the text with context — who wrote or produced the resource and why it's
  important. Famous books, definitive posts, and helpful tools.
- **Elaborative links:** more detail or context on something mentioned in passing —
  for example, Wikipedia articles on key concepts.
  These need no context beyond the inline link itself.
- **Pure citation links:** verifying a fact or sourcing a statement, in parentheses
  after the information being verified.

Working rules: for each paragraph, ask what the best links giving detail on it are; for
each link, ask whether there is a better one; prefer multiple citations when each adds
value — you are saving the reader several searches.
But link liberally, not indiscriminately: a laundry list of resources overloads the
reader, and including things of low value dilutes credibility.
Curate what matters and make it clear why what you chose made the cut.

### 10. Broker Attention Helpfully

**Applies when:** always — this is the economic statement of the Lucid principle.

The job of a guide is to **earn the trust** of readers by **brokering attention
helpfully**: helping readers allocate their time in the ways that are most effective.
Obtrusive ads, clickbait, and popups broker attention in ways that are not helpful;
readers notice over time and judge the value of media by whether it feels valuable.

Consequences for writers:

- The volume of words on a subject should roughly reflect its likely importance to
  readers.
- Topics covered should reflect demand — the information the audience really wants.
- Topics that are very important, even to a small group, should not be omitted.
- Including context and information from many sources saves the reader that research.
- Sometimes readers ask for one thing but need another: readers searching for a fad
  diet could benefit from nutrition fundamentals, so cover and connect both.
- Pitfalls and misperceptions are just as important as straightforward facts.

### 11. Address Multiple, Related Audiences

**Applies when:** several kinds of readers — sometimes on opposing sides — share the
topic (condition 3).
**Does not apply when:** the document has one reader or one role (most memos).

Know your audience, but don't narrow your audience.
A shared resource can be of extraordinary benefit to **multiple, related audiences** who
normally find themselves on different — sometimes opposing — sides: a guide to equity
compensation written for employers and employees, a guide to venture capital for
investors and entrepreneurs.

Why this works:

- It helps readers navigate where information asymmetry has made it difficult for
  people to communicate, relate, and empathize with the other side's motivations.
- It forces deeper discussion during writing: covering compensation with *both*
  employers and employees in mind drives the work to cover differences of opinion and
  express complexities more clearly for everyone.
- It is valuable for both sides to know they're operating with the same information —
  one side can even refer the other to it.

### 12. Intrigue Right Away

**Applies when:** readership is discretionary (condition 1).
**Does not apply when:** readers are captive (a required spec review) — there, lead
with the decision, not a hook.

Help people appreciate a guide's value *right away*: if you don't capture attention
quickly, you might not get it at all.
The **30-second rule**: does the work make people, no matter their experience level,
*lean in* right away?
Skimming top to bottom or through the table of contents, is there enough detail,
clarity, and logical structure that most people say "Oh, interesting"?
A beginner should be impressed with the depth but not too intimidated to start; an
expert should find details that earn their respect; readers of many types should find
"nuggets."

This is emphatically not clickbait ("5 easy steps to your first million!") and not
provocation or entertainment.
The aim is to organize the work to give visitors a clear sense of what's on offer, so
they know that if they keep reading, they will learn something of value.

## Voice

Four voices to avoid (they fail readers in different ways, and all of them fail the
respect test of guideline 4):

- **Marketing voice:** "This is awesome and contains expert tips you won't find
  anywhere else."
- **Know-it-all or paternalistic voice:** "We're experts and we have the answers.
  Follow our advice and you'll be fine."
- **It'll-be-easy voice:** "Once you learn these 17 tricks, it will be easy!"
- **Lifeless voice:** writing with no life or caring to it.
  Dry or needlessly boring writing helps no one.

(The first three are register failures scored under E1 Clarity; the fourth is the Tone
/ Reader Respect check.
See [practical-prose-guidelines.md](practical-prose-guidelines.md).)

## Answering Common Objections

Conceptions from other kinds of writing often do not apply to guides.
The objections below come up repeatedly in editorial work; the responses are the
working answers.

- **"We shouldn't cover X because it's controversial / too subjective."**
  Cover it — in a way that promotes understanding.
  Give the factual basis around the controversy: who argues what, and why?
  What do statistics or polls say?
  Do respected experts disagree, or are there mostly uninformed but popular
  misconceptions? Has opinion changed over time, and is it likely to change again?
  If you dig deep enough into the reasons for disagreement, you can often find a
  framework that reconciles them.
- **"We shouldn't cover X because it's just a fact you can look up."**
  Cover the facts that are relevant; it's the analysis and processing of those facts
  that leads to useful insight.
  Cover necessary facts in depth and reference tangential details with brief mentions
  and links.
- **"We shouldn't cover X because it's outside our scope."**
  For any such topic, the choices are (1) mention or reference it, (2) cover it in
  depth, or (3) ignore it completely.
  In cases of doubt, the right answer is usually (1) and sometimes (2), but rarely
  (3): if a reader is likely to expect something in the guide, address it — possibly by
  redirecting to the right framework or line of questioning.
- **"X is too technical for our readers, so we should omit it."**
  Hiding complexity contradicts the assumption that readers are 100% intelligent.
  The solution is structure: group technical content into clearly marked sections, or
  link to deeper material — remain the path to the deep material rather than sending
  readers elsewhere.
- **"We shouldn't link out, because we want people to stay."**
  Keeping people on a site is a concern for an impression-driven business.
  A guide's job is helping people find what they need as effectively as possible,
  wherever it lives.
- **"We link to X and Y, so we should link to everything like them."**
  No — curate.
  A laundry list of resources overloads the reader and dilutes credibility (see
  guideline 9).

## Callouts

Guides benefit from a consistent vocabulary of callouts for content that should stand
out from running prose.
The semantic categories (render them with whatever admonition mechanism the medium
provides):

| Category | Use for |
| --- | --- |
| Important | An important and often overlooked tip |
| Danger | A serious warning, where risks or costs are significant |
| Caution | A limitation, disadvantage, or quirk |
| Controversy | A topic where informed opinion varies significantly |
| Confusion | A common confusion or misunderstanding, such as confusing terminology |
| Technical | A technical point (arcane or academic, not essential) |
| New | New or recent developments |
| Incomplete | Expansion or improvement needed |

## Related Docs

- [practical-prose-guidelines.md](practical-prose-guidelines.md): the 20 dimensions all
  practical prose follows; this document extends them for the guide genre.
- [practical-prose-principles.md](practical-prose-principles.md): the seven principles;
  "broker attention helpfully" (guideline 10) descends from Lucid.
- [../runbooks/practical-guide-groundwork.runbook.md](../runbooks/practical-guide-groundwork.runbook.md):
  the pre-writing research protocol for scoping a guide.
- [practical-prose-bibliography.md](practical-prose-bibliography.md): sources, including
  the Holloway editorial-guidance lineage of this document.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
~~~

Open questions for review: (a) doc name — **decided: `writing-practical-guides.md`**
(clearer and matches the doc’s title); (b) whether the Callouts section belongs here or
in common-doc-guidelines (it is genre-agnostic); (c) whether guideline 5 should merge
into guideline 10 (kept separate above to preserve the “actionable knowledge rests on
factual knowledge” formulation).

### Chunk 3 — new runbook: `runbooks/practical-guide-groundwork.runbook.md`

The Groundwork section of the source (lines 627-806) is an operational questionnaire and
transfers nearly verbatim — it is also directly usable as an agent prompt.
Proposed frame, then the verbatim copy spec:

~~~markdown
# Runbook: Practical Guide Groundwork

Pre-writing research protocol for scoping a comprehensive practical guide.
Run it before outlining; the quality of a guide depends on this groundwork.
Useful as a human checklist or as an agent prompt (answer every question for the
proposed topic, then draft a candidate table of contents).

Groundwork consists of background and preparatory questions in three categories:

- **Scope:** what's included, what's not (and what is referenced but not covered in
  depth), and who makes up the multiple, related audiences.
- **Significance:** why the topic matters, where and how it is discussed, and its
  myriad connotations.
- **Research:** scenarios, questions, terminology, people, resources, and past works
  relevant to the topic.

[BODY: copy source §Scope, §Significance, §Questions and Entry Scenarios,
§Terminology, and §Change, Confusion, and Controversy verbatim]

## Consulting Diverse Experience and Expertise

[BODY: copy source §Consider Diverse Experience and Expertise verbatim — it is research
process, so it lives here rather than in the guidelines]

## Research Pitfalls

- Don't write much before exploring every other good resource out there: books,
  well-written fragments anywhere on the web, communities, and experts.
  Research all of it and form a perspective *before* finalizing scope and the table of
  contents.
- For pretty much every section, it's fair to ask: "Are we covering this better than
  every other page on the internet?"
- Searches also surface poor content and misconceptions, which improves coverage.
~~~

**Verbatim copy spec** (so no detail is lost in transcription):

- Source lines 650-677 (§Scope: the what-will-be-covered / entry-scenarios /
  who-is-this-for question tree, including the equity-compensation and nutrition
  examples) — copy unchanged.
- Source lines 678-777 (§Significance: all 13 numbered categories — author, individual,
  professional, academic, emotional/popular, decision-making value, news/public
  discourse, timeliness/historical, global, authorities, companies/financial, economic,
  community) — copy unchanged except dropping the `🚧` marker at line 785.
- Source lines 779-789 (§Questions and Entry Scenarios), 790-792 (§Terminology), 794-805
  (§Change, Confusion, and Controversy) — copy unchanged.
- Source lines 384-412 (§Consider Diverse Experience and Expertise) — copy unchanged
  into the consulting section.
- Source lines 1016-1034 (research pitfalls) — adapted as shown above.

### Chunk 4 — targeted merges (exact edits)

**4a. Bibliography** — add to `docs/practical-prose-bibliography.md` under “Functional
Value and Audience” (or a new “Guidance and Reference Works” subsection):

> - **Holloway, *Guidance for Writers, Contributors, and Editors*** (circa 2019).
>   Editorial guidance for comprehensive practical guides: dual-audience depth,
>   frameworks over answers, attention-brokering, multi-sided audiences.
>   The direct ancestor of [writing-practical-guides.md](writing-practical-guides.md),
>   and the origin of the “broker attention helpfully” phrasing in the Lucid principle.
>   Its recommended Markdown tooling (the atom-flowmark plugin) is the ancestor of
>   [flowmark](https://github.com/jlevy/flowmark).

**4b. Guidelines G1 Verifiability** — append one rule to the six existing rules in
`docs/practical-prose-guidelines.md` (after rule 6, line ~797):

> 7. **Links serve readers, not only verification.** Beyond citations, two further link
>    kinds carry weight in web-published documents: *recommended* links (resources
>    called out with context — who made them and why they matter) and *elaborative*
>    links (detail or context on a passing mention, needing no setup beyond the inline
>    link). Choose each link deliberately and prefer the best available source; a laundry
>    list of low-value links dilutes credibility and fails G3 Relevance.

**4c. Guidelines E1 Clarity** — add the four named voices as a teaching note in the E1
section (exact placement at review time, near the banned-register rule):

> Four named voice failures, useful as a self-check: *marketing voice* ("expert tips you
> won’t find anywhere else"), *know-it-all voice* ("follow our advice and you’ll be
> fine"), *it’ll-be-easy voice* ("just learn these 17 tricks"), and *lifeless voice*
> (dry writing with no care in it).
> The first three are register violations under this dimension; the fourth is the Tone /
> Reader Respect check.

### Chunk 5 — README and Layers updates (after Chunks 2-3 land)

1. **Layers table** (README line ~250): add one row after Rubric:
   > | **Genre: Guides** | [writing-practical-guides.md](docs/writing-practical-guides.md) | What does the comprehensive-guide genre additionally demand: 12 guidelines with applies-when caveats? |
   > and a Runbook-row mention of the groundwork runbook.
2. **Scope section**: one added sentence after the three key points:
   > Genre supplements extend these core layers where a genre demands more; the first
   > covers [comprehensive practical guides](docs/writing-practical-guides.md).
3. **Draft D’s folded list** gains one bullet:
   > - **Writing a comprehensive guide:**
   >   [writing-practical-guides.md](docs/writing-practical-guides.md) and the
   >   [groundwork runbook](runbooks/practical-guide-groundwork.runbook.md).
4. **Draft B** gains the lineage close (see Chunk 1).

### Chunk 6 — housekeeping

- Run the resource sync so the new docs ship in the wheel and appear in
  `pprose guidelines --list` / `pprose runbook --list` (devtools/sync_resources.py;
  verify with `make lint-check` and `tests/test_resources_sync.py`).
- Decide whether `docs/project/reviews-holloway-editorial-guidance.md` moves into
  `docs/project/reviews/` under the new naming convention.
- Track the chunks as beads under a new epic once this plan is approved (one bead per
  chunk, Chunk 5 blocked by 2-3, Chunk 6 by all).
- After everything lands, re-run the README eval and regenerate the screenshot cards if
  the README changed materially (Drafts A-E).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
