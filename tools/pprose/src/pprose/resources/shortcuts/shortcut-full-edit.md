---
title: Full Edit Document
description: Deep editorial pass across all 20 Practical Prose dimensions; apply the safe fixes, flag substantive issues, and write an editorial-review side document
category: documentation
author: Joshua Levy (github.com/jlevy) with agent assistance
---
# Full-Edit Shortcut

The deepest edit tier: a systematic pass across all six groups and 20 dimensions of
`pprose guidelines practical-prose-guidelines`. A superset of the
`pprose shortcut shortcut-copy-edit` (common substrate + Expression and Form); full-edit
adds the substantive dimensions and produces an editorial review.

## What It Produces

1. **Edited document:** safe fixes applied in place (unless run audit-only).
2. **Editorial review:** a side document for the author or other editors (structure
   below).

## Apply vs. Flag

- **Auto-apply** (safe, meaning-preserving): the common substrate and the Expression and
  Form dimensions (E1-E3, F1-F3): formatting, clarity wording, banned-register words,
  concision, consistency, organization, broken links.
  Apply a fix only if you are certain it preserves meaning, claim strength, and
  citations.
- **Flag, do not silently rewrite** (substantive, judgment-bearing): Purpose, Reasoning,
  Grounding, and Judgment issues, meaning anything that would change factual meaning,
  claim strength, scope, cited evidence, or the line of argument.
  Record these in the review as suggested fixes for the author.

## Procedure

1. **Orient.** Read the document for task, scope, audience, risk level, and output
   shape. Read `pprose guidelines practical-prose-guidelines`; for the review-time
   questions and applicability-by-risk-level, use
   `pprose shortcut practical-prose-quick-checklist`.

2. **Run the passes by group** (the four audit passes in
   `pprose shortcut practical-prose-quick-checklist` §The Four Audit Passes, required
   for high-stakes docs; keep them separate):
   - **Lint pass:** F1 Organization, F2 Consistency, F3 Formatting, E1 banned-register
     and vague-word checks, plus the lexical catalog in
     `pprose guidelines ai-prose-corrections`. Use `pprose metrics`. *Auto-apply.*
   - **Expression pass:** E1-E3 clarity, coherence, concision, plus the structural
     patterns and attention flags in `pprose guidelines ai-prose-corrections` (false
     agency, negative listing, fragments, adverb density).
     *Auto-apply.*
   - **Reasoning audit:** R1-R4, J2 Fairness, J3 Robustness: assumptions, mechanisms,
     counter-evidence, parsimony, alternative lenses.
     *Flag.*
   - **Claim audit:** G1 Verifiability, G2 Factuality, G3 Relevance: every quantitative
     claim against its cited source; re-run calculations.
     *Flag.*
   - **Purpose audit:** P1-P4, J1 Calibration: output shape vs.
     task, scope, skim-recoverability.
     *Flag structural moves; apply small reorders.*

3. **Track issues** with project issue/bead tooling when available (an epic plus one
   child per fix when there are more than 5), else the agent’s to-do/checklist.

4. **Apply** the auto-applicable fixes.
   Preserve factual meaning, claim strength, citations, and intentional voice.

5. **Write the editorial review** (structure below) to `<source-basename>.review.md`
   beside the source, or to a user-given path.

6. **Verify.** Re-scan the diff for regressions; confirm no applied edit changed
   meaning; close or update any issues created.

7. **Report** the edited file, the review file, the issue classes fixed, and the count
   of flagged items left for the author.

## Editorial-Review Structure

Write the review as Markdown with this shape:

~~~markdown
# Editorial Review: <document title>

## Scope and Context

Document, purpose, audience, and risk level; what this review covers. State plainly what
was edited directly versus what is flagged below for author judgment.

## Strengths

Concrete strengths, by dimension where useful: what the document does well and should
keep. Specific, not generic praise.

## Weaknesses

Organized by group (Purpose, Expression, Form, Reasoning, Grounding, Judgment). For each issue:
the dimension (e.g. G2 Factuality), a location pointer (line range, §heading, or quoted
phrase), and what is wrong.

## Suggested Fixes for Authors and Editors

The substantive items not auto-applied. For each: dimension, location, the concrete
suggested change, and why it matters (the reader outcome at stake). Order by severity.

## Edits Applied

A short summary of the classes of fix applied directly (lint, clarity, concision,
formatting, …) so the author can scan the diff with context.
~~~

Keep the review grounded in specific locations and claims.
A flagged weakness may be a **justified deviation** rather than a defect: if the author
documented the rule set aside, the reader outcome it serves, and the risk introduced,
note it as accepted (see *Justified Deviations* in
`pprose guidelines practical-prose-rubric`).

## Audit-Only Mode

If the user asks to review without editing, run passes 1-2 and 5-7 but make no changes
to the source: produce the editorial review (and findings) only, and say so in the
report.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
