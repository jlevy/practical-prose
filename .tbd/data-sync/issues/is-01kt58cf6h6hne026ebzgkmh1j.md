---
type: is
id: is-01kt58cf6h6hne026ebzgkmh1j
title: "Phase 1: adopt frontmatter-format for EvalReport YAML + add 'pprose report show' structured export"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-06-02-eval-output-improvements.md
labels: []
dependencies: []
parent_id: is-01kt58c3t45ac6ag66v1wfcgvc
created_at: 2026-06-02T22:48:33.740Z
updated_at: 2026-06-02T22:48:33.740Z
---
Add frontmatter-format==0.3.0 (first-party, pinned). Migrate EvalReport.to_yaml() to frontmatter-format with a logical custom_key_sort. Add 'pprose report show <eval.md> --format yaml|json' (default yaml). Re-serialize the 9 .eval.md fixtures + comparison golden; confirm formatting-only diffs. Round-trip + key-order + show-output tests.
