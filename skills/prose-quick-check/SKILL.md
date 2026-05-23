---
name: prose-quick-check
description: Audit a practical document against the 20-dimension checklist; read-only. Use when asked to audit, review, self-audit, quality-check, or pre-publish-check.
---
# Quick Check Practical Prose

This is a read-only audit skill: do not modify the target document.

Use it when the user wants findings, risks, or a pre-publish quality check rather than
an edit pass.

## Inputs

- Path to one practical prose document.
- Optional scope or risk level from the user.

## Steps

1. Read `../../shortcuts/practical-prose-quick-checklist.md`.
2. Skim the target for purpose, scope, and output shape.
3. Run the checklist across Purpose, Expression, Grounding, Reasoning, and Judgment.
4. Separate deterministic issues from judgment calls.
5. For high-stakes documents, keep lint, claim, reasoning, and purpose passes separate.

## Output

Return findings ordered by severity with file and line references where practical.
Include no rewrite unless the user asks for a follow-up edit pass.
