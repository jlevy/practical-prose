---
type: is
id: is-01ksbzxycfj95nzb0mexrshpp6
title: Reshape rubric '0' score to 'ERR' sentinel; numeric range becomes 1-5
kind: epic
status: closed
priority: 2
version: 17
labels: []
dependencies: []
child_order_hints:
  - is-01ksbzzpf4vq12anme7phg3j6p
  - is-01ksbzzpkjjrnbn179v1kjykge
  - is-01ksbzzpr06ran53c25q48bdry
  - is-01ksbzzpwf3z5m79a4tqkx11h8
  - is-01ksbzzq12pg20htppqdndyhy8
  - is-01ksbzzq5ghgjgw13ryjtwppq4
  - is-01ksbzzq9x1qkkrwk2ccmq9905
  - is-01ksbzzqe9b8arc4xf2m6t0rdd
  - is-01ksbzzqjqmgnat4ecwx6sch1q
  - is-01ksbzzqq22pzvn2ngtz388tad
  - is-01ksbzzqvdwg4rewq1rb1583ee
  - is-01ksbzzr01wje4d885ttp4jyrs
  - is-01ksbzzr4f9kxys44jrw3esyz3
  - is-01ksbzzr90mr7hztqp2pmtzr6r
  - is-01ksbzzrdg2tp7k2ftqm10g7xh
created_at: 2026-05-24T03:19:48.360Z
updated_at: 2026-05-24T03:55:37.058Z
closed_at: 2026-05-24T03:55:37.057Z
close_reason: all 14 child beads implemented on rubric-zero-to-err branch; PR pending
---
Today the rubric admits score 0 with two conflated meanings: (a) the top-level decision tree says 0 = 'attempted but missing' (a substantive low score), while (b) every per-dimension anchor and the scoring prompt say 0 = 'Cannot assess' (an evaluator/process failure). Score 0 is also silently excluded from group/overall means (eval_report.py:543), so a 0 carries no signal in the rollup but reads as a quality verdict to humans. LLM scorers in practice almost always emit 0 with the process-failure meaning.

Reshape:
- Numeric scores become 1-5 (no 0).
- Add ERR as a named sentinel meaning 'scorer could not assess' (process failure, never a document-quality verdict).
- Keep NA as today: dimension does not engage with this artifact.
- Map the rare 'attempted but materially missing' case (current 0 meaning per the decision tree) to score 1 with a citation of the missed rule.

Wins:
- One meaning per value; the prompt, anchors, and rollup all line up.
- Numeric scores are always truthy (no 'if score:' coercion accident).
- ERR is countable separately (alongside na_dimensions) and surfaces eval-quality issues instead of being a silent zero.

Bumps the rubric version (20-dim-v1 -> 20-dim-v2). Child beads cover schema, code, docs, prompt, render/compare, migration, resource sync, tests, and runbook sweep.
