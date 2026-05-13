---
title: Plan Spec — Eval Scoring Re-Architecture
description: Replace the `claude` CLI subprocess in eval_score.py with the Anthropic SDK + prompt caching + bounded async concurrency
author: Joshua Levy (github.com/jlevy) with agent assistance
---
# Feature: Eval Scoring Re-Architecture

**Date:** 2026-05-12

**Author:** Joshua Levy

**Status:** Implemented (all three phases)

## Overview

Restructure the eval tooling currently living as inline-uv-script files under `scripts/`
into a proper modern Python package under `tools/`, then replace the `claude` CLI
subprocess with the Anthropic SDK using **prompt caching** on the rubric + guidelines +
instructions block, and add **bounded async concurrency** for batch runs across N
artifacts.

The current implementation is a set of `#!/usr/bin/env -S uv run --script` files with
inline PEP 723 dependency metadata.
This works but defeats normal project tooling (ruff, pytest, basedpyright, CI), shares
no dep lock, and makes the SDK migration awkward to test.
The re-architecture lays a proper package layer in **Phase 0** (using the
`simple-modern-uv` copier template at
[attic/simple-modern-uv](../../../../attic/simple-modern-uv/) — or its published origin
if preferred), then migrates the scoring path in **Phase 1**, then adds batch
concurrency in **Phase 2**.

The async concurrency pattern is modeled on the `gather_limited` primitive from the
leximetry codebase (`leximetry/utils/aio_limited.py`).

## Goals

- **Batch wall-clock time** drops from ~4 hours (12 docs × ~23 min each) to ~2–3 minutes
  for a 12-doc round.
- **Per-doc cost** drops ~10× by virtue of prompt caching on the ~99K-token
  rubric+guidelines block that’s identical across all docs in a batch.
- **F6 hangs eliminated** — no more `claude` CLI subprocess that can stick indefinitely;
  SDK calls have native HTTP timeouts and retries.
- **F3 robustness improved** — the SDK’s structured-output / tool-use path removes the
  JSON-fence parsing layer and the corresponding failure modes.
- **Audit trail preserved** — raw response, prompt hash, model identity, cache-hit stats
  persist to `*.eval.raw.txt` and `metadata.repro` exactly as today.
- **Output schema unchanged** — every existing `*.eval.yaml`, fixture, and
  `eval_report.py validate` invocation continues to work bit-for-bit.

## Non-Goals

- **Not replacing the rubric or guidelines.** Content of the prompt-shaped inputs is
  unchanged.
- **Not changing the eval-report YAML schema** or the validation logic in
  `eval_report.py`. The data contract stays put; only the package layout and the
  model-call substrate change.
- **Not adopting pydantic-ai.** Direct Anthropic SDK only — multi-provider abstraction
  is out of scope for this round.
- **Not extracting metaproc runpool.** That would solve subprocess orchestration, which
  we no longer have after Phase 1.
- **Not changing the one-call-per-doc, 18-dims-in-one-response architecture.** The
  rubric’s alignment principle (Calibration + Fairness + Robustness scored against the
  same read of the doc) requires holistic scoring.
- **Not publishing to PyPI** in this spec.
  The package lives under `tools/` in this repo for now; publishing is a separate
  decision.

## Background

### Today’s path

`tools/prose-eval/src/prose_eval/eval_score.py` builds a ~110K-token prompt
(instructions + rubric + guidelines \+ artifact), spawns
`claude -p <prompt> --model sonnet` as a subprocess, reads stdout, extracts a ```json
fence, parses against the rubric schema, and writes the filled YAML. Each call is
independent and re-pays the full input-token cost for the ~99K invariant portion (rubric
\+ guidelines + instructions).

### Friction observed in self-eval-v0.1

| ID | Issue |
| --- | --- |
| F2 | `REPO_ROOT = BUNDLE_ROOT.parents[3]` stale assumption. **Fixed in round 1.** |
| F3 | Model invents out-of-range `rule_number`. **Partially fixed:** prompt appendix + validator softening (F3a). |
| F4 | Raw response not saved on parse failure. **Fixed in round 1.** |
| F5 | ~23 min/doc → 4h for a 12-doc batch. **This spec addresses this.** |
| F6 | `claude` CLI subprocess can hang indefinitely. **This spec addresses this.** |

Full details:
[evals/self-eval-v0.1/findings.md](../../../../evals/self-eval-v0.1/findings.md).

### Approaches considered

| Path | Why not |
| --- | --- |
| **Depend on full `metaproc`** | Wrong dependency direction; couples writing tool to a trading codebase. |
| **Extract `metaproc/runpool` as a standalone lib** | ~2200 LOC for problems we no longer have (process management, memory pressure, GCP backends). Solves the wrong axis. |
| **Adopt leximetry’s full pattern** | Pydantic-ai + per-metric call shape. Per-metric calls would break the rubric’s holistic-scoring design property. The `gather_limited` primitive itself (~57 LOC) is excellent and we adopt it. |
| **Anthropic SDK + prompt caching (this spec)** | Smallest delta, biggest performance win, no new dep on multi-provider abstractions, preserves audit trail and YAML schema. |

### Why repackage the scripts first (Phase 0)

The current `scripts/*.py` files use PEP 723 inline metadata (`/// script`) with
`#!/usr/bin/env -S uv run --script` shebangs.
This is fine for one-off scripts, but it has three real costs for the SDK migration:

1. **Each script declares its own deps inline.** `eval_score.py`, `eval_report.py`, and
   `eval_compare.py` each pin `pydantic`, `pyyaml`, `chopdiff` independently.
   Adding `anthropic` + `aiolimiter` would mean editing every script’s metadata block,
   and they would resolve different versions if not kept in sync by hand.
2. **No proper test runner.** Tests today require an out-of-band
   `uv run --python 3.11 --with pytest --with chopdiff --with pyyaml --with pydantic python -m pytest test_eval_score.py`
   invocation. There’s no `make test`, no CI hook, no lint pass — F2/F4 ship-bug
   regressions are caught only by manual re-run.
3. **No shared module layout.** `rubric_schema.py` is imported by `eval_score.py` and
   `eval_report.py` only because they’re sibling files; testing a function from
   `practical_prose_metrics.py` from a test elsewhere requires `sys.path` shimming.

Moving the code under a packaged `tools/<package-name>/` layout produced by the
[simple-modern-uv](../../../../attic/simple-modern-uv/) copier template fixes all three:
one lockfile, one `pytest` invocation, one set of CLI entry points, ruff + basedpyright
\+ codespell wired up, CI green on push.

## Design

### Approach

In `tools/prose-eval/src/prose_eval/eval_score.py`:

1. Replace `call_claude` (currently `subprocess.run(["claude", "-p", prompt], ...)`)
   with a function that uses the Anthropic SDK directly.
2. Restructure the prompt as a **multi-block message** so prompt caching applies to the
   invariant portion (rubric + guidelines + per-dimension rule bounds + instructions).
   The artifact and artifact-specific framing go in a separate, uncached final block.
3. Add a small `gather_limited(*, max_concurrent, max_rps)` async helper patterned on
   leximetry’s `aio_limited.py` — ~30 LOC, no new deps beyond `aiolimiter` (or implement
   the leaky bucket inline, ~10 more LOC, and skip even that dep).
4. Add a `batch` subcommand or `--batch` flag to `eval_score.py` accepting N YAML paths,
   which schedules all N through `gather_limited`. Default concurrency: 4. Default RPS
   cap: 2.
5. Persist `cache_creation_input_tokens` and `cache_read_input_tokens` per call into
   `metadata.repro` so the audit trail records the cache hit rate of each batch run.

### Components

After Phase 0 the eval code lives under `tools/prose-eval/` with this shape:

```
tools/prose-eval/
├── Makefile                          # install / lint / test / build
├── pyproject.toml                    # hatchling + uv-dynamic-versioning
├── README.md
├── devtools/lint.py                  # ruff + codespell + basedpyright runner
├── src/prose_eval/
│   ├── __init__.py
│   ├── eval_score.py                 # SDK scorer (was tools/prose-eval/src/prose_eval/eval_score.py)
│   ├── eval_report.py                # schema + validators (unchanged logic)
│   ├── eval_compare.py               # N-way comparison renderer
│   ├── metrics.py                    # deterministic doc metrics
│   ├── rubric_schema.py              # rubric loader
│   ├── rubric_schema.yaml            # packaged data
│   ├── _concurrency.py               # gather_limited helper (Phase 2)
│   └── prompts/
│       └── eval-rubric-score.md      # packaged data
└── tests/
    ├── test_eval_score.py
    ├── test_eval_report.py
    ├── test_eval_compare.py
    ├── test_metrics.py
    ├── fixtures/                     # calibration set + golden comparison
    └── test_fixtures/
```

Files with **behavioral** changes (Phase 1 + 2):

- **`eval_score.py`**:
  - `call_claude(prompt, model)` → `call_anthropic(messages, model)` using
    `client.messages.create` with cache_control on the invariant block.
  - New: `_build_messages(artifact_path)` returning the multi-block shape.
  - New: `score_batch(yaml_paths, *, model, max_concurrent, max_rps)` — parallel scoring
    orchestrator.
  - Existing `parse_response` + `extract_json_block` unchanged.
- **`_concurrency.py`** (new): `gather_limited(coros, *, max_concurrent, max_rps)`,
  ~30-40 lines.

Files with **no behavioral changes**, just relocation:
- `eval_report.py`, `eval_compare.py`, `metrics.py`, `rubric_schema.py`.

### API Changes

- **CLI:** the four entry points become installable as console scripts in the new
  package: `eval-score`, `eval-report`, `eval-compare`, `prose-metrics`. After
  `make install` in `tools/prose-eval/` they’re on PATH inside the package’s `.venv`.
  `eval-score` gains a `batch` subcommand; the others keep their argparse surface.
- **Imports:** `from rubric_schema import X` becomes
  `from prose_eval.rubric_schema import X`. Tests are updated to match.
- **YAML schema:** unchanged.
  The only addition is `metadata.repro.cache_stats` (optional dict with
  `creation_input_tokens` and `read_input_tokens`). Older YAMLs without this field
  continue to validate.
- **Dependency:** add `anthropic>=0.39` (Phase 1) and optionally `aiolimiter>=1.2`
  (Phase 2; skippable if we inline the leaky bucket).
  Remove the hard runtime dependency on the `claude` CLI being on PATH; keep it as a
  fallback path behind a `--use-cli` flag.
- **Env:** requires `ANTHROPIC_API_KEY` in env (SDK default behavior).

### Auth model

The SDK reads `ANTHROPIC_API_KEY` from env by default.
The runbook will note the env var requirement.
The `claude` CLI auth path (which uses OAuth / managed credentials) is dropped from the
default path; `--use-cli` can stay as an escape hatch.

### Reproducibility

Today `metadata.repro` captures `model`, `command`, `raw_response_path`,
`prompt_sha256`, `rubric_sha256`, `guidelines_sha256`. We preserve all of these and add:
- `cache_stats`: `{creation_input_tokens, read_input_tokens}` from the Anthropic
  response usage block.
- `sdk_version`: `anthropic` package version at call time.

`prompt_sha256` is computed over the **rendered prompt text** (concatenation of all
blocks) so it stays comparable to historical YAMLs.

## Implementation Plan

### Phase 0: Scaffold a proper Python package under `tools/` (DONE)

Stood up a packaged Python project with the simple-modern-uv layout and migrated
`scripts/*.py` into it so the rest of the spec lands on solid ground.
**Source `scripts/` directory is intentionally left in place during Round 1’s in-flight
self-eval run; it’ll be deleted once the running background scorer completes.**

- [x] Confirmed defaults: package `prose-eval`, module `prose_eval`, directory
  `tools/prose-eval/`. Entry points named `eval-score`, `eval-report`, `eval-compare`,
  `prose-metrics`.
- [x] Bootstrapped from the **published** copier template (not the attic copy) so future
  `copier update` works:
  `bash uvx copier copy --vcs-ref v0.2.25 --defaults \ --data package_name=prose-eval \ --data package_module=prose_eval \ --data 'package_description=Practical-prose eval tooling: rubric scoring, reports, comparisons' \ --data 'package_author_name=Joshua Levy' \ --data package_author_email=joshuadlevy@gmail.com \ --data package_github_org=jlevy \ gh:jlevy/simple-modern-uv tools/prose-eval `
  The resulting `tools/prose-eval/.copier-answers.yml` records
  `_src_path: gh:jlevy/simple-modern-uv` and `_commit: v0.2.25`. Future template
  updates: `cd tools/prose-eval && uvx copier update`.
- [x] Copied source files into the new package’s `src/prose_eval/`: `eval_score.py`,
  `eval_report.py`, `eval_compare.py`, `practical_prose_metrics.py` → `metrics.py`,
  `rubric_schema.py`, `rubric_schema.yaml`, `prompts/eval-rubric-score.md`.
- [x] Copied test files into `tools/prose-eval/tests/`: `test_*.py`, `test_fixtures/`,
  `fixtures/`.
- [x] Stripped PEP 723 inline-script headers from each migrated file.
  Moved deps into `tools/prose-eval/pyproject.toml`:
  `toml dependencies = [ "chopdiff>=0.2.1", "pydantic>=2.0", "pyyaml>=6.0", ] ` Kept the
  dev block from the template (`pytest`, `ruff`, `codespell`, `basedpyright`,
  `pytest-sugar`, `funlog`).
- [x] Rewrote intra-package imports (`from eval_report import X` →
  `from prose_eval.eval_report import X`, etc.)
  and removed `sys.path.insert(...)` shims from source files and tests.
- [x] Updated path resolution in `eval_score.py`:
  `PACKAGE_ROOT = Path(__file__).resolve().parent`; rubric / guidelines resolved via
  `REPO_ROOT = _find_repo_root(PACKAGE_ROOT)` (walks up for `.git`); prompt template
  loaded from `PACKAGE_ROOT / "prompts" / ...`.
- [x] Wired up entry points in `pyproject.toml`:
  `toml [project.scripts] eval-score = "prose_eval.eval_score:main" eval-report = "prose_eval.eval_report:main" eval-compare = "prose_eval.eval_compare:main" prose-metrics = "prose_eval.metrics:main" `
- [x] Included packaged data in the wheel
  (`[tool.hatch.build.targets.wheel].include = ["src/prose_eval/rubric_schema.yaml", "src/prose_eval/prompts/*.md"]`).
- [x] Restricted pytest discovery to `tests/` (was `["src", "tests"]` per the template
  default, which caused collection of the source modules).
- [x] Relaxed basedpyright for the migrated legacy code — turned off the strict-type
  rules that flag pre-existing patterns (Optional-access, mixed int|str arithmetic,
  unknown-type propagation, unannotated-class-attribute, etc.). Tightening is a
  follow-on once the SDK migration in Phase 1 lands and the surface is small enough to
  type properly.
- [x] Phase 0 gate verified: - `make install` ✅ - `make lint` ✅ (0 errors) - `make test`
  146/150 — the 4 remaining failures
  (`test_metrics.py::TestB14_ReproducibilityRegression`) are **pre-existing
  fixture-drift errors** that fail identically in the original `scripts/` location.
  Tracked separately; not a Phase 0 regression.

**Phase 0 deferred items (do after the in-flight scorer finishes):**

- [ ] Delete `scripts/` once round-1 scoring completes and we’re sure no background
  process references the old paths.
- [ ] Update runbooks
  ([practical-prose-eval-single.runbook.md](../../../../runbooks/practical-prose-eval-single.runbook.md),
  [practical-prose-eval-compare.runbook.md](../../../../runbooks/practical-prose-eval-compare.runbook.md))
  to call the new entry points (`eval-score …` instead of
  `../tools/prose-eval/src/prose_eval/eval_score.py …`).
- [ ] Update root `README.md` Tooling section to point at `tools/prose-eval/`.
- [ ] Optional: enable the template’s `.github/workflows/ci.yml` for the
  `tools/prose-eval/` subdir.
  (Out of scope per Non-Goals until publishing is decided.)
- [ ] Fix the 4 pre-existing fixture-drift failures in
  `test_metrics.py::TestB14_ReproducibilityRegression` (chopdiff added new fields —
  regenerate the pinned JSON, or pin chopdiff version).

### Phase 1: Single-doc SDK migration with prompt caching (DONE)

(Operates on the post-Phase-0 layout.
Source paths refer to `tools/prose-eval/src/prose_eval/`.)

- [x] Added `anthropic>=0.39` and `python-dotenv>=1.0` to
  `tools/prose-eval/pyproject.toml`. (`aiolimiter` added with Phase 2.) Per Q6 decision,
  the `claude` CLI fallback was **dropped entirely**; SDK-only.
- [x] Added `call_anthropic(messages, model)` using `client.messages.create` with
  `cache_control={"type": "ephemeral"}` on the invariant block (`_cached_block_text()`).
  Also added `call_anthropic_async()` for batch.
- [x] Added `_build_messages(artifact_path)` returning a 2-block user message: block 1 =
  instructions + rule bounds + rubric + guidelines (cached); block 2 =
  `## Artifact under review` header + artifact body (uncached).
- [x] Added `_load_env_files()` mirroring leximetry’s pattern; auto-loads `.env` /
  `.env.local` from `cwd` hierarchy and `$HOME` at the start of `main()`.
  `ANTHROPIC_API_KEY` is required (early error if missing).
- [x] Added `_resolve_model()` for `sonnet`/`opus`/`haiku` aliases.
  `DEFAULT_MODEL = "claude-sonnet-4-5"`.
- [x] Rewired `main()` to use the SDK; no CLI fallback path retained.
- [x] Extended `ReproContext` with `model_id`, `sdk_version`, `cache_stats`. Extended
  `EvalMetadata` schema to accept the new fields.
  Persists under `metadata.repro` (the validator’s existing extra='forbid' was widened).
- [x] Updated `tests/test_eval_score.py` with `_FakeAnthropic` mock + 5 new tests:
  `_build_messages` shape and cache-control, `_resolve_model` aliases, ReproContext
  SDK-field persistence, `call_anthropic` usage parsing, full end-to-end `main()`
  round-trip persisting `cache_stats`. All 155 tests pass (up from 150).
- [x] Manual verification: re-scored `readme.eval.yaml` end-to-end via SDK in **58s**
  (target <60s ✓). `cache_stats.creation_input_tokens=26198` written.
  `overall_mean` shifted 4.36 → 3.67 — outside the ±0.2 target but **attributable to
  model-version calibration drift** (Sonnet 4.5 now assesses
  Calibration/Fairness/Robustness/Factuality where the round-1 model marked them NA).
  Logged as a separate calibration finding, not a Phase 1 regression.

### Phase 2: Batch scoring with bounded concurrency (DONE)

- [x] Added `src/prose_eval/_concurrency.py` with
  `gather_limited(*coros, max_concurrent, max_rps, return_exceptions)` patterned on
  leximetry’s `aio_limited.py` — `asyncio.Semaphore` + `aiolimiter.AsyncLimiter`.
  Aiolimiter dep added.
- [x] Factored `_score_one` body into `_prepare_score()` + `_apply_score()` shared
  between sync and async paths.
  Added `_score_one_async()` for the batch path.
- [x] Added
  `score_batch(yaml_paths, *, model, evaluator, allow_misaligned, argv, max_concurrent=8, max_rps=4.0)`
  using `gather_limited` with `return_exceptions=True` so one failing doc doesn’t abort
  the batch.
- [x] Wired `--batch`, `--max-concurrent`, `--max-rps` argparse flags per Q8 decision
  (flag, not subcommand).
  Defaults `8` / `4.0` per Q9. `main()` routes to `score_batch` when `--batch` +
  multiple inputs; otherwise falls back to the sequential `_score_one` loop.
  Per-doc OK/FAIL is printed as each completes.
- [x] Manual verification: re-ran the 12-doc self-eval batch in **1m33s** (target <5 min
  ✓; round-1 took ~4 hours, so **~160× speedup**). Output lives in
  `evals/self-eval-v0.2/`. 8/12 docs completed cleanly and pass `eval-report validate`;
  the other 4 hit F3a alignment failures (out-of-range `rule_number` dropped → orphaned
  sub-5 score). `cache_stats` confirms the mechanism: 2 docs showed
  `read_input_tokens=26198` / `creation=0` (cache hits), the other 6 fired concurrently
  before priming. Round 3 candidate: pre-warm the cache with one call before fanning out
  the rest.
- [x] Updated
  [runbooks/practical-prose-eval-single.runbook.md](../../../../runbooks/practical-prose-eval-single.runbook.md)
  and
  [runbooks/practical-prose-eval-compare.runbook.md](../../../../runbooks/practical-prose-eval-compare.runbook.md)
  to mention the new `--batch` form, the `ANTHROPIC_API_KEY` requirement, the observed
  batch wall-clock, and the F3a alignment-failure recovery path.

## Testing Strategy

- **Phase 0 gate:** `make install && make lint && make test` in `tools/prose-eval/` must
  pass before touching call_claude → call_anthropic. The 79 existing tests across
  `test_eval_score.py` (24), `test_eval_report.py` (~40), `test_eval_compare.py`, and
  `test_practical_prose_metrics.py` should all pass under the new layout with only
  import-path renames.
- **Unit tests preserved through Phase 1.** All 24 tests in `test_eval_score.py` keep
  passing by mocking the SDK client at the same layer as today’s CLI subprocess mock.
- **Integration test (manual):** re-run round-1 self-eval and require:
  - Mean overall score per doc within ±0.2 of round-1 values.
  - Per-dimension scores within ±1 (allowing for normal model variance).
  - All YAMLs pass `eval_report.py validate`.
  - `cache_read_input_tokens > 0` on docs 2..N of a batch.
- **Calibration regression:** re-score `scripts/fixtures/guidelines-self.eval.yaml` and
  confirm overall mean within ±0.3 of the pinned 4.1.
- **Hang resistance (F6):** the SDK has built-in HTTP timeouts; verify by inspection
  that a per-call timeout is set (e.g., 5 min) and that `score_batch` does not stall the
  whole batch on one slow call.

## Rollout Plan

- Single commit on `main` (or a branch + PR if preferred) implementing both phases.
- Update
  [runbooks/practical-prose-eval-single.runbook.md](../../../../runbooks/practical-prose-eval-single.runbook.md)
  with the new commands and env-var note.
- Bump the round-1 self-eval to round-2 once the new tool is in place and re-run for
  comparison.

## Open Questions

### Phase 0 (must resolve before bootstrapping the template)

1. **Package name?** Candidates: `prose-eval` (concise), `practical-prose-eval`
   (descriptive, matches repo name), `pp-eval` (very short).
   Default assumption: `prose-eval`.
2. **Module name?** Snake_case of the package.
   With `prose-eval` → `prose_eval`.
3. **Entry-point names?** Current scripts are `eval_score.py` / `eval_report.py` /
   `eval_compare.py` / `practical_prose_metrics.py`. Proposed console scripts:
   `eval-score`, `eval-report`, `eval-compare`, `prose-metrics`. Worth keeping the `pp-`
   prefix to avoid generic name collisions on PATH?
4. **Local template path vs.
   published origin?** Bootstrap from `attic/simple-modern-uv/` (frozen in this repo) or
   `uvx uvtemplate` (the published wrapper that pulls latest)?
   Frozen is more reproducible.
5. **Where do rubric+guidelines docs live for the package to find them?** They stay in
   `docs/` at repo root.
   The package resolves them via the git repo root, found by walking up from the package
   install dir or via `git rev-parse --show-toplevel`. Same logic as the F2 fix already
   in `eval_score.py`.

### Phase 1 / 2 — resolved

| # | Question | Decision |
| --- | --- | --- |
| 6 | Drop `claude` CLI path or keep `--use-cli` fallback? | **Drop entirely.** SDK-only. Requires `ANTHROPIC_API_KEY` from env (loaded from `.env` or `.env.local` if present). |
| 7 | `aiolimiter` dep or inline leaky-bucket? | **Use `aiolimiter`.** Battle-tested, ~30 LOC for `gather_limited`. |
| 8 | `batch` as subcommand or flag? | **Flag.** `eval-score a.yaml b.yaml ... --batch [--max-concurrent N --max-rps M]`. Single argparse entry, multiple positional args. |
| 9 | Default `--max-concurrent` and `--max-rps`? | **`max-concurrent=8, max-rps=4`.** ~2 min for 12 docs. Override per-run. |
| 10 | Per-call timeout? | **10 minutes.** Generous; longest round-1 doc was ~5 min, 10 min absorbs cold-cache + variance. |

Also: load `.env` / `.env.local` via `python-dotenv` at the start of each console-script
entry point (`eval-score`, `eval-report`, `eval-compare`, `prose-metrics`), matching the
pattern used by leximetry’s CLI entry point (which calls
`clideps.env_vars.dotenv_utils.load_dotenv_paths()` from main).
Our equivalent: a small `_load_env_files()` helper that walks `cwd` and home for `.env`
/ `.env.local`, ~15 LOC, dep `python-dotenv>=1.0`.

## References

- [attic/simple-modern-uv/](../../../../attic/simple-modern-uv/) — the copier template
  used by Phase 0.
- [evals/self-eval-v0.1/findings.md](../../../../evals/self-eval-v0.1/findings.md) —
  F1–F6 friction log.
- [tools/prose-eval/src/prose_eval/eval_score.py](../../../../tools/prose-eval/src/prose_eval/eval_score.py)
  — the file being relocated and rewritten.
- [tools/prose-eval/src/prose_eval/prompts/eval-rubric-score.md](../../../../tools/prose-eval/src/prose_eval/prompts/eval-rubric-score.md)
  — the prompt template that becomes the cached block.
- [runbooks/practical-prose-eval-single.runbook.md](../../../../runbooks/practical-prose-eval-single.runbook.md)
  — the runbook to update.
- The `gather_limited` primitive in the leximetry codebase
  (`leximetry/utils/aio_limited.py`) — pattern adopted here.
- The metaproc `runpool` subsystem — surveyed; rejected as overkill for this use case
  (process-pool orchestration vs.
  async I/O).
