---
name: prose-full-edit
description: Full editorial pass over a practical document across all 20 Practical Prose dimensions; modifies the doc AND writes an editorial-review side document. A superset of prose-copy-edit. Use when asked for a deep or full edit, an editorial review, a substantive edit, or a strengths-and-weaknesses review with suggested fixes.
---
# Full Edit

This is the deepest edit tier (an apply skill: it may modify the target document) and a
**superset of `prose-copy-edit`**. It works the document across all five groups and 20
dimensions of the Practical Prose guidelines (Purpose, Expression, Grounding, Reasoning,
Judgment), and it writes an **editorial-review side document** with strengths,
weaknesses, and suggested fixes for the author or other editors.

Apply-vs-flag: auto-apply the safe Expression and formatting fixes; **flag** substantive
Purpose / Grounding / Reasoning / Judgment issues in the review rather than silently
rewriting — never change factual meaning, claim strength, scope, or citations.

## Inputs

- Path to one practical-prose document.
- Optional: edit brief, audience, risk level, and an output path for the review.
- Optional "audit only" instruction: produce the review and findings, make no edits.

## Steps

1. Run `pprose shortcut shortcut-full-edit` — the playbook, including the
   editorial-review structure.
2. Follow it: per-group passes against `pprose guidelines practical-prose-guidelines`,
   apply the safe fixes, flag the substantive ones, and write the editorial review.

## Output

- The edited document (unless run audit-only).
- The editorial-review side document (default `<source-basename>.review.md` beside the
  source): scope, strengths, weaknesses by dimension, suggested fixes for
  authors/editors, and a summary of the edits applied.
