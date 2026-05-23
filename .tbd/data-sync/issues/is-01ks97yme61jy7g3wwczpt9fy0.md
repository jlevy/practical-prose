---
type: is
id: is-01ks97yme61jy7g3wwczpt9fy0
title: "Validate Relevance rollout: lint, tests, end-to-end eval"
kind: task
status: closed
priority: 2
version: 2
labels:
  - rubric-rollout
  - relevance
  - validation
dependencies: []
parent_id: is-01ks97vjxrmnzmxk6ke3hmt505
created_at: 2026-05-23T01:42:16.261Z
updated_at: 2026-05-23T02:12:41.978Z
closed_at: 2026-05-23T02:12:41.978Z
close_reason: Implemented as part of the combined 20-dim-v1 rollout (commit on claude/vibrant-goldberg-828VB)
---
Final sub-bead. Run the full validation suite and an end-to-end smoke test before marking the epic done.

## Validation steps

1. **Lint:** `cd tools/prose-eval && uv run python devtools/lint.py`

2. **Tests:** `cd tools/prose-eval && uv run pytest` — expect all tests pass (including the golden comparison regen from R6).

3. **End-to-end smoke test:** Run a fresh metrics+score against one of the example texts (e.g. `example-texts/nasa-stakeholder-expectations-definition.md`):
   ```bash
   uv run prose-eval report from-metrics example-texts/nasa-stakeholder-expectations-definition.md
   uv run prose-eval score example-texts/nasa-stakeholder-expectations-definition.md.eval.md
   uv run prose-eval report validate example-texts/nasa-stakeholder-expectations-definition.md.eval.md
   ```
   Confirm: Relevance scored in the output; rubric_version reads the new version; report validates clean.

4. **Sanity check:** The NASA doc may score lower on Relevance than the SQLite doc — confirm the LLM is actually engaging with the new dimension and not just defaulting to 5s.

5. **Manual spot check:** Open the rendered eval report and confirm the Relevance row appears in the qualitative table in the Grounding group.

## Acceptance

All four pass cleanly. Mark the epic and all sub-beads closed.

## Depends on

All other sub-beads in the epic (R2-R10).
