---
title: Review Document
description: Read-only tiered editorial review; report what a common edit, a copy edit, and a full substantive pass would each change, with no edits to the source and no numeric scores
date: 2026-06-09
status: active
category: documentation
author: Joshua Levy (github.com/jlevy) with agent assistance
---
# Review Shortcut

A **read-only** editorial review.
It runs the same audit passes as `pprose shortcut shortcut-full-edit`, but it **changes
nothing in the source and assigns no scores**: it produces a single tiered review
document. Use it for feedback or an edit plan, not to apply edits (use the copy-edit or
full-edit playbooks for that), to score a document (use
`pprose runbook practical-prose-eval-single`), or to compare versions (use
`pprose runbook practical-prose-eval-compare`).

## What It Produces

One editorial-review side document (default `<source-basename>.review.md`) whose
findings are sorted into three tiers of edit depth, so the author can see at a glance
how much work each layer is and what needs their judgment.

## The Three Tiers

- **Tier 1, common edit (safe, meaning-preserving).** What a `pprose-common-edit` pass
  would fix: organization, structure, writing style, Markdown formatting, links,
  headings, lists, frontmatter, and footer.
  Read `pprose guidelines common-doc-guidelines`; use `pprose metrics` for the
  deterministic signals.
- **Tier 2, copy edit (language and formatting; no meaning change).** What a
  `pprose-copy-edit` pass would apply: the Expression and Form dimensions (E1-E3, F1-F3:
  clarity, coherence, concision, organization, consistency, formatting) of
  `pprose guidelines practical-prose-guidelines`.
- **Tier 3, full feedback (substantive; author judgment).** The judgment-bearing
  dimensions: Purpose (P1-P4), Reasoning (R1-R4), Grounding (G1-G3), and Judgment
  (J1-J3): anything that would change factual meaning, claim strength, scope, cited
  evidence, or the line of argument.
  Flag these as suggested fixes; never present them as already decided.

## Procedure

1. **Orient.** Read the document for task, scope, audience, risk level, and output
   shape. Read `pprose guidelines practical-prose-guidelines`; for the review-time
   questions and applicability-by-risk-level use
   `pprose shortcut practical-prose-quick-checklist`.

2. **Run the audit passes** from `pprose shortcut shortcut-full-edit` §Procedure (lint,
   Expression, reasoning audit, claim audit, purpose audit) but **apply nothing**. Use
   `pprose metrics` for the deterministic lint signals, and check every quantitative
   claim against its cited source in the claim audit.

3. **Sort every finding into Tier 1, Tier 2, or Tier 3** by the mapping above.
   When a defect could sit in two tiers, file it at the **shallowest tier that fully
   fixes it** (a wording change that also happens to clarify an argument is Tier 2, not
   Tier 3).

4. **Write the tiered review** (structure below) to `<source-basename>.review.md` beside
   the source, or to a user-given path.
   **Make no changes to the source.
   Assign no scores**; that is what `pprose-eval` is for.

5. **Report** the review path, the count of findings per tier, and the recommended next
   action: run `pprose-copy-edit` to apply Tiers 1-2 automatically; Tier 3 is for author
   judgment. If the user actually wanted a scored rubric, point them to `pprose-eval`; to
   compare versions, `pprose-compare`.

## Tiered-Review Structure

Write the review as Markdown with this shape:

~~~markdown
# Review: <document title>

## Scope and Context

Document, purpose, audience, and risk level; what this review covers. State plainly:
this is read-only; no edits were made and no scores assigned.

## Strengths

Concrete, specific strengths worth keeping, by dimension where useful. Not generic
praise.

## Tier 1: Common Edit (Formatting and Structure)

Findings a common-edit pass would fix. For each: a location pointer (line range,
§heading, or quoted phrase) and the fix. Safe and meaning-preserving.

## Tier 2: Copy Edit (Expression and Form)

E1-E3 and F1-F3 findings a copy-edit pass would apply. For each: the dimension
(e.g. E3 Concision), a location pointer, and the change. Language and formatting only.

## Tier 3: Full Feedback (Substantive; Author Judgment)

Purpose, Reasoning, Grounding, and Judgment issues to weigh. For each: the dimension
(e.g. G2 Factuality), a location pointer, the concrete suggested change, and why it
matters (the reader outcome at stake). Order by severity. A flagged item may be a
**justified deviation** rather than a defect: if the author documented the rule set
aside, the reader outcome it serves, and the risk introduced, note it as accepted (see
*Justified Deviations* in `pprose guidelines practical-prose-rubric`).

## Next Steps

How to act on this review: run `pprose-copy-edit` to apply Tiers 1-2 automatically;
Tier 3 needs author judgment. For a scored 1-5 rubric use `pprose-eval`; to compare
versions use `pprose-compare`.
~~~

Keep every finding grounded in a specific location or quoted phrase.
Assign no numeric scores: tiers describe edit depth, not quality grades.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
