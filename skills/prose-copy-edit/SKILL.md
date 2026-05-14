---
name: prose-copy-edit
description: Copy-edit a Markdown document against Practical Prose style; modifies the doc. Use when asked to copy edit, proofread, polish, tighten, rewrite, or line edit.
---
# Copy Edit Practical Prose

This is an apply skill: it may modify the target document.

Use it when the user wants the document improved, not only audited.

## Inputs

- Path to one Markdown document.
- Optional edit brief, audience, and tolerance for heavier rewrites.

## Steps

1. Read `../../shortcuts/shortcut-copy-edit.md`.
2. Read `../../docs/common-doc-guidelines.md`.
3. For Practical Prose artifacts, also consult
   `../../docs/practical-prose-guidelines.md` only for sections relevant to the edit.
4. Audit the document, track issues, and apply edits directly.
5. Use external issue or bead tooling only when it is available in the project; otherwise
   track issues with the agent's normal to-do or checklist tooling.
6. Preserve factual meaning, claim strength, citations, and intentional voice.
7. Re-scan the diff for regressions before reporting.

## Output

Report the changed file, the main issue classes fixed, and any unresolved issues that
need author judgment.
