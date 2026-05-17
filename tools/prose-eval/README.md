# prose-eval

`prose-eval` is the Practical Prose evaluation CLI. It combines deterministic document
metrics with rubric-based model scoring and comparison reports.

## Commands

Run from this package workspace during local development:

```bash
uv run prose-eval metrics path/to/document.md
uv run prose-eval report from-metrics path/to/document.md --label NAME --scope-class brief --out NAME.eval.md
uv run prose-eval score NAME.eval.md
uv run prose-eval report validate NAME.eval.md --complete
uv run prose-eval compare *.eval.md --format unified
```

The package also exposes compatibility entry points:

- `prose-metrics`
- `eval-report`
- `eval-score`
- `eval-compare`

Prefer the grouped `prose-eval ...` command in new docs and workflows.

## Model Scoring

`prose-eval score` uses the Anthropic SDK and reads `ANTHROPIC_API_KEY` from the
environment. It also auto-loads `.env` and `.env.local` from the current directory
hierarchy and `$HOME`.

The scorer prompt includes:

- `docs/practical-prose-rubric.md`
- `docs/practical-prose-guidelines.md`
- deterministic metrics from the eval report
- the artifact under review

Rubric and guideline content are sent in a cached prompt block; the metrics and artifact
remain uncached because they vary by document.

## Development

```bash
make install
uv run pytest
uv run python devtools/lint.py
```

The package includes runtime data files under `src/prose_eval/`, including
`rubric_schema.yaml` and prompt templates in `src/prose_eval/prompts/`.
