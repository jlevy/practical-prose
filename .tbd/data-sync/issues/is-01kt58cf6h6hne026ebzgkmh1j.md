---
type: is
id: is-01kt58cf6h6hne026ebzgkmh1j
title: "Phase 1: adopt frontmatter-format for EvalReport YAML + add 'pprose show' structured export"
kind: task
status: closed
priority: 1
version: 10
spec_path: docs/project/specs/active/plan-2026-06-02-eval-output-improvements.md
labels: []
dependencies: []
parent_id: is-01kt58c3t45ac6ag66v1wfcgvc
child_order_hints:
  - is-01kt5a9dndecj1kw0yx9p0g31t
  - is-01kt5a9e1c8qazhysvvgk5vwka
  - is-01kt5a9ecp8t9evj7h09scbzac
  - is-01kt5a9eq9h2cyxtnczrx3p6n7
  - is-01kt5a9f1fs7fwnhvf8vtk4b09
created_at: 2026-06-02T22:48:33.740Z
updated_at: 2026-06-03T19:15:11.959Z
closed_at: 2026-06-03T19:15:11.958Z
close_reason: Superseded by reporting CLI redesign epic pp-d2j3 (spec plan-2026-06-03-reporting-cli-redesign.md); work folded into its phases.
---
Add frontmatter-format==0.3.0 (first-party, pinned). Migrate EvalReport.to_yaml() to frontmatter-format with a logical custom_key_sort. Add top-level 'pprose show <eval.md>' command (sibling of render, new module + cli.py registration) with --format mdyaml|yaml|json (default mdyaml = markdown + YAML frontmatter; yaml = pure structured frontmatter; json = structured JSON) and --output (long flags only per python-cli-patterns; format inferred from extension when --format omitted). Re-serialize the 9 .eval.md fixtures + comparison golden; confirm formatting-only diffs. Round-trip + key-order + show-output tests for all three formats.
