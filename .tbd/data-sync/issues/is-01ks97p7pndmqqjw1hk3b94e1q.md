---
type: is
id: is-01ks97p7pndmqqjw1hk3b94e1q
title: Add parsimony dimension to rubric_schema.yaml (single source of truth) + bump rubric version
kind: chore
status: open
priority: 2
version: 4
labels:
  - rubric-rollout
  - parsimony
  - schema
dependencies:
  - type: blocks
    target: is-01ks97pd2e5h9h8rgzyraxja9f
  - type: blocks
    target: is-01ks97pmpnytq5mjeg6becv852
  - type: blocks
    target: is-01ks97qev6jz44nkqjs438dwen
parent_id: is-01ks97m4tenhgn7w974et1nrnk
created_at: 2026-05-23T01:37:41.076Z
updated_at: 2026-05-23T01:39:37.764Z
---
Update tools/prose-eval/src/prose_eval/rubric_schema.yaml — the single source of truth for the rubric. Python code derives `DIMENSIONS`, `GROUPS`, and `dimension_count()` from this YAML at import time, so most code is dimension-agnostic.

## Changes

1. **Insert `parsimony` dimension entry** under the Reasoning group, between `precision` and `calibration`. Fields:
   - `key: parsimony`
   - `label: Parsimony`
   - `section: 16` (or 17 if Relevance lands first)
   - `question:` one-line scoring prompt (pull from P1 anchors)

2. **Renumber subsequent dimensions:**
   - calibration: section 16 → 17
   - fairness: section 17 → 18
   - robustness: section 18 → 19

3. **Bump version:** `version: 18-dim-v1` → `version: 19-dim-v1` (or `20-dim-v1` if Relevance is concurrent).

4. **Update `rule_counts`:** add `parsimony: 6` (matches the 6 rules from P1).

5. **Decide NA-eligibility for `parsimony`** — add to `na_applicable_dimensions` list. Per P1, NA when document makes no inferential claims.

## Files touched

- tools/prose-eval/src/prose_eval/rubric_schema.yaml (only)

## Depends on

pp-v2q7 (P1: canonical content lock)
