---
title: Practical Prose Eval, single-document runbook
description: End-to-end operational steps for evaluating one practical writing artifact and producing a validated eval-report YAML.
date: 2026-05-07
last_updated: 2026-05-10
status: active
---
# Practical Prose Eval, Single-Document Runbook

Version: v0.1 (last update 2026-05-11)\
Joshua Levy (github.com/jlevy)

## Purpose

End-to-end operational steps for evaluating one practical writing artifact: run
quantitative metrics, score the 18 qualitative dimensions, cite guideline-rule
violations, produce a validated `<artifact>.eval.yaml` report.

The substance of *how* to score lives in `practical-prose-rubric.md` (anchors per
dimension, alignment principle, output format); this runbook covers what commands to
run, in what order, with what verification.

For comparing N evaluated artifacts, see `practical-prose-eval-compare.runbook.md`.

## Inputs and outputs

- **Input:** one Markdown artifact + the rubric (`practical-prose-rubric.md`) + the
  prescriptive guidelines (`practical-prose-guidelines.md`).
- **Output:** one `<artifact-name>.eval.yaml` validated against the schema in
  `eval-report` (`EvalReport`).

## Setup

The eval tooling lives as an installable Python package at
[../tools/prose-eval/](../tools/prose-eval/). Install once:

```bash
cd tools/prose-eval && make install
```

This puts four console scripts on PATH inside the package’s `.venv`: `eval-report`,
`eval-score`, `eval-compare`, `prose-metrics`. Activate the venv (or use `uv run <cmd>`
from inside `tools/prose-eval/`) before running the commands below.

For batch eval audits, the convention is to store the `*.eval.yaml` outputs under
`evals/<round-name>/` at the repo root (e.g. `evals/self-eval-v0.1/`).

`eval-score` reads `ANTHROPIC_API_KEY` from the environment.
The entry point auto-loads `.env` / `.env.local` from the current directory and `$HOME`,
so the typical setup is:

```bash
echo 'ANTHROPIC_API_KEY=sk-ant-...' > .env   # gitignored
```

## Steps

### 1. Generate the YAML stub

```bash
eval-report from-metrics path/to/artifact.md --label NAME \
  --scope-class deep_research > artifact.eval.yaml
```

This runs the metrics script internally, populates the `quant` block in schema-correct
shape, and stubs `qual` (all zeros = “cannot assess”), `violations`, and `metadata`.

**Pick a `--scope-class`** so the comparison generator can flag density problems
relative to genre expectations.
Omitting it runs in diagnostic-only mode (density ratios are computed but no concerns
are surfaced). Choices:

| `--scope-class` | When to use | Density expectations |
| --- | --- | --- |
| `status` | Status updates, standups, brief progress notes | Few links / tags allowed |
| `memo` | Short decision memos, internal recommendations | ≥0.5 links / 1k words |
| `brief` | Research briefs, analyst notes | ≥1.0 links / 1k words |
| `deep_research` | Long-form research reports, theses, multi-section analyses | ≥1.0 links / 1k words and ≥0.3 tables / 1k words |
| `design_doc` | Technical design docs, architecture proposals, specs | ≥0.5 links / 1k words |

`scope_class` is a **density-threshold tag**, not a doc-type taxonomy.
The rubric’s list of practical-document types (articles, blog posts, technical papers,
decision memos, etc.)
is a descriptive framing of what the rubric applies to; `scope_class` is the narrower
axis the eval tooling uses to decide whether a particular artifact has the linking and
tabular density its genre expects.
Map the broader doc type onto the closest scope class above.

Inspect the populated `quant` block for outliers before scoring:

- **Zero links in a long document** → likely citation / reference failure
- **Very high word count with low heading count** → potential structure problem
- **Bracket tags present** → distinguish provenance markers from template placeholders
- **High `code_blocks` or `tables` count** → may affect prose density interpretation
- **Non-zero `lint.banned_register_hits`** → strong-register words flagged; verify each
  is earned by a citation, otherwise count it as a Clarity Rule 4 violation.

These signals feed the qualitative scoring; they don’t substitute for it.

For one-off raw metrics inspection without producing a YAML:

```bash
prose-metrics path/to/artifact.md --format=yaml
```

### 2. Score the 18 qualitative dimensions

Two paths. The model-scoring path is the default and is what the compare workflow
consumes; use the manual path for the first reviewer-level pass on a new doc class or
when calibrating the rubric.

**Model-scoring path (default):**

```bash
eval-score path/to/artifact.eval.yaml
```

This calls the Anthropic SDK with the rubric, guidelines, and artifact, parses the
structured JSON response, and fills the `qual` + `violations` blocks of the YAML in
place. The rubric + guidelines block is sent with prompt-caching enabled, so subsequent
calls (and `--batch` runs) reuse the cache and cost ~10× less than the first call.
Useful flags:

- `--dry-run` — print the prompt to stdout without invoking the model.
- `--out path` — write the filled YAML to a different file.
- `--model <name>` — passed to the Anthropic SDK. Accepts aliases (`sonnet`, `haiku`,
  `opus`) or an exact model ID. Defaults to the SDK’s default model.
- `--batch` — score multiple YAMLs in one invocation:
  `eval-score a.eval.yaml b.eval.yaml ... --batch [--max-concurrent 8 --max-rps 4]`. See
  [practical-prose-eval-compare.runbook.md](practical-prose-eval-compare.runbook.md) for
  the typical batch workflow.

**Manual path:**

Read the artifact end to end.
For each of the 18 dimensions, assign a score 0-5 (or `NA`) per the anchors in
`practical-prose-rubric.md`. Use the `SCORE (REASON)` shape internally before composing
the YAML.

`NA` is reserved for dimensions the artifact’s task genuinely does not require — for
example, Calibration on a document that makes no probability or forecast claims, or
Fairness on a reference doc that surfaces no opposing positions.
A score of 0 means the dimension is applicable but content is missing or unassessable;
do not confuse the two.

For any score below 5, identify at least one specific guideline-rule violation from
`practical-prose-guidelines.md`. Capture: the dimension by name, the rule number, a
one-line description, and a location pointer (line range like `L412-418`, section
heading like `§2.8`, or quoted phrase).

### 3. Fill the `qual`, `violations`, and `metadata` blocks

If you ran the model-scoring path in step 2, this is already done; skip to step 4.

If manual: open the YAML produced in step 1 and edit:

- `qual`: replace the all-zero stubs with real 0-5 scores per group (`expression`,
  `purpose`, `grounding`, `reasoning`, `judgment`). Score 0 means “cannot assess”; leave
  0 only for genuinely-missing-content cases.
- `violations`: one entry per cited guideline-rule violation (dimension, rule_number,
  description, location).
- `metadata`: replace `evaluator: TODO` with the human or model-scoring identity; add
  optional `method` and `notes`. `eval_date` is pre-filled.

The `quant`, `derived`, and `artifact` blocks were generated in step 1; do not edit them
by hand. The schema validator recomputes `derived` from `quant` + `qual`.

### 4. Validate

```bash
eval-report validate path/to/artifact.eval.yaml
```

Expected: `OK: path/to/artifact.eval.yaml`. Common failures:

- Score outside 0-5
- Missing dimension under `qual`
- `headings.total` doesn’t equal sum of `h1..h6`
- Unknown field (typos like `discipline:` misspelled)
- Unknown dimension or rule_number out of range under `violations`

Validation enforces the alignment principle: every score below 5 needs a matching cited
violation, and every score-5 (or score-0 = “cannot assess”) needs none.

For the publish gate before feeding into a multi-doc comparison, add `--complete`:

```bash
eval-report validate path/to/artifact.eval.yaml --complete
```

`--complete` additionally requires `metadata.status='complete'`, evaluator set (not
`TODO`), `rubric_version` present, no all-zero stubs, and a reason in `qual_reasons` for
every dimension scored 1-5. The model-scoring path (step 2) sets these automatically.
`eval-compare` rejects draft / alignment-invalid inputs by default so the gate
effectively runs there too.

### 5. Optionally: render the per-artifact section

To preview the artifact’s section of the comparison Markdown (mostly useful for
eyeballing the derived rollups before adding to a multi-doc comparison):

```bash
eval-compare path/to/artifact.eval.yaml --format unified
```

This produces a 1-column “comparison” against just the one artifact.

## Alignment audit (before declaring the eval done)

- [ ] Every dimension scored below 5 has at least one violation cited.
- [ ] Every score-5, score-0, and `NA` has no violation in the read pass.
- [ ] Quantitative outliers from step 1 correlate with rubric findings.
- [ ] `eval_report.py validate` passes.

If the audit fails, revise scores or violations until consistent.

## Calibration set

`../tools/prose-eval/tests/fixtures/` ships a small calibration set with **agreed scores
and violations under `18-dim-v1`** so future agent or human evaluators can be tested for
drift and self-eval overrating against a fixed reference:

| Fixture | Artifact | Type | Overall mean | NA dims |
| --- | --- | --- | ---: | ---: |
| `rev1-net.eval.yaml` | External deep-research artifact (rev1) | strong baseline (deep_research) | ~4.1 | 0 |
| `rev2-net.eval.yaml` | External deep-research artifact (rev2 dry-run) | weaker baseline (deep_research) | ~3.1 | 0 |
| `guidelines-self.eval.yaml` | `practical-prose-guidelines.md` itself | self-eval (guidelines doc) | ~4.1 | 4 (Inference Discipline, Calibration, Fairness, Robustness) |

Use this set to calibrate model-scoring runs:

```bash
eval-score path/to/your-artifact.eval.yaml --model sonnet
# then run eval_score against the calibration artifacts and compare overall_mean +
# per-dimension scores to the pinned values above; gap >0.5 on overall or >1 on any
# dimension flags a calibration drift to investigate.
```

The 6 `figma-*.eval.yaml` fixtures are comparison-renderer test data, not calibration
baselines: many dimensions are scored 0 because the original 12-dim eval did not
enumerate per-dim violations satisfying the 18-dim-v1 alignment property.
To restore those scores, re-eval the underlying artifact under 18-dim-v1.

Bump the calibration set whenever the rubric is bumped (`practical-prose-rubric.md`
§Versioning explains the trigger).
Re-score each fixture, update the table above, and commit together with the rubric
change.

## Related docs

- [practical-prose-rubric.md](../docs/practical-prose-rubric.md): per-dimension
  0-5 anchors and scoring rules.
- [practical-prose-guidelines.md](../docs/practical-prose-guidelines.md):
  prescriptive rules cited by `violations`.
- [practical-prose-eval-compare.runbook.md](practical-prose-eval-compare.runbook.md):
  runbook for comparing N evals.
- [eval_report.py](eval-report): schema, validator, `from-metrics` stub generator.
- [eval_score.py](eval-score): model-scoring runner (calls `claude` CLI) that fills
  `qual` + `violations`.
- [practical_prose_metrics.py](prose-metrics): quantitative metrics tool.

<!-- This document follows common-doc-guidelines.md.
Review guidelines before editing.
-->
