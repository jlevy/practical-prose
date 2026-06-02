---
type: is
id: is-01kt5a9eq9h2cyxtnczrx3p6n7
title: Re-serialize the 9 .eval.md fixtures + update comparison goldens to new key order
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-06-02-eval-output-improvements.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt5a9f1fs7fwnhvf8vtk4b09
parent_id: is-01kt58cf6h6hne026ebzgkmh1j
created_at: 2026-06-02T23:21:52.103Z
updated_at: 2026-06-02T23:22:13.089Z
---
Regenerate tools/pprose/tests/fixtures/*.eval.md and any golden output (expected-comparison.md, expected YAML) under the new frontmatter-format writer + key order. Confirm diffs are formatting-only (no semantic change).
