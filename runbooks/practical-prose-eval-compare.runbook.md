---
title: Practical Prose Eval, multi-document comparison runbook
description: Operational steps for producing a unified comparison Markdown report from N validated single-doc eval reports.
date: 2026-05-07
last_updated: 2026-05-14
status: active
---
# Practical Prose Eval, Multi-Document Comparison Runbook

Version: v0.1 (last update 2026-05-14)\
Joshua Levy (github.com/jlevy)

## Purpose

Produce a unified comparison Markdown from N evaluated artifacts: unified table
(qualitative scores + quantitative metrics + derived ratios), optional per-section
drilldowns, and per-pair deltas.
The deterministic generator is `prose-eval compare`; this runbook wraps it with the
alignment audit and the analytical-prose layer the generator cannot produce.

For an exact rendering of the generator’s output shape, see
`../tools/prose-eval/tests/fixtures/expected-comparison.md`: the golden output that
`../tools/prose-eval/tests/test_eval_compare.py` pins against the six
`figma-*.eval.md` fixtures.

## Inputs and outputs

- **Input:** N validated `<artifact>.eval.md` files (each produced by
  `practical-prose-eval-single.runbook.md`).
- **Output:** one comparison Markdown combining the generator’s table with
  reviewer-authored cross-artifact analysis.

## Setup

The eval tooling lives as an installable Python package at
[../tools/prose-eval/](../tools/prose-eval/). Install once
(`cd tools/prose-eval && make install`) and use the `prose-eval` console script with
the `score`, `report`, and `compare` subcommands.

Batch eval outputs live under `evals/<round-name>/` at the repo root.

## Steps

### 1. Score each artifact

For a one-off run on a single artifact: see
[practical-prose-eval-single.runbook.md](practical-prose-eval-single.runbook.md).

For a multi-artifact batch (the common case for this runbook), score all artifacts in
one invocation using the `--batch` flag:

```bash
prose-eval score evals/<round>/*.eval.md --batch --max-concurrent 8 --max-rps 4
```

This fans out the SDK calls under `gather_limited` (an `asyncio.Semaphore`
+ `aiolimiter` leaky bucket).
  Defaults: `--max-concurrent 8`, `--max-rps 4`.

**Prompt caching**: the rubric + guidelines + instructions block is marked
`cache_control: ephemeral`, so once one call has written the cache, others within ~5
minutes read it at ~0.1× the input cost.
Observed batch run on 12 docs (this repo’s self-eval-v0.2): **~1m33s wall-clock** vs ~4
hours sequential in round 1. Note: when many calls fire simultaneously and no prior
cache exists, each independently creates the cache; cache *hits* land on docs that
arrive after at least one cache-creating call has completed.

**Expect occasional alignment failures.** The validator may drop a violation whose
`rule_number` is out of range for its dimension (F3a softening), which can orphan a
sub-5 score and fail alignment for that doc.
Failed docs leave their raw responses at `<name>.eval.raw.txt` for recovery.
Either rescore the failed doc(s) individually (model variance often clears it on retry),
or pass `--allow-misaligned` for human review.

### 2. Confirm each input is validated

```bash
for f in path/to/*.eval.md; do
  prose-eval report validate "$f" || break
done
```

Each file should print `OK: <path>`. Do not proceed if any fail.

### 3. Generate the comparison Markdown

```bash
prose-eval compare \
  path/to/a.eval.md \
  path/to/b.eval.md \
  path/to/c.eval.md \
  --format unified \
  --pairs 'a=b' 'b=c' \
  > comparison.md
```

Flags:

- `--format unified`: single combined table (default; matches the reference shape).
  Use `--format sections` for per-section drilldowns, `--format both` for both.
- `--bold-rule max`: bold per-row max(es) when not all artifacts tie (default).
  Use `--bold-rule materially-different` for a stricter rule (max must be ≥ 1 above the
  median).
- `--pairs 'from=to' ...`: emit Δ tables for each pair, dimension by dimension, plus
  mean delta. Useful for “process A → process B” comparisons.

### 4. Verify the alignment audit across artifacts

The generator emits the table mechanically; confirm the alignment principle holds across
all artifacts:

- [ ] Every below-5 score in any artifact has at least one cited violation in that
  artifact's eval report.
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
6. **Reproducibility footer:** eval date, evaluator, method, list of eval reports
   consumed, and the exact command used to generate the table.

Aim for falsifiable claims grounded in specific table cells, not generic.

### 6. Save the report

- One-off comparisons: save alongside the artifacts being compared (one directory per
  topic / eval).
- Ongoing alignment-regression tracking: pin the expected scores in the single-doc
  runbook’s regression fixtures (`../tools/prose-eval/tests/fixtures/`) and cite this
  report.

## Alignment audit (before declaring the comparison done)

- [ ] Every input eval report validated.
- [ ] Generator ran without warnings (including cross-rubric-version warnings).
- [ ] Cross-artifact alignment audit passed.
- [ ] Analytical prose grounded in specific table cells.
- [ ] Reproducibility footer includes the exact command.

## Related docs

- [practical-prose-eval-single.runbook.md](practical-prose-eval-single.runbook.md):
  produces the eval reports this runbook consumes.
- [practical-prose-rubric.md](../docs/practical-prose-rubric.md): per-dimension 0-5
  anchors and scoring rules.
- [practical-prose-guidelines.md](../docs/practical-prose-guidelines.md): prescriptive
  rules cited by violations.
- [eval_compare.py](../tools/prose-eval/src/prose_eval/eval_compare.py): the
  deterministic generator.
- [eval_report.py](../tools/prose-eval/src/prose_eval/eval_report.py): schema and
  validator.

<!-- This document follows common-doc-guidelines.md.
Review guidelines before editing.
-->
