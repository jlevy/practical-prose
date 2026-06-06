---
type: is
id: is-01ktdvkrqm1m1tg056wa26a2qa
title: "Scoring prompt: require a rule_finding for every score below 5"
kind: feature
status: closed
priority: 1
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01ktdvks6hym56yct9tn3z1tae
parent_id: is-01ktdvk2r21qw63cg34kvas59d
created_at: 2026-06-06T06:58:31.283Z
updated_at: 2026-06-06T07:03:47.684Z
closed_at: 2026-06-06T07:03:47.683Z
close_reason: Root cause was the 'Volume' guidance capping the whole report at ~10 findings, conflicting with the one-finding-per-sub-5 requirement. Reworded Volume to make the per-dimension floor mandatory and override brevity, and added an explicit hard-requirement bullet. tools/pprose/src/pprose/prompts/eval-rubric-score.md.
---
tools/pprose/src/pprose/prompts/eval-rubric-score.md: the scorer writes good prose reasons but under-emits structured rule_findings for sub-5 scores, tripping the alignment guard (we needed --allow-misaligned; ~11 issues on Bush). Update the prompt so every score < 5 emits a matching rule_finding; verify against both example docs.
