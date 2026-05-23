---
type: is
id: is-01ks97qrtgbfkphsyhd1tb0spf
title: Add §16 Parsimony to practical-prose-guidelines.md + renumber §16-§18 → §17-§19
kind: chore
status: open
priority: 2
version: 2
labels:
  - rubric-rollout
  - parsimony
  - docs
dependencies:
  - type: blocks
    target: is-01ks97s25n1s058wk2nfqbtvx3
parent_id: is-01ks97m4tenhgn7w974et1nrnk
created_at: 2026-05-23T01:38:31.376Z
updated_at: 2026-05-23T01:39:40.150Z
---
Update docs/practical-prose-guidelines.md: add the new §16 section, renumber three subsequent dims, and fix all inline cross-references.

## Changes

1. **Insert new `### 16. Parsimony`** section after the existing §15 Precision (around line 786). Body pulls from P1 locked content (description + 6 rules + cross-reference notes vs Concision/Discipline/Soundness/Precision).

2. **Renumber subsequent dimension headings:**
   - `### 16. Calibration` → `### 17. Calibration` (line 793)
   - `### 17. Fairness` → `### 18. Fairness` (line 834)
   - `### 18. Robustness` → `### 19. Robustness` (line 879)

3. **Update dimension table** (lines 30-50) to add the Parsimony row and adjust Judgment group entries.

4. **Fix inline cross-references:**
   - Line 70: `lenses (§16-§18)` → `(§17-§19)`
   - Line 709: `Fairness (§17)` → `Fairness (§18)`
   - Line 908: `Fairness (§17)` → `(§18)`
   - Lines 930, 958, 973, 989, 1006: various `§16`, `§17`, `§18` references

## Files touched

- docs/practical-prose-guidelines.md (only)

## Depends on

pp-v2q7 (P1: content)
