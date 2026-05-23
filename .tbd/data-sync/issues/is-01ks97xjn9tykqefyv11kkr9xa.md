---
type: is
id: is-01ks97xjn9tykqefyv11kkr9xa
title: Add §13 Relevance to practical-prose-guidelines.md + renumber §13-§18 → §14-§19
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
created_at: 2026-05-23T01:41:41.672Z
updated_at: 2026-05-23T01:42:27.733Z
---
Update docs/practical-prose-guidelines.md.

## Changes

1. **Insert new `### 13. Relevance`** section after §12 Factuality. Body pulls from R1 (description + 5 rules + cross-reference notes vs Scope/Concision/Verifiability/Factuality/Parsimony).

2. **Renumber subsequent dimension headings:**
   - `### 13. Inference Discipline` → `### 14. Inference Discipline`
   - `### 14. Soundness` → `### 15. Soundness`
   - `### 15. Precision` → `### 16. Precision`
   - `### 16. Calibration` → `### 17. Calibration` (or 18 if Parsimony at 16)
   - `### 17. Fairness` → `### 18. Fairness` (or 19)
   - `### 18. Robustness` → `### 19. Robustness` (or 20)

3. **Update dimension table** to include the Relevance row.

4. **Fix inline cross-references:** every `§N` ref where N ≥ 13 must be incremented by 1.

## Files touched

- docs/practical-prose-guidelines.md (only)

## Coordination

If Parsimony epic already landed (so Parsimony is at §16), then §13-§15 shift +1 here (Inference Discipline → 14, Soundness → 15, Precision → 16... wait, that conflicts with Parsimony at 16). Re-coordinate: Relevance shifts §13-§15 to §14-§16; then Parsimony at §16 needs to become §17, and so on. The R1 (content lock) and R2 (schema) beads handle the final numbering; this bead applies whatever R2 settled on.

## Depends on

pp-xt1p (R1: content)
