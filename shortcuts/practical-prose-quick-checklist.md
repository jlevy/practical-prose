---
title: Practical Prose Quick Checklist
description: Single-page pre-publish self-audit covering the 20 practical-prose dimensions in five short groups; for use when the full guidelines are too long to load
category: documentation
author: Joshua Levy (github.com/jlevy) with agent assistance
---
# Practical Prose Quick Checklist

A one-page pre-publish self-audit for documents written under
[practical-prose-guidelines.md](../docs/practical-prose-guidelines.md).
Walk the five groups in order.
For each line: yes / no / NA. If a question is unclear, jump to its dimension in the
full guidelines (the §-number points there directly).

For generation-time guidance (drafting a doc from scratch), see
[practical-prose-agent-policy.md](practical-prose-agent-policy.md); this checklist is
for pre-publish audit of an already-drafted doc.

**Scope of the audit:**

- The applicable dimensions depend on `risk_level`. Low-stakes notes audit only §1 / §5
  / §7 / §10; standard internal docs audit Purpose + Expression + Grounding
  + §15 Soundness; decision memos / audits / deep research audit all 20; reference /
  runbook docs focus on §1 / §2 / §8 / §10 / §16 + Maintainable.
  See `practical-prose-metrics.md` §Applicability Profiles.
- A scored rule miss can be a **justified deviation** instead of a defect, if you
  document the rule set aside, the reader outcome served, and the risk introduced.
  See *Justified Deviations* in `practical-prose-rubric.md`.

## Purpose (§1-§4)

- [ ] **§1 Suitability** — Is the task named?
  Does the output shape (recommendation, findings, milestones, …) fit the task?
  Is the reader burden the document removes named (§1.6)?
- [ ] **§2 Scope** — Is the scope declared at the opening, and does the body honor it?
  Is what the document is *not competent to conclude* named (§2.5)?
- [ ] **§3 Breadth** — Within scope, are the relevant case classes, prior work, and
  standard sources present?
- [ ] **§4 Depth** — Do the sections the document’s purpose depends on get more detail
  than tangential ones?

## Expression (§5-§10)

- [ ] **§5 Clarity** — Any banned-register words, vague magnitudes, meta-commentary, or
  parallel-structure padding (“not X but Y” without a real X)?
- [ ] **§6 Coherence** — Does each paragraph have one job?
  Do transitions bridge or stub?
- [ ] **§7 Concision** — Does every section earn its place?
  Any duplication across sections?
- [ ] **§8 Organization** — Heading hierarchy logical?
  Tables earn their tabular shape?
  Figures captioned? Links resolve?
- [ ] **§9 Consistency** — Dialect, casing, parallel-list syntax, citation style,
  register all consistent?
- [ ] **§10 Formatting** — Markdown renders correctly?
  Frontmatter and footer present and well-placed?
  No raw-source artifacts visible?

## Grounding (§11-§13)

- [ ] **§11 Verifiability** — Every quantitative claim source-traceable at the
  stakes-appropriate bar?
  Confidence tags paired with sources?
  For central claims, is what would invalidate them named (§11.5)?
- [ ] **§12 Factuality** — Cited sources support the claim at the asserted strength?
  Numbers match sources, or rounding disclosed?
- [ ] **§13 Relevance** — Every cited source and every section bears on the document's
  purpose? Digressions marked as digressions? Each source passes the one-sentence
  test ("this source supports claim X, which bears on purpose Y")?

## Reasoning (§14-§17)

- [ ] **§14 Discipline** — Observation, judgment, interpretation, implication
  kept distinct? Each rung carries its own evidence?
- [ ] **§15 Soundness** — Mechanisms named where causation is asserted?
  Assumptions surfaced?
  Counter-evidence engaged?
  Counterfactual test for causal claims: would we expect to see something different if
  the explanation were wrong (§15.8)?
- [ ] **§16 Precision** — Most specific term the audience can parse used?
  Umbrella terms avoided where sub-distinctions matter?
- [ ] **§17 Parsimony** — Each load-bearing reasoning chain the minimum sufficient
  sound argument? No citable facts re-derived, no non-load-bearing rungs, no weaker
  warrant where a stronger one was available?

## Judgment (§18-§20)

- [ ] **§18 Calibration** — Probability claims anchored in base rates?
  Scenario probabilities sum to 100%? Confidence without cowardice: no mushy hedging on
  strong evidence (§18.6)?
- [ ] **§19 Fairness** — Opposing positions engaged at proportional depth, with any
  asymmetry declared?
- [ ] **§20 Robustness** — Key claims tested against the most-threatening alternative
  interpretation? Lens-dependent claims surfaced as findings?

## Audit-pass operationalization

If the document is high-stakes, run the four audit passes separately rather than one
broad pass:

1. **Lint pass** — Cosmetic / deterministic: §8 Organization, §9 Consistency, §10
   Formatting, §5 banned-register and vague-word checks.
   Use `prose-eval metrics`.
2. **Claim audit** — Every quantitative claim against its cited source.
   §11 Verifiability, §12 Factuality.
   Re-run calculations.
3. **Reasoning audit** — Assumptions, mechanisms, counter-evidence, parsimony,
   alternative lenses.
   §14 Discipline, §15 Soundness, §17 Parsimony, §19 Fairness, §20 Robustness.
   Best with a fresh-context agent.
4. **Purpose audit** — Output shape vs task shape; scope; skim-recoverability.
   §1 Suitability, §2 Scope, §3 Breadth, §4 Depth.
   Best with a reader simulation.

The pass separation is **required** for high-stakes documents, **recommended** for
standard internal docs, and **optional** for low-stakes drafts.
Where the discipline applies, do not combine passes — running them in parallel by the
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
