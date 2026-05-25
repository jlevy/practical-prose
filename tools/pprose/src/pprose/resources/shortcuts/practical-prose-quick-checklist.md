---
title: Practical Prose Quick Checklist
description: Single-page pre-publish self-audit covering the 20 practical-prose dimensions in six short groups; for use when the full guidelines are too long to load
category: documentation
author: Joshua Levy (github.com/jlevy) with agent assistance
---
# Practical Prose Quick Checklist

A one-page pre-publish self-audit for documents written under
[practical-prose-guidelines.md](../docs/practical-prose-guidelines.md).
Walk the six groups in order.
For each line: yes / no / NA. If a question is unclear, jump to its dimension in the
full guidelines (the §-number points there directly).

For generation-time guidance (drafting a doc from scratch), see
[practical-prose-agent-policy.md](practical-prose-agent-policy.md); this checklist is
for pre-publish audit of an already-drafted doc.

**Scope of the audit:**

- The applicable dimensions depend on `risk_level`. Low-stakes notes audit only P1 / E1
  / E3 / F3; standard internal docs audit Purpose, Expression, Grounding,
  and R2 Soundness; decision memos / audits / deep research audit all 20; reference
  / runbook docs focus on P1 / P2 / F1 / F3 / R3 and the Maintainable principle.
  See `practical-prose-metrics.md` §Applicability Profiles.
- A scored rule miss can be a **justified deviation** instead of a defect, if you
  document the rule set aside, the reader outcome served, and the risk introduced.
  See *Justified Deviations* in `practical-prose-rubric.md`.

## Purpose (P1-P4)

- [ ] **P1 Suitability:** Is the task named?
  Does the output shape (recommendation, findings, milestones, …) fit the task?
  Is the reader burden the document removes named (§1.6)?
- [ ] **P2 Scope:** Is the scope declared at the opening, and does the body honor it?
  Is what the document is *not competent to conclude* named (§2.5)?
- [ ] **P3 Breadth:** Within scope, are the relevant case classes, prior work, and
  standard sources present?
- [ ] **P4 Depth:** Do the sections the document’s purpose depends on get more detail
  than tangential ones?

## Expression (E1-E3)

- [ ] **E1 Clarity:** Any banned-register words, vague magnitudes, meta-commentary, or
  parallel-structure padding (“not X but Y” without a real X)?
- [ ] **E2 Coherence:** Does each paragraph have one job?
  Do transitions bridge or stub?
- [ ] **E3 Concision:** Does every section earn its place?
  Any duplication across sections?

## Form (F1-F3)

- [ ] **F1 Organization:** Heading hierarchy logical?
  Tables earn their tabular shape?
  Figures captioned? Links resolve?
- [ ] **F2 Consistency:** Dialect, casing, parallel-list syntax, citation style,
  register all consistent?
- [ ] **F3 Formatting:** Markdown renders correctly?
  Frontmatter and footer present and well-placed?
  No raw-source artifacts visible?

## Reasoning (R1-R4)

- [ ] **R1 Discipline:** Observation, judgment, interpretation, implication
  worked through in order, each higher rung supported by the prior? Each rung
  carries its own evidence?
- [ ] **R2 Soundness:** Mechanisms named where causation is asserted?
  Assumptions surfaced?
  Counter-evidence engaged?
  Counterfactual test for causal claims: would we expect to see something different if
  the explanation were wrong (§12.8)?
- [ ] **R3 Precision:** Most specific term the audience can parse used?
  Umbrella terms avoided where sub-distinctions matter?
- [ ] **R4 Parsimony:** Each load-bearing reasoning chain the minimum sufficient
  sound argument? No non-load-bearing rungs; no weaker warrant where a stronger one
  was available; re-derivations only where they add inspectability, confidence, or
  audience understanding beyond what a citation would?

## Grounding (G1-G3)

- [ ] **G1 Verifiability:** Every quantitative claim source-traceable at the
  stakes-appropriate bar?
  Confidence tags paired with sources?
  For central claims, is what would invalidate them named (§15.5)?
- [ ] **G2 Factuality:** Cited sources support the claim at the asserted strength?
  Numbers match sources, or rounding disclosed?
- [ ] **G3 Relevance:** Every cited source and every section bears on the document's
  purpose? Digressions marked as digressions? Each source passes the one-sentence
  test ("this source supports claim X, which bears on purpose Y")?

## Judgment (J1-J3)

- [ ] **J1 Calibration:** Probability claims anchored in base rates?
  Scenario probabilities sum to 100%? Confidence without cowardice: no mushy hedging on
  strong evidence (§18.6)?
- [ ] **J2 Fairness:** Opposing positions engaged at proportional depth, with any
  asymmetry declared?
- [ ] **J3 Robustness:** Key claims tested against the most-threatening alternative
  interpretation? Lens-dependent claims surfaced as findings?

## Audit-pass operationalization

If the document is high-stakes, run the four audit passes separately rather than one
broad pass:

1. **Lint pass:** Cosmetic / deterministic: F1 Organization, F2 Consistency, F3
   Formatting, E1 banned-register and vague-word checks.
   Use `pprose metrics`.
2. **Claim audit:** Every quantitative claim against its cited source.
   G1 Verifiability, G2 Factuality.
   Re-run calculations.
3. **Reasoning audit:** Assumptions, mechanisms, counter-evidence, parsimony,
   alternative lenses.
   R1 Discipline, R2 Soundness, R4 Parsimony, J2 Fairness, J3 Robustness.
   Best with a fresh-context agent.
4. **Purpose audit:** Output shape vs task shape; scope; skim-recoverability.
   P1 Suitability, P2 Scope, P3 Breadth, P4 Depth.
   Best with a reader simulation.

The pass separation is **required** for high-stakes documents, **recommended** for
standard internal docs, and **optional** for low-stakes drafts.
Where the discipline applies, do not combine passes. Running them in parallel by the
same agent in the same context loses the cognitive separation the structure depends on.

## When to use this checklist

- Before publishing any practical-prose document (decision memo, audit, research report,
  spec, design doc, technical paper).
- After a Substance pass, before a Quality-audit pass, when the full guidelines are too
  long to load into context.
- As the Lint-pass anchor for high-stakes evaluations.

This checklist stays in sync with the full
[practical-prose-guidelines.md](../docs/practical-prose-guidelines.md); when the
guidelines change, update this checklist in the same edit.

<!-- This document follows common-doc-guidelines.md.
Review guidelines before editing.
-->
