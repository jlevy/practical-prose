---
type: is
id: is-01ks97qev6jz44nkqjs438dwen
title: Regenerate .eval.md test fixtures and golden expected-comparison.md
kind: chore
status: closed
priority: 2
version: 3
labels:
  - rubric-rollout
  - parsimony
  - tests
dependencies:
  - type: blocks
    target: is-01ks97s25n1s058wk2nfqbtvx3
parent_id: is-01ks97m4tenhgn7w974et1nrnk
created_at: 2026-05-23T01:38:21.157Z
updated_at: 2026-05-23T02:12:37.266Z
closed_at: 2026-05-23T02:12:37.266Z
close_reason: Implemented as part of the combined 20-dim-v1 rollout (commit on claude/vibrant-goldberg-828VB)
---
Ten `.eval.md` fixture files in `tools/prose-eval/tests/fixtures/` each hardcode the dimension scores in YAML frontmatter, render 'Overall mean (18 dims)' in body text, and include the qualitative-table rows. All must be regenerated for the 19-dim (or 20-dim) rubric.

## Fixtures to regenerate

- guidelines-self.eval.md
- rev1-net.eval.md
- rev2-net.eval.md
- figma-ddog-r1.eval.md
- figma-ddog-r2.eval.md
- figma-ddog-r4.eval.md
- figma-net-r1.eval.md
- figma-net-r2.eval.md
- figma-net-r4.eval.md

For each: add `qual.judgment.parsimony` and `qual_reasons.judgment.parsimony`, recompute `derived.rubric_rollup`, bump `metadata.rubric_version` to 19-dim-v1, update body 'Overall mean (18 dims)' → '19 dims', add Parsimony row to the qualitative table.

## Golden file

- expected-comparison.md: byte-for-byte regression assertion in `test_golden_six_way_unified_with_pairs`. Regenerate from the updated fixtures. Add Parsimony row in Judgment section between Precision and Calibration; recompute mean rollups.

## Approach

Either:
- Regenerate via `uv run prose-eval report from-metrics` + `score` against the underlying source docs.
- Or hand-patch the YAML, then run `uv run prose-eval compare` to regenerate the golden.

## Files touched

- tools/prose-eval/tests/fixtures/*.eval.md (10 files)
- tools/prose-eval/tests/fixtures/expected-comparison.md (1 file)

## Depends on

pp-or98 (P3: Pydantic models accept new field), pp-jw8w (P2: rubric_version matches), pp-8wp0 (P5: dim-count rendering)
