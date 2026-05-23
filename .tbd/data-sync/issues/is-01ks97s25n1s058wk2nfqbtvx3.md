---
type: is
id: is-01ks97s25n1s058wk2nfqbtvx3
title: "Validate Parsimony rollout: lint, tests, end-to-end eval"
kind: task
status: closed
priority: 2
version: 2
labels:
  - rubric-rollout
  - parsimony
  - validation
dependencies: []
parent_id: is-01ks97m4tenhgn7w974et1nrnk
created_at: 2026-05-23T01:39:13.717Z
updated_at: 2026-05-23T02:12:38.719Z
closed_at: 2026-05-23T02:12:38.719Z
close_reason: Implemented as part of the combined 20-dim-v1 rollout (commit on claude/vibrant-goldberg-828VB)
---
Final sub-bead. Run the full validation suite and an end-to-end smoke test before marking the epic done.

## Validation steps

1. **Lint:**
   ```bash
   cd tools/prose-eval && uv run python devtools/lint.py
   ```

2. **Tests:**
   ```bash
   cd tools/prose-eval && uv run pytest
   ```
   Expect: all tests pass (including the golden comparison regen from P7).

3. **End-to-end smoke test:** Run a fresh metrics+score against one of the example texts (e.g. `example-texts/sqlite-appropriate-uses.md`):
   ```bash
   uv run prose-eval report from-metrics example-texts/sqlite-appropriate-uses.md
   uv run prose-eval score example-texts/sqlite-appropriate-uses.md.eval.md
   uv run prose-eval report validate example-texts/sqlite-appropriate-uses.md.eval.md
   ```
   Confirm: Parsimony scored in the output; rubric_version reads `19-dim-v1`; report validates clean.

4. **Sanity check rubric self-eval:** Run the self-eval against the updated guidelines doc and confirm Parsimony scores reasonably (probably 4 or 5 — the guideline doc itself should not have non-parsimonious chains).

5. **Manual spot check:** Open the rendered eval report for sqlite-appropriate-uses and confirm the Parsimony row appears in the qualitative table in the right place.

## Acceptance

All four pass cleanly. Then mark the epic and all sub-beads closed.

## Depends on

All other sub-beads in the epic (P2-P11).
