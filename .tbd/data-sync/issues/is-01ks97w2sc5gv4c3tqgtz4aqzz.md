---
type: is
id: is-01ks97w2sc5gv4c3tqgtz4aqzz
title: Lock canonical §13 Relevance content (guideline rules + rubric anchors + metric row + profile placement)
kind: task
status: open
priority: 2
version: 6
labels:
  - rubric-rollout
  - relevance
  - spec
dependencies:
  - type: blocks
    target: is-01ks97wdme24jtc6pja2yyqkwk
  - type: blocks
    target: is-01ks97xjn9tykqefyv11kkr9xa
  - type: blocks
    target: is-01ks97xwbrn363f1mnbm2pptwm
  - type: blocks
    target: is-01ks97y1tdc5cjhxakkbtj012a
  - type: blocks
    target: is-01ks97ycmb6hp3mfmz5q8qkbpd
parent_id: is-01ks97vjxrmnzmxk6ke3hmt505
created_at: 2026-05-23T01:40:52.652Z
updated_at: 2026-05-23T01:42:26.866Z
---
First sub-bead in the Relevance epic. Output is a locked draft of the canonical content that every downstream sub-bead pulls from. User must sign off before downstream beads proceed.

## Deliverables

### 1. Guideline rules (draft)

For docs/practical-prose-guidelines.md §13:

1. **Cite only sources that bear on the document's purpose.** A source supplying tangential context can be referenced inline but should not be anchored as evidence for a headline claim.
2. **Cut intermediate reasoning that doesn't load-bear on the task.** If a section can be removed without changing any headline conclusion or actionable step, it's extraneous.
3. **Mark digressions as digressions.** If a section is included for completeness but not load-bearing, signal it with a 'Background' / 'Related work' / 'Aside' header so the reader can skip.
4. **Each source's contribution should be statable in one sentence.** If you can't say 'this source supports claim X relevant to purpose Y,' cut the source.
5. **Don't pad bibliographies for performative-rigor reasons.** Cite the sources that earned their place; performative citation is a form of fake rigor.

### 2. Rubric anchors (from user spec)

For docs/practical-prose-rubric.md §13:

- **NA:** Document has no sources or reasoning chains (rare — pure data dumps).
- **0:** Cannot assess.
- **1:** Half or more sources or reasoning chains are irrelevant to the document's conclusions or purpose.
- **2:** A significant fraction of sources or reasoning points are ancillary or extraneous to the purpose.
- **3:** In between — workable; some material doesn't fully earn its place.
- **4:** A few sources or notes are a bit of a stretch (cited for completeness or as digressions) but still loosely relevant.
- **5:** Every source and line of reasoning is relevant to the purpose; nothing can be removed without lowering the quality of the work.

### 3. Metric row

For docs/practical-prose-metrics.md:

- Quantitative: count of cited sources flagged as ancillary/tangential to the purpose; count of unmarked digressions exceeding N words; count of sections marked digression/background that load-bear on a headline claim (mislabel).
- Qualitative: 'For each source and each section, does it bear on the document's purpose?'
- Tooling: LLM-assist; manual.

### 4. Profile placement

For docs/practical-prose-metrics.md Applicability Profiles table:

- Low-stakes: typically NA (short notes don't have meaningful source sets).
- Standard: conditional (when doc cites sources or has reasoning).
- High: required.
- Reference/runbook: required (irrelevant references confuse readers).

### 5. Cross-reference notes

Relevance vs §2 Scope, vs §7 Concision, vs §11 Verifiability, vs §12 Factuality, and (if landed) vs §16 Parsimony. Each gets a one-sentence distinguisher in the guidelines text.

## Acceptance

User signs off on the locked draft. All downstream sub-beads (R2-R11) then pull this content verbatim into their files.
