---
type: is
id: is-01ks97y1tdc5cjhxakkbtj012a
title: "Update practical-prose-metrics.md for Relevance: add row + renumber + adjust profiles + version bump"
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
created_at: 2026-05-23T01:41:57.197Z
updated_at: 2026-05-23T01:42:28.333Z
---
Update docs/practical-prose-metrics.md.

## Changes

1. **Insert Relevance metric row** after the §12 Factuality row. Pull from R1: count of ancillary cited sources; count of unmarked digressions exceeding N words; count of mislabeled sections; qualitative check; LLM-assist + manual tooling.

2. **Renumber subsequent rows** (every §N row where N ≥ 13 shifts by 1).

3. **Update Applicability Profiles table** per R1: low-stakes typically NA; standard conditional; high required; reference/runbook required.

4. **Update version strings:** `18 review dimensions`, `18-dim-v1`, `18-dimension rubric` → 19 (or 20). Adjust all dimension cross-references.

5. **Update Fairness footnote** section number ref if §17 shifts to §18 or §19.

## Files touched

- docs/practical-prose-metrics.md (only)

## Depends on

pp-xt1p (R1: content)
