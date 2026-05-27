---
type: is
id: is-01kshh860nz3ttj6b5qe1p3wdf
title: Wire measure() to new pipeline; update format_human output
kind: task
status: closed
priority: 1
version: 3
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshh8k0tzbbehs802szk9vwy
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T06:58:41.809Z
updated_at: 2026-05-26T08:00:23.119Z
closed_at: 2026-05-26T08:00:23.117Z
close_reason: "Superseded by spec rewrite 2026-05-26: pprose now depends on chopdiff BlockDoc (jlevy/chopdiff#8). Replaced by a slimmer pprose-only bead set under the same epic pp-3hg4."
---
Replace the body of measure() in pprose/metrics.py so it calls build_structure once and then Metrics.from_structure. Delete strip_code_and_frontmatter and the regex-based structural counters (HEADING_RE, SETEXT_*, INLINE_LINK_RE, IMAGE_RE, AUTOLINK_RE, REF_LINK_DEF_RE, REF_LINK_USE_RE, FOOTNOTE_*_RE, TABLE_SEP_RE, CODE_FENCE_RE, CODE_INLINE_RE, FRONTMATTER_RE). Rewrite format_human to render: the heading_outline as an indented tree with section sizes; new list/table/code/distribution sections; the existing lint sections (renamed). Update format_summary_table to use new column names. Verify CLI 'pprose metrics path/to/doc.md' and '--format yaml' produce sensible output.
