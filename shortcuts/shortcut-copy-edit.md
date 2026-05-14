---
title: Copy Edit Document
description: Copy-edit and proofread a document against common-doc-guidelines; track and fix all issues with available task tooling
category: documentation
author: Joshua Levy (github.com/jlevy) with agent assistance
---
# Copy-Edit Shortcut

## Instructions

Apply the standard documentation guidelines to a document:

1. Read `common-doc-guidelines.md` fully.

2. Audit the target against every rule.
   Be thorough; small issues count.
   - **If you find more than 5 issues and project issue tooling is available:** File an
     epic or parent issue with one child issue per fix. Use `tbd` beads when available;
     otherwise use the repo's equivalent tracker.
   - **If no external issue tracker is available:** Use the agent's normal to-do or
     checklist tooling.
   - **If you find 5 or fewer issues:** Use the agent's normal to-do or checklist tooling
     unless the user asked for external issue tracking.

3. Apply all fixes.
   Close or update any external issues you created as you fix them.

4. Verify:
   - Check git diff and re-scan for regressions.
   - If external issues were used, confirm the relevant child issues and parent issue are
     closed or updated.

5. Report issues found, changes made, and any external issue or bead IDs.
