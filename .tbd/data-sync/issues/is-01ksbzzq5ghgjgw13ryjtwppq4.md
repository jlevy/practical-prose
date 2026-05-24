---
type: is
id: is-01ksbzzq5ghgjgw13ryjtwppq4
title: "Rubric doc: rewrite score-value intro and add motivation note (why no 0)"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01ksbzxycfj95nzb0mexrshpp6
created_at: 2026-05-24T03:20:46.511Z
updated_at: 2026-05-24T03:20:46.511Z
---
docs/practical-prose-rubric.md ~lines 38-55: rewrite the score-value bullets to 1-5 + NA + ERR. Add a short motivation paragraph explaining that 0 was conflating 'attempted but missing' (a quality verdict) with 'cannot assess' (a process failure), and that ERR cleanly separates the second case. Note the side benefit: numeric scores are always truthy, so 'if score:' checks can't accidentally treat an unassessable dim as a quality-zero swing.
