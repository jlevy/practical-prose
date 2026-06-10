# Review: Holloway Editorial Guidance vs. Practical Prose

## Scope and context

- **Source document:** `~/wrk/github/editorial-guidance/README.md` ("Guidance for
  Writers, Contributors, and Editors"), written for Holloway Guides circa 2019-2020.
- **Question:** which portions belong in Practical Prose, in what form (new doc vs.
  blended into the existing principles/guidelines), and with what applicability caveats.
- **Reviewed against:** practical-prose-principles.md (7 principles),
  practical-prose-guidelines.md (20 dimensions), the rubric, and the bibliography.

The source is a different *kind* of document from the practical-prose layers: it mixes
genre definition (what a guide is), authoring strategy (the 12 guidelines), research
protocol (Groundwork), editorial process (roles, milestones), and product documentation
(the Holloway Reader).
Only some of these layers transfer; the ones that do are valuable precisely because they
cover ground the 20 dimensions deliberately do not.

## The key distinction: guidance writing is a subgenre

Practical prose is writing that helps a reader understand, decide, do, or verify.
The Holloway doc is about a narrower thing: **comprehensive guides that help readers
navigate complex, high-stakes topics** — pedagogical-navigational reference works for
multi-level, multi-sided audiences, built for recurring use.
Most of its distinctive advice presumes that genre: discretionary readership (the reader
can leave), situational variability (no single right answer), information asymmetry
between audiences, and long shelf life.

That presumption is exactly why these guidelines push editors somewhere they don’t
usually go — and exactly why each needs an “applies when” caveat if imported.
A runbook author told to “give frameworks, not answers” would write a worse runbook.

## Mapping: the twelve guidelines (plus one)

| # | Holloway guideline | Status vs. practical prose | Where it maps |
| --- | --- | --- | --- |
| 1 | Make deep coverage accessible | **Novel** as a stated aim (deep *and* engaging; impress expert and beginner at once) | Touches P4 Depth, E1 Clarity; the dual-audience tension is unstated in PP |
| 2 | Earn the respect of experts first | **Novel** — a priority ordering (credibility before accessibility, never the reverse) | No PP equivalent; relates to the Truthful principle’s spirit |
| 3 | Start from the beginning | **Mostly novel** — curse-of-knowledge, foundations-first ordering, no circular or out-of-order definitions | F1 rule “order the task requires” gestures at it; the pedagogy is new |
| 4 | 100% intelligent and 100% ignorant | **Novel** — the single most quotable heuristic; includes the anti-condescension corollary | Aligns with Humane and the Tone/Reader-Respect modifier |
| 5 | Cover the facts that are helpful | **Covered** in spirit ("helpful, not only factual" ≈ G3 Relevance + P1 Suitability) | Keep the formulation “actionable knowledge rests on factual knowledge” |
| 6 | Consider diverse experience and expertise | **Process guidance** (whom to consult), not document quality | Research-protocol material; faint J2 Fairness connection |
| 7 | Give frameworks, not answers | **Novel and distinctive** — “experts don’t answer questions”; guidance neither fully prescriptive nor passive | No PP home; the most important single import |
| 8 | Cover controversy | **Half-covered** — J2 Fairness scores the result; Holloway gives the authoring decision rule (agreement → recommend; controversy → perspectives + framework + citations) | Import the decision rule |
| 9 | Help people see what they don’t know | **Novel** — unknown unknowns as a coverage goal; the TOC as a map of the reader’s ignorance | P3 Breadth covers case classes, not this purpose |
| 10 | Link or cite pretty much everything | **Half-covered** — G1 treats links as evidence; Holloway adds the service taxonomy (recommended / elaborative / pure-citation links) and curation duty | Import the taxonomy; note both docs warn against laundry lists |
| 11 | Broker attention helpfully | **Already migrated** — the phrase sits inside the Lucid principle (#4) verbatim; P4’s “section depth matches importance” carries the allocation rule | Credit the lineage; the demand-aware coverage angle is still new |
| 12 | Address multiple, related audiences | **Novel** — shared reference for opposing sides (employers/employees), with the information-asymmetry rationale | PP assumes a mostly singular reader |
| + | Intrigue right away (30-second rule) | **Novel** — lean-in test, “nuggets,” explicitly not clickbait | Engagement is deliberately unscored in PP; belongs in genre guidance, not the rubric |

Also valuable outside the twelve:

- **Groundwork** (scope / significance / entry-scenarios questionnaires): a pre-writing
  research protocol. P2 Scope covers *declaring* scope in the document; Groundwork covers
  *deciding* it. The entry-scenarios device (5-10 scenarios, including misguided ones)
  and the 13-category significance questionnaire are operational gold — runbook
  material, not guideline material.
- **Concerns and Pitfalls**: objection-response pairs ("it’s too controversial," “too
  technical,” “out of scope,” “don’t link out”) — the editor-facing counters that do the
  “pushing editors in directions they don’t typically go” work.
  These should survive intact; they are the most battle-tested part of the source.
- **Voice pitfalls** (marketing voice, know-it-all voice, it’ll-be-easy voice, lifeless
  voice): aligns with E1’s banned register and the Tone modifier; the four named voices
  are a better teaching device than a word list.
- **Block-style taxonomy** (important / danger / caution / controversy / confusion /
  technical / new / incomplete): a callout vocabulary for admonitions.
  Product-specific emoji aside, the *semantic categories* transfer to any Markdown
  admonition guidance.

## What should not be imported

- **Roles and Working Together, Process milestones**: Holloway organizational process.
- **Tools**: dated (Google Docs/Atom-era), though the atom-flowmark plugin is a nice
  ancestry note for flowmark.
- **The Holloway Reader**: product documentation.
- **Iterative publishing framing**: tied to the Holloway product thesis; the
  built-to-improve idea survives in PP’s Maintainable principle already.

## Recommendation

A blend would be wrong: most of the novel material is authoring strategy for a genre,
not scoreable document properties, and forcing it into the 20-dimension structure would
break the tight principles ↔ guidelines ↔ rubric triple.
Instead, four moves:

1. **New genre-supplement doc** — `docs/writing-practical-guides.md` ("Writing Practical
   Guides"), a sibling layer that builds on the practical-prose layers the way they
   build on common-doc-guidelines.
   Contents: the ~9 novel guidelines (1, 2, 3, 4, 7, 8-rule, 9, 12, 30-second rule), the
   link taxonomy, the voice pitfalls, the objection-response pairs, and the callout
   taxonomy. **Each guideline carries an explicit applicability header** (see caveat
   mechanism below). Modernized: Holloway product references removed; agent-era framing
   added (these principles are as useful for prompting an agent to draft a guide as for
   briefing a human writer).
2. **New groundwork runbook or shortcut** — the scope / significance / entry-scenarios /
   terminology / controversy questionnaires as an operational pre-writing protocol
   (`runbooks/` or a `guide-groundwork` shortcut).
   This is separately useful as an agent prompt: an agent can run the questionnaire
   against a topic before outlining.
3. **Small merges into existing layers:**
   - Bibliography: add the Holloway editorial-guidance doc and editorial-principles URL
     as a source tradition; note the broker-attention lineage into Lucid and the
     atom-flowmark → flowmark ancestry.
   - Guidelines G1/F1: the recommended / elaborative / citation link taxonomy.
   - E1 / Tone modifier: the four named voice pitfalls as teaching examples.
4. **No rubric changes now.** The rubric’s anchors already scale by “purpose, audience,
   genre, and risk level,” so the genre doc plugs into an existing lever.
   If guide evals become common, a `guide` scope-class can join the existing five
   (status / brief / memo / deep_research / design_doc) later — separate decision.

### Caveat mechanism

Follow the source’s own instinct ("Not all books should follow all the recommendations
here") but make it structural.
Each guideline in the new doc opens with a two-line applicability header:

> **Applies when:** advisory content under situational variability — the reader’s right
> action depends on facts the writer cannot know.
> **Does not apply when:** the correct action is determinate (runbooks, procedures,
> compliance steps) — there, prescribe plainly.

(That example is Frameworks-Not-Answers; Experts-First applies to public reference works
more than internal memos; Multiple-Audiences applies to shared references, not
single-reader documents; the 30-second rule applies to discretionary readership, not
captive readers of a spec.)
The doc opens by defining the guide genre — essentially the source’s “What Makes a
Guide?” list, trimmed of product context — so the caveats have something to point at.

## Does this change the earlier README advice?

Mostly it strengthens it:

- **Draft B ("How Is This Different?")** gains a credibility line: these principles come
  from years of editorial practice on published guides, not from prompt engineering.
  The Personal Note already gestures at Holloway; a genre doc makes that backstory
  load-bearing.
- **Draft D (consolidate the maps)** becomes more important, not less: a new layer row
  and a new runbook will grow the Layers table, so the README can’t afford four
  overlapping routing sections.
- **README Scope section**: once the genre doc exists, add one sentence noting that
  genre supplements (starting with practical guides) extend the core layers — this also
  pre-answers “does every rule apply to every document?”, which the caveat mechanism
  handles at the doc level.
- **One reframe:** the strongest principles here (frameworks-not-answers, 100%/100%,
  unknown unknowns) are also good *agent* directives.
  The genre doc should be written to serve both audiences from the start — which is the
  project’s whole thesis applied to its own content.

## Suggested next steps

1. ~~Decide the genre doc’s name~~ — decided: `writing-practical-guides.md`.
2. Draft `writing-practical-guides.md` from the mapping above (novel items only, with
   applicability headers).
3. Draft the groundwork runbook/shortcut from the questionnaires.
4. Make the small merges (bibliography, link taxonomy, voice pitfalls).
5. Revisit the README Scope/Layers wording once 1-3 land.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
