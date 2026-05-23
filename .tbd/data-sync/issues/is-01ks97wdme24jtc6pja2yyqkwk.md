---
type: is
id: is-01ks97wdme24jtc6pja2yyqkwk
title: Add relevance dimension to rubric_schema.yaml at §13 + renumber §13-§18 → §14-§19 + bump version
kind: chore
status: open
priority: 2
version: 4
labels:
  - rubric-rollout
  - relevance
  - schema
dependencies:
  - type: blocks
    target: is-01ks97whzq6pr6kdgw01bk87x1
  - type: blocks
    target: is-01ks97ws5fabst53vaqba9vdfk
  - type: blocks
    target: is-01ks97xacz7gyeyycb8ggn697e
parent_id: is-01ks97vjxrmnzmxk6ke3hmt505
created_at: 2026-05-23T01:41:03.758Z
updated_at: 2026-05-23T01:42:25.639Z
---
Update tools/prose-eval/src/prose_eval/rubric_schema.yaml — the single source of truth.

## Changes

1. **Insert `relevance` dimension entry** under the Grounding group, between `factuality` and the next dim. Fields:
   - `key: relevance`
   - `label: Relevance`
   - `section: 13`
   - `question:` one-line scoring prompt (pull from R1 anchors)

2. **Renumber subsequent dimensions** (shift by 1):
   - inference_discipline: 13 → 14
   - soundness: 14 → 15
   - precision: 15 → 16
   - calibration: 16 → 17 (or 18 if Parsimony already at 16)
   - fairness: 17 → 18 (or 19)
   - robustness: 18 → 19 (or 20)
   - Plus parsimony (if landed): 16 → 17.

3. **Bump version:** `version: 18-dim-v1` → `version: 19-dim-v1` (or 20-dim-v1 if Parsimony concurrent).

4. **Update `rule_counts`:** add `relevance: 5` (matches the 5 rules from R1).

5. **Decide NA-eligibility for `relevance`** — add to `na_applicable_dimensions` per R1.

## Files touched

- tools/prose-eval/src/prose_eval/rubric_schema.yaml (only)

## Coordination

If Parsimony epic (pp-38s0) lands first, this bead must account for the new ordering (Parsimony at §16, others shifted). Adjust section numbers accordingly.

## Depends on

pp-xt1p (R1: canonical content lock)
