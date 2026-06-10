---
type: is
id: is-01ktr5csj7ca1e81c3q0tf8z3e
title: Add genre routing to the four guideline-reading skills
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01ktr5ct9yhxvyw18mnhdaqgjj
parent_id: is-01ktr5c579rk5z365t9eaax1ea
created_at: 2026-06-10T07:01:52.838Z
updated_at: 2026-06-10T07:07:23.318Z
closed_at: 2026-06-10T07:07:23.317Z
close_reason: "Added a genre-routing step to all four guideline-reading skill sources (copy-edit step 4, full-edit step 3, review step 2, eval step 2): if the target is a comprehensive practical guide, also read 'pprose guidelines writing-practical-guides', honoring each guideline's applies-when caveat. Wording tailored per skill (language-level for copy-edit; audit+fold-into-review for full-edit/review; genre context before scoring for eval, citing the rubric's genre lever). Regenerated discovery copies (skills/) and refreshed installed mirrors (.claude/, .agents/); routing verified on all three surfaces; sync --check and tests pass. Note: an install run from tools/pprose cwd created stray .claude/.agents/AGENTS.md there — removed; install anchors at cwd, not git root."
---
Add one routing step to tools/pprose/src/pprose/resources/skills/{pprose-copy-edit,pprose-full-edit,pprose-review,pprose-eval}.md: if the target document is a comprehensive practical guide, also read 'pprose guidelines writing-practical-guides' and apply/audit/score with its genre supplement in mind (each guideline there carries an applies-when caveat). pprose-common-edit stays genre-blind by design. Regenerate discovery copies via devtools/sync_resources.py; refresh this repo's installed skills via 'pprose install --auto'.
