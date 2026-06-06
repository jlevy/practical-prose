---
type: is
id: is-01ktdvkr8fvq08g2bgskm2n0bv
title: Clean iTunes fixture conversion artifacts (unescape \- and \$)
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01ktdvks6hym56yct9tn3z1tae
parent_id: is-01ktdvk2r21qw63cg34kvas59d
created_at: 2026-06-06T06:58:30.798Z
updated_at: 2026-06-06T07:01:36.421Z
closed_at: 2026-06-06T07:01:36.420Z
close_reason: Unescaped 29 '\-' list bullets to real Markdown lists and the one '\$250.00'; flowmark-normalized. Fixture now renders as clean Markdown so Formatting/Consistency score the document, not pandoc artifacts.
---
example-texts/apple-media-services-terms.md has 29 escaped '\-' list hyphens and one '\$' from pandoc conversion. These are scored under Formatting/Consistency, penalizing the conversion not Apple's document. Unescape them (and any similar artifacts) so the fixture renders as clean Markdown.
