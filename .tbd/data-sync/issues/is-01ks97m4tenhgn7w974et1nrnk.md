---
type: is
id: is-01ks97m4tenhgn7w974et1nrnk
title: '[epic] Add "Parsimony" as a 4th Reasoning sub-dimension'
kind: epic
status: open
priority: 2
version: 13
labels:
  - rubric-rollout
  - parsimony
dependencies: []
child_order_hints:
  - is-01ks97mrcpevmbkaqgkvwrx6nx
  - is-01ks97p7pndmqqjw1hk3b94e1q
  - is-01ks97pd2e5h9h8rgzyraxja9f
  - is-01ks97pmpnytq5mjeg6becv852
  - is-01ks97pt59x63ht24wf74d08yf
  - is-01ks97q4vvxq99hpdhpt396gvy
  - is-01ks97qev6jz44nkqjs438dwen
  - is-01ks97qrtgbfkphsyhd1tb0spf
  - is-01ks97r0f8b0ad44w0z5xnccgw
  - is-01ks97rbrhph4pbq49mhwp9xhz
  - is-01ks97rpmhnq79he6aqq15fvkk
  - is-01ks97s25n1s058wk2nfqbtvx3
created_at: 2026-05-23T01:36:32.590Z
updated_at: 2026-05-23T01:39:13.717Z
---
Add a new Practical Prose dimension **Parsimony** as a fourth Reasoning sub-dimension, alongside Inference Discipline, Soundness, and Precision.

## Concept

Parsimony measures whether each load-bearing reasoning chain is the cleanest, simplest sound argument possible for its conclusion. Length is not the test; necessity given the warrant strengths in use is. A 50-step rigorous proof is parsimonious if no shorter sound proof exists; a 2-step hand-wave is non-parsimonious if it elides necessary intermediates.

## Where it lands

- **Group:** Reasoning (alongside §13 Inference Discipline, §14 Soundness, §15 Precision)
- **Section number:** §16 if landed alone (Calibration/Fairness/Robustness shift to §17/§18/§19, rubric version → 19-dim-v1). If the Relevance epic lands first or concurrently, Parsimony lands at §17 and rubric version → 20-dim-v1.

## Distinct from neighbors

- **§13 Inference Discipline** — tests whether rungs are named; Parsimony tests whether the chain is minimum.
- **§14 Soundness** — tests whether each step is valid; Parsimony tests whether the chain shape is minimum given the per-step warrants. **Parsimony presupposes Soundness ≥ 3.**
- **§7 Concision** — prose-level economy (words/paragraphs); Parsimony is argument-level economy (rungs in the inferential chain).

## Rubric anchors (locked in P1 sub-bead)

- **5:** Every line of inference appears to be the most clean and simple argument possible to a sound conclusion.
- **4:** A few arguments could be simplified but maintain the same level of soundness and precision.
- **3:** In between; workable.
- **2:** Obviously extraneous elements in multiple load-bearing chains.
- **1:** Obviously extraneous elements throughout.

## Scope of rollout

Touches ~30 files: rubric schema (single source of truth), Pydantic models, LLM scoring prompt, render module, three test files, ten golden eval fixtures + the comparison golden, five canonical docs, two shortcuts, one skill, one runbook, README. Detailed sub-bead breakdown follows.

## Prior art noted in the design

GRADE 'indirectness' (evidence-based medicine), Toulmin warrant/backing, Tim van Gelder argument-map depth, Minimum Description Length, proof minimization. Parsimony is closest to MDL: minimize (argument length + unexplained residual).
