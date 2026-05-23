---
type: is
id: is-01ks97xwbrn363f1mnbm2pptwm
title: Add §13 Relevance anchors to practical-prose-rubric.md + renumber + bump rubric_version
kind: chore
status: open
priority: 2
version: 2
labels:
  - rubric-rollout
  - relevance
  - docs
dependencies:
  - type: blocks
    target: is-01ks97yme61jy7g3wwczpt9fy0
parent_id: is-01ks97vjxrmnzmxk6ke3hmt505
created_at: 2026-05-23T01:41:51.607Z
updated_at: 2026-05-23T01:42:28.027Z
---
Update docs/practical-prose-rubric.md.

## Changes

1. **Insert §13 Relevance anchor section** after §12 Factuality. Body pulls from R1: NA, 0, 1, 2, 3, 4, 5 anchors.

2. **Renumber subsequent anchor sections** (every §N where N ≥ 13 shifts by 1):
   - §13 Inference Discipline → §14
   - §14 Soundness → §15
   - §15 Precision → §16
   - §16 Calibration → §17 (or 18 if Parsimony at 16)
   - §17 Fairness → §18 (or 19)
   - §18 Robustness → §19 (or 20)

3. **Update Dimensions table:** insert row 13 for Relevance; renumber subsequent.

4. **Update version strings:**
   - Frontmatter description: '18 dimensions' → 19 (or 20)
   - `18-dim-v1` → `19-dim-v1` everywhere
   - `(§1-§18)` → `(§1-§19)`
   - Versioning section guidance lines

5. **Update Failure-Mode Questions table** and any cross-refs to §13+ sections.

## Files touched

- docs/practical-prose-rubric.md (only)

## Coordination

Same as the guidelines bead — final numbering depends on whether Parsimony already landed. Schema bead R2 (pp-gqa8) settles the canonical numbering before this runs.

## Depends on

pp-xt1p (R1: content)
