---
name: pprose-copy-edit
description: Copy-edit a Markdown document for language and formatting (the Expression dimensions); modifies the doc. A superset of pprose-common-edit. Use when asked to copy edit, proofread, polish, tighten, rewrite, or line edit.
---
# Copy Edit

This is an apply skill: it may modify the target document. It is a **superset of
`pprose-common-edit`**: it applies the common documentation substrate *and* the
Expression dimensions (E1–E6: clarity, coherence, concision, organization, consistency,
formatting) of the Practical Prose guidelines. It stops short of the substantive
dimensions — for a full all-dimension editorial pass that also writes an editorial
review, use `pprose-full-edit`.

## Inputs

- Path to one Markdown document.
- Optional edit brief, audience, and tolerance for heavier rewrites.

## Steps

1. Run `pprose shortcut shortcut-copy-edit` and follow it.
2. Apply the common substrate: `pprose guidelines common-doc-guidelines`.
3. Apply the Expression dimensions (E1–E6) from
   `pprose guidelines practical-prose-guidelines` (§Expression Dimensions).
4. Audit the document, track issues (project issue/bead tooling when available, else the
   agent's to-do/checklist), and apply edits directly.
5. Preserve factual meaning, claim strength, citations, and intentional voice. Do not
   edit the substantive dimensions (Purpose, Grounding, Reasoning, Judgment); if those
   need work, note it and recommend `pprose-full-edit`.
6. Re-scan the diff for regressions before reporting.

## Output

Report the changed file, the Expression issue classes fixed, and any substantive
(Purpose / Grounding / Reasoning / Judgment) issues you noticed but did not edit.
