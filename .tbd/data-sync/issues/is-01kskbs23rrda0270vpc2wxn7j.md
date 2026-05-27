---
type: is
id: is-01kskbs23rrda0270vpc2wxn7j
title: "[chopdiff v0.4.x] Add Paragraph.inlines (typed inline walk)"
kind: task
status: open
priority: 1
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
dependencies:
  - type: blocks
    target: is-01kskbs2ymzshjbfvnsg1wp8n9
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:01:32.273Z
updated_at: 2026-05-27T00:02:13.907Z
---
Tracked here; work in jlevy/chopdiff. Add a cached Paragraph.inlines: list[Inline] property that walks the inline children of the cached parse result and emits typed values: Text(text), Link(url, text, kind: 'inline'|'autolink'|'reference_use'), Image(url, alt), CodeSpan(text), FootnoteRef(ref_id), LineBreak. Emphasis / Strong flatten to their inner text for v0.4.x (typed exposure can come later if a real metric needs it). Enables every link/image/footnote-ref/code-span pprose metric and removes the link/image/footnote regex sweeps.
