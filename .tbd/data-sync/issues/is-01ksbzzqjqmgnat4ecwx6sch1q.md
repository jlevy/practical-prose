---
type: is
id: is-01ksbzzqjqmgnat4ecwx6sch1q
title: "Rubric doc: update scoring regex + 'How to score' guidance"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01ksbzxycfj95nzb0mexrshpp6
created_at: 2026-05-24T03:20:46.934Z
updated_at: 2026-05-24T03:20:46.934Z
---
docs/practical-prose-rubric.md ~line 172 and ~231: the 'integer 0-5 or NA' line becomes 'integer 1-5 or NA or ERR'; the regex (NA|[0-5]) becomes (NA|ERR|[1-5]).
