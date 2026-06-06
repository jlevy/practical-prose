---
type: is
id: is-01ktdvkrg2safyp2p9xv376xqz
title: Fix Bush fixture section headings (bare '## 1'..'## 8')
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01ktdvks6hym56yct9tn3z1tae
parent_id: is-01ktdvk2r21qw63cg34kvas59d
created_at: 2026-06-06T06:58:31.041Z
updated_at: 2026-06-06T07:01:54.967Z
closed_at: 2026-06-06T07:01:54.966Z
close_reason: Converted bare '## 1'..'## 8' ATX headings to thematic-break + bold-numeral section dividers. Preserves the original's numbered section structure without injecting the generic/templated-heading (F1 rule-9) defect our conversion had added.
---
example-texts/as-we-may-think.md renders the original section numbers as bare '## 1'..'## 8' headings, which trip F1 rule-9 (generic/templated headings) and drag Organization to 2 — scoring our conversion, not Bush. Decide a faithful representation (e.g., non-heading numbered separators) that does not inject a navigational defect the original did not have.
