---
type: is
id: is-01ks97r0f8b0ad44w0z5xnccgw
title: Add §16 Parsimony anchors to practical-prose-rubric.md + renumber + bump rubric_version
kind: chore
status: closed
priority: 2
version: 3
labels:
  - rubric-rollout
  - parsimony
  - docs
dependencies:
  - type: blocks
    target: is-01ks97s25n1s058wk2nfqbtvx3
parent_id: is-01ks97m4tenhgn7w974et1nrnk
created_at: 2026-05-23T01:38:39.208Z
updated_at: 2026-05-23T02:12:37.851Z
closed_at: 2026-05-23T02:12:37.851Z
close_reason: Implemented as part of the combined 20-dim-v1 rollout (commit on claude/vibrant-goldberg-828VB)
---
Update docs/practical-prose-rubric.md with new §16 Parsimony score anchors, renumbering, and version bump.

## Changes

1. **Insert §16 Parsimony anchor section** after the §15 Precision anchors (around line 786). Body pulls from P1: NA, 0, 1, 2, 3, 4, 5 anchors plus the soundness-dependency note.

2. **Renumber subsequent anchor sections:**
   - `#### §16 Calibration` → `#### §17 Calibration`
   - `#### §17 Fairness` → `#### §18 Fairness`
   - `#### §18 Robustness` → `#### §19 Robustness`

3. **Update Dimensions table** (lines 147-166): insert row 16 for Parsimony; renumber Calibration=17, Fairness=18, Robustness=19.

4. **Update version strings:**
   - Frontmatter description (line 2): '18 dimensions' → '19 dimensions'
   - Line 9 `18-dim-v1` → `19-dim-v1`
   - Line 14 `the 18 dimensions` → `the 19 dimensions`
   - Lines 31-32 `(§1-§18)` → `(§1-§19)`
   - Line 1009 versioning guidance `18-dim-v1` → `19-dim-v1`
   - Other version-string mentions at lines 898, 925, 951, 961-966, 990, 998-1018

5. **Update Failure-Mode Questions table** (lines 217-225) and cross-refs at lines 623, 753, 873.

## Files touched

- docs/practical-prose-rubric.md (only)

## Depends on

pp-v2q7 (P1: content)
