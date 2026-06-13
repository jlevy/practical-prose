---
type: is
id: is-01kv02fkc0h7fhcjp1ptg0fhrk
title: "[flexdoc 0.1.0] collect()/node_table crashes on valid markdown (layer nesting violated)"
kind: bug
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - upstream-flexdoc
  - blocked-upstream
dependencies:
  - type: blocks
    target: is-01kskbsx1f7fm5cmj1j6hca4qb
  - type: blocks
    target: is-01kv01wyqcvnjrwzp5096t3d43
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-06-13T08:44:54.527Z
updated_at: 2026-06-13T18:36:09.391Z
---
FlexDoc.collect()/node_table() raises ValueError: 'layer nesting violated: markdown node ... not within parent ...' on 2 of 61 real repo docs (docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md and docs/project/specs/done/plan-2026-05-12-eval-scoring-rearchitecture.md). Because collect() is the only typed path to images/footnote_refs/code_spans, metrics.py cannot safely swap those off regex until fixed. blocks()/sections()/toc()/links()/filtered() do NOT use node_table and are robust. File upstream against jlevy/flexdoc.
