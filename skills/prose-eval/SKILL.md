---
name: prose-eval
description: Score one practical document with metrics and rubric grading; read-only on source. Use when asked to score, evaluate, grade, rubric-check, or measure quality.
---
# Evaluate One Practical Prose Document

This is read-only on the source document. It writes eval report files.

Use it when the user wants a formal Practical Prose evaluation of one document.

## Inputs

- Path to one Markdown artifact.
- Artifact label.
- Scope class: `status`, `memo`, `brief`, `deep_research`, or `design_doc`.
- `ANTHROPIC_API_KEY` for model scoring, unless the user asks for dry-run or manual
  scoring only.

## Steps

1. Read `../../runbooks/practical-prose-eval-single.runbook.md`.
2. Generate the eval stub:

   ```bash
   uvx prose-eval report from-metrics path/to/artifact.md --label NAME --scope-class brief --out artifact.eval.md
   ```

3. Inspect deterministic metrics:

   ```bash
   uvx prose-eval metrics path/to/artifact.md --format yaml
   ```

4. Score the qualitative dimensions:

   ```bash
   uvx prose-eval score artifact.eval.md
   ```

5. Validate the result:

   ```bash
   uvx prose-eval report validate artifact.eval.md --complete
   ```

For local development before publication, run the same subcommands with
`cd tools/prose-eval && uv run prose-eval ...`.

## Output

Return the eval report path, validation result, and any scoring or alignment issues that
need human review.
