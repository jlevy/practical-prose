---
type: is
id: is-01ks97vjxrmnzmxk6ke3hmt505
title: '[epic] Add "Relevance" as a 3rd Grounding sub-dimension'
kind: epic
status: open
priority: 2
version: 12
labels:
  - rubric-rollout
  - relevance
dependencies: []
child_order_hints:
  - is-01ks97w2sc5gv4c3tqgtz4aqzz
  - is-01ks97wdme24jtc6pja2yyqkwk
  - is-01ks97whzq6pr6kdgw01bk87x1
  - is-01ks97ws5fabst53vaqba9vdfk
  - is-01ks97wyqfkqcx7w5mzkwhs893
  - is-01ks97xacz7gyeyycb8ggn697e
  - is-01ks97xjn9tykqefyv11kkr9xa
  - is-01ks97xwbrn363f1mnbm2pptwm
  - is-01ks97y1tdc5cjhxakkbtj012a
  - is-01ks97ycmb6hp3mfmz5q8qkbpd
  - is-01ks97yme61jy7g3wwczpt9fy0
created_at: 2026-05-23T01:40:36.408Z
updated_at: 2026-05-23T01:42:16.261Z
---
Add a new Practical Prose dimension **Relevance** as a third Grounding sub-dimension, alongside §11 Verifiability and §12 Factuality.

## Concept

Relevance measures how much of a document's sources, citations, and intermediate reasoning chains bear on the document's stated purpose. A document with thoroughly cited but tangential sources fails Relevance even if every source is traceable (Verifiability) and accurately summarized (Factuality). The Grounding group thus tests three properties of evidence: it can be found (Verifiability), it says what the document says it says (Factuality), and it matters for the document's purpose (Relevance).

## Where it lands

- **Group:** Grounding (alongside §11 Verifiability, §12 Factuality)
- **Section number:** §13 — Inference Discipline through Robustness all shift by 1.
- **Rubric version:** `19-dim-v1` if landed alone; `20-dim-v1` if landed concurrently with the Parsimony epic (pp-38s0).

## Distinct from neighbors

- **§11 Verifiability:** tests traceability of claims to sources. Relevance tests whether the traced sources connect to the document's purpose.
- **§12 Factuality:** tests whether sources support the claim made. Relevance tests whether that claim matters for the document's purpose.
- **§2 Scope:** declares what's in the document. Relevance tests whether the content delivered honors that declaration.
- **§7 Concision:** prose-level economy (words/paragraphs). Relevance: content-level economy (sources/points).
- **§16 Parsimony (if landed):** minimum sound argument chain for a load-bearing claim. Relevance: minimum sufficient set of materials. Parsimony failure: 'chain too long for its conclusion.' Relevance failure: 'source/section not connected to the purpose.'

## Rubric anchors (from user spec; locked in R1 sub-bead)

- **5:** Every source and line of reasoning is relevant to the purpose; nothing can be removed without lowering quality.
- **4:** A few sources or notes are a bit of a stretch (cited for completeness or as digressions) but still loosely relevant.
- **3:** In between.
- **2:** A significant fraction of seemingly extraneous sources or points ancillary to the purpose.
- **1:** Half or more sources seem irrelevant to the conclusions or purpose.

## Coordination with Parsimony epic (pp-38s0)

Both epics add a new dim. If Parsimony lands first:
- It picks up §16 with version 19-dim-v1.
- Relevance then comes in at §13 with version 20-dim-v1, and Parsimony renumbers to §17.

If Relevance lands first:
- It picks up §13 with version 19-dim-v1.
- Parsimony then comes in at §17 (because §13-§16 shifted) with version 20-dim-v1.

If concurrent:
- Both land together, version → 20-dim-v1, Relevance at §13, Parsimony at §17.

The sub-bead R1 (content lock) and the schema/doc beads explicitly note the renumber-dependence.

## Scope of rollout

Same shape as Parsimony — ~30 files: rubric schema, Pydantic models (different field placement: GroundingScores instead of JudgmentScores), LLM scoring prompt, render module (already handled by Parsimony's dynamic-dim-count fix), three test files, ten golden eval fixtures + the comparison golden, five canonical docs, two shortcuts, one skill, one runbook, README.
