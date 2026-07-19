---
name: pprose-common-edit
description: Apply the common Markdown documentation guidelines and required footer to durable docs; modifies docs. Use whenever creating, editing, reviewing, or reorganizing Markdown, including READMEs, guides, specs, plans, runbooks, and agent instructions, unless the task is explicitly read-only. Also use when asked to tidy, clean up, conform, fix formatting or structure, or add the footer.
---
# Common Edit

This is the basic, universal edit tier (an apply skill: it may modify the target
documents).
It applies the common documentation guidelines to almost any durable Markdown
document, workflow, or repo, whether or not it is a Practical Prose artifact.

Before acting, read the bundled
[common-doc-guidelines.md](references/common-doc-guidelines.md) in full.
The reference is part of this skill; the `pprose` CLI is not required.

For focused removal of AI-writing tells use `pprose-de-slop`; for a deeper
language-and-formatting pass (the Expression and Form dimensions, including the de-slop
audit) use `pprose-copy-edit`; for a full all-dimension editorial pass use
`pprose-full-edit`. Each tier is a superset of the one before, with `pprose-de-slop`
folded in from copy-edit up.

## Inputs

- Paths to one or more Markdown documents.
- Optional scope note from the user, such as “format only” or “make all obvious fixes.”

## Steps

1. Read `references/common-doc-guidelines.md` completely before editing.
2. Inspect the target against organization, structure, writing style, Markdown
   formatting, links, headings, lists, frontmatter, and footer rules.
3. Apply fixes directly to the document while preserving its intended content and voice.
4. Ensure every governed document ends with exactly one guideline footer, unless the
   guideline’s impracticality exception applies.
5. Run the project’s configured Markdown formatter when one exists.
6. Re-read the diff and check that no edit changed factual meaning.

## Output

Report the changed file, the main issue classes fixed, and any rule you intentionally
left alone.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
