---
name: pprose-de-slop
description: Remove AI-writing tells and formulaic LLM prose while preserving meaning and voice; modifies the target. Use when asked to de-slop, de-slopify, humanize, remove AI tells, make writing sound less AI-generated or less machine-like, or fix hollow emphasis, canned transitions, false agency, negative parallelism, dramatic fragments, generic conclusions, marketing register, and reflexive three-item lists.
---
# Remove AI-Writing Tells

This is a focused apply skill: it edits prose to remove documented LLM-register tells
without installing a different authorial voice.
It may modify the target document.

Before acting, read the bundled
[ai-prose-corrections.md](references/ai-prose-corrections.md) in full.
The reference is part of this skill; the `pprose` CLI is not required.
For a broader language-and-formatting pass that includes this audit, use
`pprose-copy-edit`.

This skill improves prose quality.
It does not promise detector evasion, hide authorship, or manufacture signs of human
composition.

## Inputs

- One or more prose documents or clearly identified passages.
- Optional audience, genre, voice sample, and tolerance for heavier rewriting.

## Steps

1. Read `references/ai-prose-corrections.md` completely before editing.
2. Read the full target and identify its purpose, audience, genre, intended voice, and
   local authoring rules.
3. Audit in two passes:
   - Find lexical and structural patterns the reference marks for correction.
   - Inspect attention flags for repetition or density; do not treat them as banned
     words or constructions.
4. Rewrite confirmed tells by naming the actor, claim, relationship, mechanism,
   quantity, or consequence the original obscured.
5. Preserve factual meaning, claim strength, citations, technical terms, and useful
   structure. Keep intentional rhetoric when it passes the reference’s licensing test or
   a genre convention requires it.
6. Do not mechanically swap synonyms or add typos, slang, contractions, anecdotes,
   quirks, or unevenness to simulate a person.
   Do not make claims about detector scores or detector evasion.
7. Follow the target project’s formatting and validation rules.
   If the target is Markdown, run its configured formatter when one exists.
8. Re-read the result and diff for changed meaning, flattened voice, new repetition,
   unsupported specificity, or awkward rhythm.

## Output

Report the changed files or passages, the main tell classes corrected, and any flagged
construction retained because it carried information or fit the genre.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
