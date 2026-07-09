---
type: is
id: is-01kv02fkk6gp3h22megwd8mw70
title: "[flexdoc 0.1.0] sections()/toc() drops real ATX headings that blocks() finds"
kind: bug
status: closed
priority: 2
version: 4
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
created_at: 2026-06-13T08:44:54.757Z
updated_at: 2026-06-14T02:13:59.029Z
closed_at: 2026-06-14T02:13:59.028Z
close_reason: "Fixed in flexdoc 0.2.0 (PR jlevy/flexdoc#7): sections()/toc() derive from structural heading blocks; verified toc()==blocks() across all repo docs."
---
In AGENTS.md, doc.blocks() correctly returns 4 heading blocks (1 h1 + 3 h2: '## Practical Prose (pprose)', '## tbd', '## flowmark'), but doc.toc()/sections() returns only the h1 with span covering the whole doc; the 3 h2 are dropped. Likely related to the HTML-comment marker block (<!-- BEGIN PPROSE INTEGRATION -->) perturbing the blank-line paragraph view that _section_list bisects against. Makes toc()/sections() unreliable for heading-by-level counts. File upstream against jlevy/flexdoc.
