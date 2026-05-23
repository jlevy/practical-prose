---
type: is
id: is-01ks97xacz7gyeyycb8ggn697e
title: Regenerate .eval.md test fixtures and golden expected-comparison.md for Relevance
kind: chore
status: open
priority: 2
version: 2
labels:
  - rubric-rollout
  - relevance
  - tests
dependencies:
  - type: blocks
    target: is-01ks97yme61jy7g3wwczpt9fy0
parent_id: is-01ks97vjxrmnzmxk6ke3hmt505
created_at: 2026-05-23T01:41:33.214Z
updated_at: 2026-05-23T01:42:27.444Z
---
Same regeneration work as the Parsimony equivalent (pp-6iju). If Parsimony's regen has already landed, this bead extends the same 19-dim fixtures to 20-dim; if Relevance lands alone, it goes 18 → 19.

## Fixtures to regenerate (10 files in tools/prose-eval/tests/fixtures/)

- guidelines-self.eval.md
- rev1-net.eval.md
- rev2-net.eval.md
- figma-ddog-r1.eval.md, r2, r4
- figma-net-r1.eval.md, r2, r4

For each:
- Add `qual.grounding.relevance` and `qual_reasons.grounding.relevance`.
- Recompute `derived.rubric_rollup`.
- Bump `metadata.rubric_version` (19 or 20).
- Update body 'Overall mean (N dims)' (or rely on Parsimony's dynamic dim-count fix in eval_render.py).
- Add Relevance row to the qualitative table in the Grounding group.
- If Parsimony also present: include both new rows in correct positions.

## Golden file

- expected-comparison.md: regenerate from the updated fixtures. Add Relevance row in Grounding section after Factuality; recompute mean rollups.

## Approach

Same as P7 (pp-6iju): regen via `uv run prose-eval report from-metrics` + `score`, OR hand-patch YAML + run `uv run prose-eval compare` to regenerate the golden.

## Files touched

- tools/prose-eval/tests/fixtures/*.eval.md (10 files)
- tools/prose-eval/tests/fixtures/expected-comparison.md

## Depends on

pp-6lh8 (R3: Pydantic models), pp-gqa8 (R2: schema)
