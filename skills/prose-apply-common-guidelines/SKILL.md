---
name: prose-apply-common-guidelines
description: Apply common Markdown documentation guidelines; modifies the target doc. Use when asked to tidy, clean up, conform, fix formatting, or add the footer.
---
# Apply Common Documentation Guidelines

This is an apply skill: it may modify the target document.

Use it for general Markdown documentation cleanup, even when the target is not a
Practical Prose evaluation artifact.

## Inputs

- Path to one Markdown document.
- Optional scope note from the user, such as "format only" or "make all obvious fixes."

## Steps

1. Read `../../docs/common-doc-guidelines.md`.
2. Inspect the target document against organization, structure, writing style, Markdown
   formatting, links, headings, lists, frontmatter, and footer rules.
3. Apply fixes directly to the document while preserving its intended content and voice.
4. Ensure the required guideline footer is present when the document is part of this
   repo's durable documentation.
5. Re-read the diff and check that no edit changed factual meaning.

## Output

Report the changed file, the main issue classes fixed, and any rule you intentionally
left alone.
