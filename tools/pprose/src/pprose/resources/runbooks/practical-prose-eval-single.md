---
title: Practical Prose Eval, single-document runbook
description: End-to-end operational steps for evaluating one practical writing artifact and producing a validated pprose report.
date: 2026-05-07
last_updated: 2026-05-14
status: active
---
# Practical Prose Eval, Single-Document Runbook

Version: v0.1 (last update 2026-05-14)\
Joshua Levy (github.com/jlevy)

## Purpose

End-to-end operational steps for evaluating one practical writing artifact: run
quantitative metrics, score the 20 qualitative dimensions, cite guideline-rule
violations, produce a validated `<artifact>.eval.md` report.

The substance of *how* to score lives in `practical-prose-rubric.md` (anchors per
dimension, alignment principle, output format); this runbook covers what commands to
run, in what order, with what verification.

For comparing N evaluated artifacts, see `practical-prose-eval-compare.runbook.md`.

## Inputs and outputs

- **Input:** one Markdown artifact, the rubric (`practical-prose-rubric.md`), and the
  prescriptive guidelines (`practical-prose-guidelines.md`).
- **Output:** one `<artifact-name>.eval.md` validated against the schema in
  `pprose report` (`EvalReport`).

## Prerequisites

`pprose` available on the command line and `ANTHROPIC_API_KEY` set for scoring — see
[Tooling](../AGENTS.md#tooling). Batch eval outputs go under `evals/<round-name>/` at the
repo root.

## Steps

### 1. Generate the eval-report stub

```bash
pprose report from-metrics path/to/artifact.md --label NAME \
  --scope-class deep_research --out artifact.eval.md
```

This runs the metrics script internally, populates the `quant` block in schema-correct
shape, and stubs `qual` (all ERR = scorer-could-not-assess), `violations`, and
`metadata`.

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

For one-off raw metrics inspection without producing an eval report:

```bash
pprose metrics path/to/artifact.md --format=yaml
```

### 2. Score the 20 qualitative dimensions

Two paths. The model-scoring path is the default and is what the compare workflow
consumes; use the manual path for the first reviewer-level pass on a new doc class or
when calibrating the rubric.

**Model-scoring path (default):**

```bash
pprose score path/to/artifact.eval.md
```

This calls the Anthropic SDK with the rubric, guidelines, and artifact, parses the
structured JSON response, and fills the `qual` and `violations` blocks of the eval report
in place. The rubric and guidelines block is sent with prompt-caching enabled, so
subsequent calls (and `--batch` runs) reuse the cache and cost ~10× less than the first
call.
Useful flags:

- `--dry-run`: print the prompt to stdout without invoking the model.
- `--out path`: write the filled eval report to a different file.
- `--model <name>`: **required.** Pydantic AI model spec. Accepts short aliases
  (`opus`, `sonnet`, `haiku`, `gpt`, `gpt-mini`, `gemini`, ...) or a provider-
  prefixed string (`anthropic:claude-opus-4-7`, `openai:gpt-5.5`,
  `google:gemini-3.5-flash`). Run `pprose score --list-models` for the full
  suggested set; any other Pydantic AI model string is accepted too.
- `--list-models`: print the suggested model list and exit (no scoring).
- `--batch`: score multiple eval reports in one invocation:
  `pprose score a.eval.md b.eval.md ... --batch [--max-concurrent 8 --max-rps 4]`.
  See [practical-prose-eval-compare.runbook.md](practical-prose-eval-compare.runbook.md)
  for the typical batch workflow.

**Manual path:**

Read the artifact end to end.
For each of the 20 dimensions, assign a score 1-5 (or `NA` / `ERR`) per the anchors in
`practical-prose-rubric.md`. Use the `SCORE (REASON)` shape internally before composing
the eval report.

`NA` is reserved for dimensions the artifact’s task genuinely does not require. For
example, Calibration on a document that makes no probability or forecast claims, or
Fairness on a reference doc that surfaces no opposing positions.
`ERR` is reserved for procedural failures — the artifact is truncated mid-claim, an
upstream tool failed, the assigned model refused to score the dimension. Do not use
ERR to register a quality complaint; an attempted-but-empty dimension is a score of 1
with a rule citation, not ERR.

For any score below 5, identify at least one specific guideline-rule violation from
`practical-prose-guidelines.md`. Capture: the dimension by name, the rule number, a
one-line description, and a location pointer (line range like `L412-418`, section
heading like `§2.8`, or quoted phrase).

### 3. Fill the `qual`, `violations`, and `metadata` blocks

If you ran the model-scoring path in step 2, this is already done; skip to step 4.

If manual: open the eval report produced in step 1 and edit:

- `qual`: replace the all-ERR stubs with real 1-5 scores per group (`expression`,
  `purpose`, `grounding`, `reasoning`, `judgment`). Use `NA` where the dimension does
  not engage; leave `ERR` only when a procedural failure prevents scoring.
- `violations`: one entry per cited guideline-rule violation (dimension, rule_number,
  description, location).
- `metadata`: replace `evaluator: TODO` with the human or model-scoring identity; add
  optional `method` and `notes`. `eval_date` is pre-filled.

The `quant`, `derived`, and `artifact` blocks were generated in step 1; do not edit them
by hand. The schema validator recomputes `derived` from `quant` and `qual`.

### 4. Validate

```bash
pprose report validate path/to/artifact.eval.md
```

Expected: `OK: path/to/artifact.eval.md`. Common failures:

- Score outside 1-5 (and not `NA` / `ERR`)
- Missing dimension under `qual`
- `headings.total` doesn’t equal sum of `h1..h6`
- Unknown field (typos like `discipline:` misspelled)
- Unknown dimension or rule_number out of range under `violations`

Validation enforces the alignment principle: every score below 5 needs a matching cited
violation, and every score-5 (and every `NA` / `ERR`) needs none.

For the publish gate before feeding into a multi-doc comparison, add `--complete`:

```bash
pprose report validate path/to/artifact.eval.md --complete
```

`--complete` additionally requires `metadata.status='complete'`, evaluator set (not
`TODO`), `rubric_version` present, at least one dimension actually scored (not all
NA/ERR), and a reason in `qual_reasons` for every dimension scored 1-5. The
model-scoring path (step 2) sets these automatically.
`pprose compare` rejects draft / alignment-invalid inputs by default so the gate
effectively runs there too.

### 5. Optionally: render the per-artifact section

To preview the artifact’s section of the comparison Markdown (mostly useful for
eyeballing the derived rollups before adding to a multi-doc comparison):

```bash
pprose compare path/to/artifact.eval.md --format unified
```

This produces a 1-column “comparison” against just the one artifact.

## Alignment audit (before declaring the eval done)

- [ ] Every dimension scored below 5 has at least one violation cited.
- [ ] Every score-5, `NA`, and `ERR` has no violation in the read pass.
- [ ] Quantitative outliers from step 1 correlate with rubric findings.
- [ ] `pprose report validate` passes.

If the audit fails, revise scores or violations until consistent.

## Calibration set

`../tools/pprose/tests/fixtures/` ships a small calibration set with **agreed scores
and violations under `pp20v1`** (legacy `20-dim-v1` / `18-dim-v1-stale-baseline`
reports are still loaded; the eval loader migrates `score: 0` to `ERR` automatically)
so future agent or human evaluators can be tested for drift and self-eval overrating
against a fixed reference:

| Fixture | Artifact | Type | Overall mean | NA dims |
| --- | --- | --- | ---: | ---: |
| `rev1-net.eval.md` | External deep-research artifact (rev1) | strong baseline (deep_research) | ~4.1 | 0 |
| `rev2-net.eval.md` | External deep-research artifact (rev2 dry-run) | weaker baseline (deep_research) | ~3.1 | 0 |
| `guidelines-self.eval.md` | `practical-prose-guidelines.md` itself | self-eval (guidelines doc) | ~4.1 | 5 (Discipline, Parsimony, Calibration, Fairness, Robustness) |

Use this set to calibrate model-scoring runs:

```bash
pprose score path/to/your-artifact.eval.md --model opus
# then run pprose score against the calibration artifacts and compare overall_mean +
# per-dimension scores to the pinned values above; gap >0.5 on overall or >1 on any
# dimension flags a calibration drift to investigate.
```

The 6 `figma-*.eval.md` fixtures are comparison-renderer test data, not calibration
baselines: many dimensions were scored 0 on the original 12-dim eval because it did not
enumerate per-dim violations satisfying the alignment property. The loader migrates
those 0s to `ERR` on read of the legacy `rubric_version`.
To restore real scores, re-eval the underlying artifact under `pp20v1`.

Bump the calibration set whenever the rubric is bumped (`practical-prose-rubric.md`
§Versioning explains the trigger).
Re-score each fixture, update the table above, and commit together with the rubric
change.

## Related docs

- [practical-prose-rubric.md](../docs/practical-prose-rubric.md): per-dimension
  1-5 anchors (with `NA` / `ERR` sentinels) and scoring rules.
- [practical-prose-guidelines.md](../docs/practical-prose-guidelines.md):
  prescriptive rules cited by `violations`.
- [practical-prose-eval-compare.runbook.md](practical-prose-eval-compare.runbook.md):
  runbook for comparing N evals.
- [eval_report.py](../tools/pprose/src/pprose/eval_report.py): schema,
  validator, `from-metrics` stub generator.
- [eval_score.py](../tools/pprose/src/pprose/eval_score.py): model-scoring
  runner that fills
  `qual` and `violations`.
- [metrics.py](../tools/pprose/src/pprose/metrics.py): quantitative metrics
  tool.

<!-- This document follows common-doc-guidelines.md.
Review guidelines before editing.
-->
