# Thinking Clearly in Writing

Version: v0.1 draft (2026-05-29)\
Joshua Levy (github.com/jlevy) with agent assistance

> *The great enemy of clear language is insincerity.* —George Orwell

This is a partial draft.
The pitfalls below are the core; the principles and bibliography sections are starting
points to be extended.

## What This Covers

Practical prose is judged by whether it helps a reader understand, decide, do, verify,
or maintain something.
The fastest way it fails is not bad grammar or a banned word.
It is *fuzzy thinking wearing the costume of clear thinking*: prose that produces the
surface signals of a worked-out idea—a coined term, clean parallelism, a crisp
abstraction, a confident register—without the thinking those signals are supposed to be
evidence of.

This failure is cheap to produce and easy to miss.
It is especially common in AI-generated text and in fast first drafts, where fluent form
is nearly free and a sentence can sound finished long before it is.
Such prose passes a skim and falls apart on a reread.

This document catalogs the recurring pitfalls, distills them into a review checklist,
and names the principles underneath.
It is a companion to [practical-prose-guidelines.md](../practical-prose-guidelines.md):
the guidelines score finished prose against twenty dimensions; this document targets the
thinking errors that produce the defects, so they can be caught before the prose is
scored.

## Common Pitfalls

Each pitfall below is a way the *form* of a thought can outrun the *thought*. The
examples are drawn from real edits and kept small but specific for clear illustration.

### 1. Reification: A Name Is Not an Explanation

Coining or applying a label, then leaning on it as though naming the thing accounted for
it. The work of saying what the thing *is* and *does* never happens; the sentences only
conjugate the new word.

> A guide coins the term *soft schema*, then “defines” it: “authoring is soft, adoption
> is soft, the body stays soft.”
> The reader still cannot say what *soft* does; the sentences only repeat the label in
> different grammatical slots.

Test: state the idea once without the coined term.
If it collapses, the term was carrying weight it never earned.

### 2. Invented Symmetry

Forcing items into a parallel set, a tidy taxonomy, or a round number because the shape
reads as organized, not because the subject has that shape.
Ralph Waldo Emerson’s “foolish consistency” applied to structure.

> “Authoring is soft. Adoption is soft.
> The body is soft.” Three clean parallel beats, but the items are not parallel:
> authoring is an activity, adoption is a process, and the body is a part of a document.
> The symmetry was added for rhythm, not found in the subject.

Test: are the parallel items actually the same kind of thing, and does the contrast
carry information? If not, drop the structure and state the one point that survives.

### 3. Ungrounded Abstraction

Stating a general principle with no concrete instance near it, so the reader cannot test
it or apply it. The abstraction may be correct and still fail, because it arrives before
the cases that would make it mean something.

> A section opens: “Automation, exactness, and structure are separate axes.”
> The claim may be sound, but stated cold and first it is a framework the reader cannot
> yet use. It earns its place only after a concrete contrast, such as a rigid schema
> versus one built up gradually, and an example.

Test: an abstraction should sit beside an instance.
Show first and name the pattern after, or state it and immediately ground it.

### 4. Hand-Waving: Describing an Example Instead of Giving One

Gesturing at a thing rather than producing it: describing an example instead of writing
one, or asserting a result instead of showing or checking it.
When the whole job of a passage is to demonstrate, a description of the demonstration is
a failure.

> An illustration block reads: “a short prose summary, followed by tables that mirror
> the data.” That is a *description* of an example, not an example.
> If the block exists to show the shape, write the actual summary; “imagine a summary
> here” defeats its only purpose.

A reliable tell is meta-narration around the example: “imagine that…”, “this would
typically contain…”, “this section reads like…”. It marks the spot where the writer
described the work instead of doing it.

### 5. Performative Rigor

Adding the trappings of care—hedges, caveats, defined terms, citations, structure—in a
way that signals thoroughness without making any claim more inspectable.
The rigor is worn, not done.

> A claim arrives wrapped in three hedges, a freshly coined term, and a footnote, and
> feels carefully made.
> Yet none of the scaffolding lets the reader verify anything; strip it and the same
> unsupported claim remains.

Test: each caveat, term, or citation should make some claim more checkable.
If removing it costs the reader nothing they could act on, it was decoration.

### 6. Failure to Compress

Elaborating past the actual idea, so packaging hides a sentence-sized core, or hides
that there is no core at all.

> “There are three things that make it soft…” (a paragraph) carries the same content as
> one sentence: “structure is added gradually, rather than imposed up front.”
> The paragraph was packaging around a sentence-sized idea.

Test: ask “what is the one plain sentence here?”
Often that sentence is the whole content, and writing it down reveals how much of the
rest was filler.

### 7. Building on the Not-Yet-Real

Treating the planned, hoped-for, or hypothetical as if it exists.
The prose builds structure around something absent, and the work looks more complete
than it is.

> A “common mistakes” list warns readers not to misuse a repair feature the tool does
> not ship. The warning is well-formed and describes nothing: until the feature exists,
> it makes the system look more finished than it is.

Test: separate what *is* from what *might be*. Describe the present state plainly; mark
the speculative as speculative.

### 8. Skipping the Self-Challenge

Accepting your first framing without asking the single question that kills most bad
claims: *is this actually true?* The cheapest and most neglected step in writing.

> “Authoring is soft” survives exactly until someone asks whether it is true.
> Authoring is neither soft nor hard; it is just authoring.
> One question dissolves the claim, so the question belonged before publishing, not
> after.

Test: read each load-bearing sentence as an adversary would and try to find the
counterexample. A claim you have not tried to break is not yet a claim.

### 9. Inertia: Inheriting a Framing Instead of Re-Deriving It

Especially in editing: the pull is to improve the wording in front of you rather than
ask whether that framing should exist.
Polishing inside an inherited frame perfects claims that should be cut.

> An editor smooths the line “the body stays soft” into something better-cadenced.
> But the sentence did not need smoothing; it needed deleting.
> Editing inside the inherited frame improved a claim that should not have been there.

Test: before refining a passage, ask whether it would be written this way from scratch.
If not, restructure or cut rather than polish.

### 10. Vagueness as Refuge

Staying fuzzy to avoid committing to a claim that could be wrong.
Vague words have the grammar of an assertion without exposing anything that could be
checked or refuted.

> “The parser is flaky on certain inputs” has the shape of a finding is a fig leaf for
> lack of understanding.
> “The parser truncates table field when the field contains a newline” can be confirmed,
> reproduced, and fixed.
> Vagueness that appears to be specific is always worse than explicit uncertainty.

Test: can the claim be confirmed or refuted as written?
If not, make it specific enough to be wrong.

## The Checklist

The pitfalls reduce to a single review pass, run on a finished draft and kept separate
from copy-editing: it audits the thinking, not the prose.
For each item, a “no” or a “can’t tell” marks a fix.

1. **Names:** Is every coined term explained without leaning on the term itself?
2. **Symmetry:** Is every parallel list or taxonomy real, not imposed for shape?
3. **Abstractions:** Does each general claim sit beside a concrete instance?
4. **Examples:** Is each example an example, not a description of one?
5. **Rigor:** Does each caveat, term, or citation make some claim more checkable?
6. **Compression:** Is this the simplest correct statement, with no packaging left?
7. **Reality:** Is anything described as existing that does not yet?
8. **Self-challenge:** Has each load-bearing claim been asked “is this actually true?”
9. **Inertia:** Was this re-derived, or only inherited and polished?
10. **Specificity:** Is each claim concrete enough to be wrong?

When in doubt on any one sentence, fall back to the three questions the whole list
compresses to: **Is it true?
Is it the simplest form?
Can the reader do something with it?** Most pitfalls above fail at least one.

This pass is mechanizable: read the draft, walk items 1–10, flag each “no” with a
location, then apply or propose the fix.

## Bibliography Review

Several works already cited in
[practical-prose-bibliography.md](../practical-prose-bibliography.md) bear directly on
this topic:

- **Orwell, “Politics and the English Language” (1946)** is the anchor: vague,
  pretentious language enables sloppy and dishonest thinking, and plain prose is a
  corrective discipline.
  Directly underwrites pitfalls 1, 3, and 10.
- **Williams, *Style: Toward Clarity and Grace* (1990)** on nominalization—recovering
  who-does-what-to-whom—is the sentence-level remedy for the abstraction and vagueness
  pitfalls.
- **Pinker, *The Sense of Style* (2014)** on the *curse of knowledge* explains why
  writers mistake their own fluency for the reader’s understanding, a root cause of
  hand-waving.
- **Zinsser, *On Writing Well* (1976)** on clutter is the practical companion to the
  compression pitfall.
- **Popper, *Conjectures and Refutations* (1963)** and the calibration entries (Tetlock,
  Kahneman) underwrite the self-challenge principle.
- **Thomas & Turner, *Clear and Simple as the Truth* (1994)** frames classic style as
  prose presenting something the writer has genuinely seen: the opposite of performative
  rigor.

Candidate additions specific to the “form outruns thought” theme, not yet in the
bibliography:

- **Feynman, “Cargo Cult Science” (1974).** The source of the “do not fool yourself”
  principle the guidelines already invoke; the canonical statement of intellectual
  honesty as a personal discipline.
  Strong candidate for the Epistemic Calibration section.
- **Frankfurt, *On Bullshit* (2005).** A precise account of speech produced without
  regard to whether it is true: the philosophical core of performative rigor and
  reification. Short, widely cited, and directly on theme.
- **Sword, *Stylish Academic Writing* (2012)** is already cited; worth re-tagging here
  as evidence that jargon and inflation are choices, not requirements of a genre.

Open question for a later pass: whether to add a treatment of LLM-specific failure modes
(fluent-but-empty generation, confident hallucination, symmetry bias) once a citable
source exists, rather than relying on field observation alone.

## Related Docs

- [practical-prose-principles.md](../practical-prose-principles.md): the seven
  principles this document draws on (especially Essential, Lucid, Truthful, Verifiable).
- [practical-prose-guidelines.md](../practical-prose-guidelines.md): the twenty scored
  dimensions; this document targets the thinking errors upstream of those defects.
- [practical-prose-bibliography.md](../practical-prose-bibliography.md): full citations
  for the works named above.
- [common-doc-guidelines.md](../common-doc-guidelines.md): general style, organization,
  and formatting.

<!-- This document follows common-doc-guidelines.md.
Review guidelines before editing.
-->
