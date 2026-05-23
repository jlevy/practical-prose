---
type: is
id: is-01ks97rbrhph4pbq49mhwp9xhz
title: "Update practical-prose-metrics.md: add Parsimony row + renumber + adjust profiles + version bump"
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
created_at: 2026-05-23T01:38:50.769Z
updated_at: 2026-05-23T01:39:40.747Z
---
Update docs/practical-prose-metrics.md to add the Parsimony metric row and the profile placements, plus renumbering.

## Changes

1. **Insert Parsimony metric row** (after §15 Precision, before §16 Calibration) in the Metrics by Dimension table (lines 50-52). Pull from P1:
   - Quantitative: count of chains where shorter sound chain exists; count of non-load-bearing rungs; per-doc parsimony-gap flag count.
   - Qualitative: 'For each load-bearing chain, is it the minimum sufficient given its purpose and per-step warrants?'
   - Tooling: LLM-assist; manual.

2. **Renumber subsequent rows:**
   - Row 16 Calibration → 17
   - Row 17 Fairness → 18
   - Row 18 Robustness → 19

3. **Update Applicability Profiles table** (lines 125-130) to reflect Parsimony placement per P1:
   - Low-stakes: typically NA
   - Standard: conditional (when doc makes inferential claims)
   - High: required
   - Reference/runbook: typically NA

4. **Update version strings:**
   - Lines 2-3 `18 review dimensions` → 19
   - Line 80-81 `18 dimensions` → 19
   - Line 107 `18-dim-v1` → `19-dim-v1`
   - Lines 118, 127-130 `18-dimension rubric`, dim cross-refs

5. **Update Fairness footnote** (lines 59-63): `§17 Fairness` → `§18 Fairness`; `§17.1` → `§18.1`.

## Files touched

- docs/practical-prose-metrics.md (only)

## Depends on

pp-v2q7 (P1: content)
