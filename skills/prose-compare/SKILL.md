---
name: prose-compare
description: Compare evaluated document versions or variants; read-only on source docs. Use when asked to compare drafts, A/B versions, quality-diff docs, or pick the best.
---
# Compare Practical Prose Evaluations

This is read-only on source documents. It writes or prints comparison reports.

Use it after each input document already has a validated Practical Prose eval report.

## Inputs

- Paths to two or more validated `*.eval.md` reports.
- Optional labels or pair specs for deltas, such as `old=new`.

## Steps

1. Read `../../runbooks/practical-prose-eval-compare.runbook.md`.
2. Validate each input:

   ```bash
   uvx prose-eval report validate path/to/artifact.eval.md --complete
   ```

3. Generate the comparison:

   ```bash
   uvx prose-eval compare a.eval.md b.eval.md --format unified --pairs 'a=b' > comparison.md
   ```

4. Add human analytical prose only when the user asks for a full report, and ground it
   in specific table cells.

For local development before publication, run the same subcommands with
`cd tools/prose-eval && uv run prose-eval ...`.

## Output

Return the comparison path or table, validation status for each input, and any alignment
or rubric-version warnings.
