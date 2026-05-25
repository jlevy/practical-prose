---
title: Copy Edit Document
description: Language-and-formatting edit pass — the common documentation substrate plus the Expression and Form dimensions (E1-E3, F1-F3); track and fix all issues with available task tooling
category: documentation
author: Joshua Levy (github.com/jlevy) with agent assistance
---
# Copy-Edit Shortcut

A language-and-formatting pass: the common documentation substrate plus the Expression
dimensions of the Practical Prose guidelines. It is a superset of common-edit and stops
short of the substantive dimensions (use the full-edit playbook for those).

## Instructions

1. Read `common-doc-guidelines.md` fully — the common substrate: organization,
   structure, writing style, formatting, links, headings, lists, frontmatter, footer.

2. Read the Expression and Form dimensions of `practical-prose-guidelines.md`
   (§Expression Dimensions, E1-E3, and §Form Dimensions, F1-F3): E1 Clarity (banned-register words, vague magnitudes,
   meta-commentary, parallel-structure padding), E2 Coherence, E3 Concision,
   F1 Organization, F2 Consistency, F3 Formatting.

3. Audit the target against every rule in both.
   Be thorough; small issues count.
   - **More than 5 issues and project issue tooling is available:** file an epic/parent
     issue with one child per fix (`tbd` beads when available; else the repo's tracker).
   - **Otherwise:** use the agent's normal to-do or checklist tooling.

4. Apply all fixes. **Preserve factual meaning, claim strength, citations, and
   intentional voice.** Do not edit the substantive dimensions (Purpose, Reasoning,
   Grounding, Judgment) — if those need work, note it and recommend `pprose-full-edit`.
   Close or update any external issues as you fix them.

5. Verify:
   - Check git diff and re-scan for regressions.
   - If external issues were used, confirm the child issues and parent are closed/updated.

6. Report issues found, changes made, and any external issue or bead IDs.
