# Editorial Review: Writing Comprehensive Practical Guides

## Scope and Context

Reviewed [docs/writing-practical-guides.md](../writing-practical-guides.md) against
[docs/project/reviews-holloway-editorial-guidance.md](reviews-holloway-editorial-guidance.md)
and the checked-out Holloway source document from
`https://github.com/feynmanlabs/editorial-guidance`.

The requested scope was to adapt older Holloway guide-writing guidance into Practical
Prose and make clear that the result is guidance for writing comprehensive practical
guides, not all practical documents.
I edited the guide supplement directly, folded the groundwork research protocol into it
as a Groundwork section, and flagged remaining judgment calls below.

Note: the user-referenced path `docs/project/holloway-editorial-guidance.review.md` does
not exist in this checkout.
The current equivalent appears to be
[docs/project/reviews-holloway-editorial-guidance.md](reviews-holloway-editorial-guidance.md).

## Strengths

- **Purpose:** The draft already preserved the key genre distinction: comprehensive
  practical guides are different from runbooks, specs, memos, and short practical docs.
- **Expression:** The Holloway heuristics survive in teachable form, especially “100%
  intelligent and 100% ignorant,” “frameworks, not answers,” and “broker attention
  helpfully.”
- **Form:** The applies-when / does-not-apply headers are the right mechanism for
  preventing genre rules from leaking into the all-purpose Practical Prose layer.
- **Judgment:** The draft correctly treats controversy as something to contextualize,
  not avoid.

## Weaknesses

- **P1 Suitability:** The original title and opening could still be read as general
  practical-prose guidance.
  The edit now says explicitly that this is a guide-genre supplement only.
- **P3 Breadth:** The Holloway “consider diverse experience and expertise” rule was
  absent from the draft.
  Because it is mostly process guidance, I added it as a groundwork/review-input section
  rather than as another numbered quality rule.
- **F1 Organization:** The Related Docs section referenced a planned runbook that did
  not exist, leaving the package integration incomplete.
- **Maintainability:** The guide exists both in `docs/` and bundled package resources;
  the package copy must be generated from the canonical doc rather than edited by hand.

## Suggested Fixes for Authors / Editors

- **Create guide-specific eval behavior only after usage proves the need.** The rubric
  can already evaluate guides through the existing dimensions.
  A future `guide` `scope_class` should wait until guide evals need distinct density or
  structure thresholds.
- **Keep the guide supplement out of common-doc-guidelines.** The most memorable guide
  rules are tempting to globalize, but several would harm procedures, specs, and
  decision memos.
- **Consider a future shortcut for guide drafting.** The guide’s Groundwork section
  handles pre-writing research.
  A later shortcut could route agents through groundwork, outline, guide draft, and
  expert review.

## Edits Applied

- Retitled and opened the guide supplement as guidance for **comprehensive practical
  guides**, not all practical prose.
- Folded the groundwork research protocol into the guide supplement as a Groundwork
  section (scope, entry scenarios, audiences, significance, questions, terminology,
  controversy), including a review-input subsection for consulting across diverse
  experience and expertise, rather than a standalone runbook as originally planned.
- Updated README routing so the guide supplement is discoverable.
- Merged reusable Holloway link and voice guidance into
  `docs/practical-prose-guidelines.md`.
- Added the Holloway source to `docs/practical-prose-bibliography.md`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
