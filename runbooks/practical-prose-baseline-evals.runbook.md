---
title: Practical Prose Baseline Eval Runbook
description: Operational steps for evaluating the third-party example texts and the repo's self-eval docs as one default baseline set, with optional subset runs.
date: 2026-05-14
status: active
---
# Practical Prose Baseline Eval Runbook

Version: v0.1 (last update 2026-05-14)\
Joshua Levy (github.com/jlevy)

## Purpose

Generate and compare baseline Practical Prose evals for the reference artifacts in this
repo. The default run evaluates **all baseline artifacts**:

- the third-party example texts in `example-texts/`
- the self-eval docs in `docs/`

Use the subset commands only when you are debugging one side of the baseline set.

## Using the `pprose` Skill

When asking an agent to run this workflow, invoke the local `pprose` skill and point
it at this runbook:

> Use `pprose` and run `runbooks/practical-prose-baseline-evals.runbook.md`.

Unless the request names a subset, run **Default: Run All Baselines**. Subset runs are
available for debugging, but the ordinary baseline process should regenerate third-party
and self-eval reports together so the comparison files stay aligned.

## Artifact Sets

| Set | Artifact | Label | Scope class | Output |
| --- | --- | --- | --- | --- |
| third-party | `example-texts/sqlite-appropriate-uses.md` | `SQLite: Appropriate Uses` | `brief` | `evals/baselines/third-party/sqlite-appropriate-uses.eval.md` |
| third-party | `example-texts/nasa-stakeholder-expectations-definition.md` | `NASA SEH: Stakeholder Expectations` | `design_doc` | `evals/baselines/third-party/nasa-stakeholder-expectations-definition.eval.md` |
| third-party | `example-texts/irs-1040-filing-requirements.md` | `IRS 1040: Filing Requirements` | `brief` | `evals/baselines/third-party/irs-1040-filing-requirements.eval.md` |
| self | `docs/practical-prose-guidelines.md` | `Practical Prose Guidelines` | `design_doc` | `evals/baselines/self/practical-prose-guidelines.eval.md` |
| self | `docs/practical-prose-rubric.md` | `Practical Prose Rubric` | `design_doc` | `evals/baselines/self/practical-prose-rubric.eval.md` |
| self | `docs/practical-prose-bibliography.md` | `Practical Prose Bibliography` | `deep_research` | `evals/baselines/self/practical-prose-bibliography.eval.md` |

## Output Format

The only supported eval artifact format is `.eval.md`: YAML frontmatter plus a rendered
Markdown body. The scorer must not write raw model-response sidecars or other recovery
files.

Each generated report should pass:

```bash
pprose report validate path/to/report.eval.md --complete
```

## Default: Run All Baselines

Run from the repo root.
This block deletes the previous baseline output directory, regenerates stubs from
metrics, scores all six reports in one batch, validates each report, generates
comparison files, and Flowmark-formats the generated Markdown.

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
TOOL_DIR="$REPO_ROOT/tools/pprose"
OUT_DIR="$REPO_ROOT/evals/baselines"
COMMIT_SHA="$(git -C "$REPO_ROOT" rev-parse HEAD)"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR/third-party" "$OUT_DIR/self"

cd "$TOOL_DIR"

uv run pprose report from-metrics \
  "$REPO_ROOT/example-texts/sqlite-appropriate-uses.md" \
  --label "SQLite: Appropriate Uses" \
  --scope-class brief \
  --commit-sha "$COMMIT_SHA" \
  --evaluator "model:claude-sonnet-4-5" \
  --method "pprose score" \
  --out "$OUT_DIR/third-party/sqlite-appropriate-uses.eval.md"

uv run pprose report from-metrics \
  "$REPO_ROOT/example-texts/nasa-stakeholder-expectations-definition.md" \
  --label "NASA SEH: Stakeholder Expectations" \
  --scope-class design_doc \
  --commit-sha "$COMMIT_SHA" \
  --evaluator "model:claude-sonnet-4-5" \
  --method "pprose score" \
  --out "$OUT_DIR/third-party/nasa-stakeholder-expectations-definition.eval.md"

uv run pprose report from-metrics \
  "$REPO_ROOT/example-texts/irs-1040-filing-requirements.md" \
  --label "IRS 1040: Filing Requirements" \
  --scope-class brief \
  --commit-sha "$COMMIT_SHA" \
  --evaluator "model:claude-sonnet-4-5" \
  --method "pprose score" \
  --out "$OUT_DIR/third-party/irs-1040-filing-requirements.eval.md"

uv run pprose report from-metrics \
  "$REPO_ROOT/docs/practical-prose-guidelines.md" \
  --label "Practical Prose Guidelines" \
  --scope-class design_doc \
  --commit-sha "$COMMIT_SHA" \
  --evaluator "model:claude-sonnet-4-5" \
  --method "pprose score" \
  --out "$OUT_DIR/self/practical-prose-guidelines.eval.md"

uv run pprose report from-metrics \
  "$REPO_ROOT/docs/practical-prose-rubric.md" \
  --label "Practical Prose Rubric" \
  --scope-class design_doc \
  --commit-sha "$COMMIT_SHA" \
  --evaluator "model:claude-sonnet-4-5" \
  --method "pprose score" \
  --out "$OUT_DIR/self/practical-prose-rubric.eval.md"

uv run pprose report from-metrics \
  "$REPO_ROOT/docs/practical-prose-bibliography.md" \
  --label "Practical Prose Bibliography" \
  --scope-class deep_research \
  --commit-sha "$COMMIT_SHA" \
  --evaluator "model:claude-sonnet-4-5" \
  --method "pprose score" \
  --out "$OUT_DIR/self/practical-prose-bibliography.eval.md"

uv run pprose score "$OUT_DIR"/third-party/*.eval.md "$OUT_DIR"/self/*.eval.md --batch

for report in "$OUT_DIR"/third-party/*.eval.md "$OUT_DIR"/self/*.eval.md; do
  uv run pprose report validate "$report" --complete
done

uv run pprose compare "$OUT_DIR"/third-party/*.eval.md \
  --format both \
  > "$OUT_DIR/comparison-third-party.md"

uv run pprose compare "$OUT_DIR"/self/*.eval.md \
  --format both \
  > "$OUT_DIR/comparison-self.md"

uv run pprose compare "$OUT_DIR"/third-party/*.eval.md "$OUT_DIR"/self/*.eval.md \
  --format both \
  > "$OUT_DIR/comparison-all.md"

cd "$REPO_ROOT"
flowmark --auto "$OUT_DIR"/*.md "$OUT_DIR"/third-party/*.md "$OUT_DIR"/self/*.md

cd "$TOOL_DIR"
for report in "$OUT_DIR"/third-party/*.eval.md "$OUT_DIR"/self/*.eval.md; do
  uv run pprose report validate "$report" --complete
done
```

If a report fails alignment during `pprose score`, retry that specific report:

```bash
cd tools/pprose
uv run pprose score "$REPO_ROOT/evals/baselines/path/to/failed.eval.md"
```

Do not use `--allow-misaligned` for a published baseline unless the goal is explicitly
to inspect and fix a malformed model response.

## Optional: Third-Party Only

Use this only when debugging converted source examples.
The default baseline run should include the self docs too.

```bash
cd "$REPO_ROOT/tools/pprose"
uv run pprose score "$REPO_ROOT/evals/baselines/third-party"/*.eval.md --batch

for report in "$REPO_ROOT/evals/baselines/third-party"/*.eval.md; do
  uv run pprose report validate "$report" --complete
done

uv run pprose compare "$REPO_ROOT/evals/baselines/third-party"/*.eval.md \
  --format both \
  > "$REPO_ROOT/evals/baselines/comparison-third-party.md"
```

## Optional: Self-Evals Only

Use this when checking whether rubric/guideline changes alter the repo’s own
documentation scores.
The default baseline run should include the third-party examples too.

```bash
cd "$REPO_ROOT/tools/pprose"
uv run pprose score "$REPO_ROOT/evals/baselines/self"/*.eval.md --batch

for report in "$REPO_ROOT/evals/baselines/self"/*.eval.md; do
  uv run pprose report validate "$report" --complete
done

uv run pprose compare "$REPO_ROOT/evals/baselines/self"/*.eval.md \
  --format both \
  > "$REPO_ROOT/evals/baselines/comparison-self.md"
```

## Final Checks

- Every `.eval.md` validates with `--complete`.
- Generated comparison files exist for third-party, self, and all-baseline views.
- `find evals/baselines -name '*.raw.txt'` returns no files.
- `rg 'raw_response_path|\.raw\.txt|raw response' evals/baselines` returns no matches.
- Flowmark has been run on every generated Markdown file.
- Any cross-scope warning in comparison output is expected when comparing all baselines,
  because the set intentionally mixes `brief`, `design_doc`, and `deep_research`.

<!-- This document follows common-doc-guidelines.md.
Review guidelines before editing.
-->
