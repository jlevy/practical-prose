---
type: is
id: is-01kv01xdvnpve6g7b6txhhr6pv
title: "Decide link-form metrics: keep regex vs adopt coarse counts"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - blocked-upstream
  - upstream-flexdoc
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-06-13T08:34:59.060Z
updated_at: 2026-06-13T08:34:59.060Z
---
flexdoc 0.1.0 collapses inline/autolink/reference-use links into one NodeKind.link with no form discriminator, returns bare URLs as links, and does not surface reference definitions ([id]: url). So links_inline/links_autolink/links_reference_use/links_reference_definitions/bare_urls and classify_url stay as pprose-side regex. Revisit if jlevy/flexdoc#5 (link-form discriminator + reference-definition surfacing) lands. Blocked on flexdoc#5.
