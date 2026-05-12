---
title: Practical Prose Eval, multi-document comparison runbook
description: Operational steps for producing a unified comparison Markdown report from N validated single-doc eval reports.
date: 2026-05-07
last_updated: 2026-05-10
status: active
---
# Practical Prose Eval, Multi-Document Comparison Runbook

Version: v0.1 (last update 2026-05-10)\
Joshua Levy (github.com/jlevy)

## Purpose

Produce a unified comparison Markdown from N evaluated artifacts: unified table
(qualitative scores + quantitative metrics + derived ratios), optional per-section
drilldowns, and per-pair deltas.
The deterministic generator is `../scripts/eval_compare.py`; this runbook wraps it with
the alignment audit and the analytical-prose layer the generator cannot produce.

For an exact rendering of the generator’s output shape, see
`../scripts/fixtures/expected-comparison.md` — the golden output that
`../scripts/test_eval_compare.py` pins against the six `figma-*.eval.yaml` fixtures.

## Inputs and outputs

- **Input:** N validated `<artifact>.eval.yaml` files (each produced by
  `practical-prose-eval-single.runbook.md`).
- **Output:** one comparison Markdown combining the generator’s table with
  reviewer-authored cross-artifact analysis.

## Steps

Commands below assume the working directory is this runbook’s directory (`runbooks/`),
so `../scripts/...` resolves into the bundle.
Run from elsewhere by substituting the full bundle path.

### 1. Score each artifact

For each artifact, run the single-doc runbook (`practical-prose-eval-single.runbook.md`)
end to end. The output of that runbook is the input to this one.

### 2. Confirm each input is validated

```bash
for f in path/to/*.eval.yaml; do
  ../scripts/eval_report.py validate "$f" || break
done
```

Each file should print `OK: <path>`. Do not proceed if any fail.

### 3. Generate the comparison Markdown

```bash
../scripts/eval_compare.py \
  path/to/a.eval.yaml \
  path/to/b.eval.yaml \
  path/to/c.eval.yaml \
  --format unified \
  --pairs 'a=b' 'b=c' \
  > comparison.md
```

Flags:

- `--format unified` — single combined table (default; matches the reference shape).
  Use `--format sections` for per-section drilldowns, `--format both` for both.
- `--bold-rule max` — bold per-row max(es) when not all artifacts tie (default).
  Use `--bold-rule materially-different` for a stricter rule (max must be ≥ 1 above the
  median).
- `--pairs 'from=to' ...` — emit Δ tables for each pair, dimension by dimension, plus
  mean delta. Useful for “process A → process B” comparisons.

### 4. Verify the alignment audit across artifacts

The generator emits the table mechanically; confirm the alignment principle holds across
all artifacts:

- [ ] Every below-5 score in any artifact has at least one cited violation in that
  artifact’s YAML.
- [ ] Every score-5 has no cited violation.
- [ ] Quantitative outliers (e.g. one artifact with 0 inline links in a long doc)
  correlate with rubric findings (Structure score below 5 with Rule 5 cited).
- [ ] No “score 5 with violation” or “score below 5 with no violation” gaps.

If the audit fails for any artifact, return to that artifact’s single-doc runbook step 4
and revise.

### 5. Append cross-artifact analysis prose

The generator stops at the table + delta blocks.
Author the analytical prose on top, in this order (matches the reference report):

1. **Scope and method:** what artifacts are being compared and why, what is reused vs
   fresh, what rubric version was used.
2. **Headline quantitative observations:** 3-7 numbered observations the table reveals
   (e.g. “rev2 has 0 inline links across both tickers, a discrete drop from rev1”).
3. **Per-revision deltas (interpretation):** for each pair in `--pairs`, one paragraph
   explaining what the deltas reveal.
4. **Cross-artifact patterns:** invariants and trends that span all artifacts (e.g.
   “sentence length is stable across all 6 artifacts; paragraph length is the variable
   lever”).
5. **Verdict:** which artifact or process should the reader pick, and why?
   What is left to fix in a hypothetical next revision?
6. **Reproducibility footer:** eval date, evaluator, method, list of YAMLs consumed, and
   the exact command used to generate the table.

Aim for falsifiable claims grounded in specific table cells, not generic.

### 6. Save the report

- One-off comparisons: save alongside the artifacts being compared (one directory per
  topic / eval).
- Ongoing alignment-regression tracking: pin the expected scores in the single-doc
  runbook’s regression fixtures (`../scripts/fixtures/`) and cite this report.

## Alignment audit (before declaring the comparison done)

- [ ] Every input YAML validated.
- [ ] Generator ran without warnings (including cross-rubric-version warnings).
- [ ] Cross-artifact alignment audit passed.
- [ ] Analytical prose grounded in specific table cells.
- [ ] Reproducibility footer includes the exact command.

## Related docs

- [practical-prose-eval-single.runbook.md](practical-prose-eval-single.runbook.md):
  produces the YAML inputs this runbook consumes.
- [practical-prose-rubric.md](../docs/practical-prose-rubric.md): per-dimension 0-5
  anchors and scoring rules.
- [practical-prose-guidelines.md](../docs/practical-prose-guidelines.md): prescriptive
  rules cited by violations.
- [eval_compare.py](../scripts/eval_compare.py): the deterministic generator.
- [eval_report.py](../scripts/eval_report.py): schema and validator.

<!-- This document follows std-doc-guidelines.md.
Review guidelines before editing.
-->
