---
type: is
id: is-01kt5a9eq9h2cyxtnczrx3p6n7
title: Re-serialize the 9 .eval.md fixtures + update comparison goldens to new key order
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-06-02-eval-output-improvements.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt5a9f1fs7fwnhvf8vtk4b09
parent_id: is-01kt58cf6h6hne026ebzgkmh1j
created_at: 2026-06-02T23:21:52.103Z
updated_at: 2026-06-03T19:15:13.556Z
closed_at: 2026-06-03T19:15:13.554Z
close_reason: Superseded by reporting CLI redesign epic pp-d2j3 (spec plan-2026-06-03-reporting-cli-redesign.md); work folded into its phases.
---
Regenerate tools/pprose/tests/fixtures/*.eval.md and any golden output (expected-comparison.md, expected YAML) under the new frontmatter-format writer + key order. Confirm diffs are formatting-only (no semantic change).
