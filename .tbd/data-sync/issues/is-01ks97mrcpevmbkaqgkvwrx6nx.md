---
type: is
id: is-01ks97mrcpevmbkaqgkvwrx6nx
title: Lock canonical §16 Parsimony content (guideline rules + rubric anchors + metric row + profile placement)
kind: task
status: open
priority: 2
version: 8
labels:
  - rubric-rollout
  - parsimony
  - spec
dependencies:
  - type: blocks
    target: is-01ks97p7pndmqqjw1hk3b94e1q
  - type: blocks
    target: is-01ks97qrtgbfkphsyhd1tb0spf
  - type: blocks
    target: is-01ks97r0f8b0ad44w0z5xnccgw
  - type: blocks
    target: is-01ks97rbrhph4pbq49mhwp9xhz
  - type: blocks
    target: is-01ks97rpmhnq79he6aqq15fvkk
parent_id: is-01ks97m4tenhgn7w974et1nrnk
created_at: 2026-05-23T01:36:52.629Z
updated_at: 2026-05-23T01:39:39.272Z
---
First sub-bead in the Parsimony epic. Output is a locked draft of the canonical content that every downstream sub-bead pulls from.

## Deliverables

1. **Guideline rules (6 rules)** — for `docs/practical-prose-guidelines.md` §16. Current draft:
   1. Cite, don't re-derive. (Where direct evidence is available, cite it rather than building an inferential chain to the same conclusion.)
   2. Cut non-load-bearing steps. (Each rung should be necessary; if removing it leaves the argument intact, remove it.)
   3. Match chain length to warrant strength. (Long chains of strong deductive steps are parsimonious when no shorter chain of the same warrant type exists.)
   4. Don't truncate required intermediates. (Where a claim requires N intermediates with the warrants in use, all N must appear.)
   5. Prefer the most direct warrant available. (Use deduction where it works; cite measurement where available; name mechanism where known.)
   6. Parsimony applies to load-bearing chains. (Side notes, illustrative examples, motivational background are exempt.)

2. **Rubric anchors** — for `docs/practical-prose-rubric.md` §16:
   - **NA:** Document makes no inferential claims (pure reference data, raw measurements).
   - **0:** Cannot assess; or Soundness has already failed materially.
   - **1:** Obviously extraneous elements throughout chains of reasoning.
   - **2:** Obviously extraneous elements in multiple load-bearing chains.
   - **3:** Workable; chains roughly right shape; several arguments could be tightened.
   - **4:** A few arguments could be simplified but maintain the same level of soundness and precision.
   - **5:** Every line of inference or argument appears to be the most clean and simple argument possible to a sound conclusion.
   - Also: Parsimony presupposes Soundness ≥ 3; when Soundness is 1–2, Parsimony is 0.

3. **Metric row** — for `docs/practical-prose-metrics.md`. NOT raw chain length (which would penalize formal proofs). Instead:
   - Count of chains where a shorter sound chain exists (citable fact re-derived; weaker warrant where a stronger one is available).
   - Count of non-load-bearing rungs flagged within load-bearing chains.
   - Per-doc parsimony-gap flag count.
   - Qualitative check: 'For each load-bearing chain, is it the minimum sufficient given its purpose and per-step warrants?'
   - Tooling: LLM-assist; manual.

4. **Profile placement** — for `docs/practical-prose-metrics.md` Applicability Profiles table:
   - Low-stakes: typically NA.
   - Standard: conditional (when doc makes inferential claims).
   - High: required.
   - Reference/runbook: typically NA.

5. **Cross-reference notes** — Parsimony vs §7 Concision, vs §13 Inference Discipline, vs §14 Soundness, vs §15 Precision. Each gets a one-sentence distinguisher in the guidelines text.

## Acceptance

User signs off on the locked draft. All downstream sub-beads then pull this content verbatim into their files.
