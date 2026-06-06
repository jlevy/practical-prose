---
type: is
id: is-01ktdvkrz57p98g5aghdazv4r6
title: Tighten NA-vs-score guidance for performative/contractual docs
kind: feature
status: closed
priority: 1
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01ktdvks6hym56yct9tn3z1tae
parent_id: is-01ktdvk2r21qw63cg34kvas59d
created_at: 2026-06-06T06:58:31.524Z
updated_at: 2026-06-06T07:03:47.895Z
closed_at: 2026-06-06T07:03:47.894Z
close_reason: "Added a 'Genre alone does not trigger NA' note to the scoring prompt's NA guidance: performative/contractual/legal genre does not by itself NA Verifiability/Factuality when checkable claims are present (institutional attributions, statutory cites like '48 C.F.R.', addresses, dated/quantitative facts). The G1 rubric anchor already supported this; the prompt now enforces it."
---
Verifiability/Factuality were marked NA on the iTunes terms despite institutional attributions ('Apple Inc., located at One Apple Park Way') and statutory citations ('48 C.F.R.' x4). Per the G1 NA anchor, attributions to institutions DO engage Verifiability. Clarify in the rubric (docs/practical-prose-rubric.md + synced resource) and/or the scoring prompt that performative genre does not by itself trigger NA when checkable institutional/statutory claims are present.
