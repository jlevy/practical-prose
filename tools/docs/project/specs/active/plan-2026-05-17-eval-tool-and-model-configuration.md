---
title: Plan Spec - Eval Tool and Model Configuration
description: Add provider-neutral eval targets, web-search toggles, repeat runs, and simple multi-model scoring to prose-eval
author: Joshua Levy (github.com/jlevy) with agent assistance
---
# Feature: Eval Tool and Model Configuration

**Date:** 2026-05-17

**Author:** Joshua Levy with agent assistance

**Status:** Draft

## Overview

Add explicit model, source-check, repeat, and multi-model settings to `prose-eval score`
without turning the evaluator into a general orchestration framework.

The current implementation happens to call the Anthropic Messages API without any
`tools=` parameter. That means the scorer can read the artifact, rubric, guidelines,
and deterministic metrics, but it cannot search the web, fetch URLs, or externally
corroborate sources. This is a correct safe default, but the eval report should record
that capability boundary and should let users opt into web source checking when a
higher-stakes Factuality pass needs it.

The configuration model should stay boring:

- choose one or more targets, primarily `openai/gpt-5.5` and
  `anthropic/claude-opus-4-7`;
- optionally repeat each target a small number of times;
- optionally run independent scoring calls concurrently;
- optionally enable web source checking;
- optionally use one of a few built-in presets that expand to those same parameters;
- record exactly what ran in metadata.

No general ensemble language is needed in the first pass. If someone wants three repeats
or two models, those should be straightforward parameters, not a custom run graph.

## Goals

- Keep the default scoring mode closed-world: no web search, no URL fetching, no
  external source validation.
- Support OpenAI, Anthropic, OpenAI-compatible endpoints, and future providers through a
  small adapter interface instead of provider-specific fields throughout the scoring
  code.
- Focus current implementation and fixtures on `openai/gpt-5.5` and
  `anthropic/claude-opus-4-7`, while keeping the target parser open to other model ids.
- Make source-checking a simple setting: web off by default, web on only when requested,
  or manifest mode when a local evidence manifest is provided.
- Support simple repeat and multi-model runs through `--repeat` and repeated `--target`
  flags.
- Support bounded concurrency for independent scoring runs without changing run
  semantics.
- Provide a small set of built-in presets for common calibration runs; presets expand to
  normal parameters and do not introduce a separate schema.
- Record the actual target, provider, API surface, model id, model args, source-check
  mode, tool usage, run index, and external-validation status in eval metadata.
- Prevent reports from claiming external corroboration unless web source checking or an
  evidence manifest was actually used.
- Preserve individual run reports and emit a lightweight multi-run summary when more
  than one run is produced.

## Non-Goals

- Do not enable web search by default.
- Do not give `prose-eval report validate` network access. Validation remains local and
  deterministic.
- Do not require multiple models for ordinary scoring.
- Do not build a full model gateway, router, provider registry, or ensemble DSL. If
  users already run LiteLLM, OpenRouter, or another gateway, `prose-eval` should be able
  to call it through an OpenAI-compatible adapter.
- Do not try to normalize every generation parameter across providers. Only normalize
  provenance and a few cross-provider concepts; pass the rest through as provider args.
- Do not expose allowed-domain or blocked-domain controls for source checking. Web
  source checking is on or off; source quality is judged in the eval reasoning.
- Do not hardcode old provider model aliases in examples. Examples should either use
  current verified model ids or placeholders that are resolved from local config.
- Do not make Factuality impossible without web search. A no-tool run can still score
  source discipline and internal factual consistency, but it must not claim external
  corroboration.

## Borrowed Conventions

The config shape should borrow from existing tools without inheriting their full
frameworks:

| Framework | Useful convention to borrow | Avoid |
| --- | --- | --- |
| Inspect AI | `provider/model` target ids, `--model` plus provider-specific model args, OpenAI-compatible escape hatch, custom provider extensions. | Requiring users to write Python tasks just to choose a scorer. |
| Promptfoo | Simple provider strings or `{ id, config }` objects, repeat runs, provider response metadata. | Importing the whole prompt/test/assertion matrix model. |
| lm-evaluation-harness | Minimal `--model` plus provider-specific args. | Treating practical-prose audits like benchmark tasks. |
| LiteLLM | A gateway can own large provider routing schemas and expose a simple OpenAI-compatible endpoint. | Reimplementing LiteLLM's router or credential model inside `prose-eval`. |
| OpenAI Evals | Eval runs should be reproducible and metadata-rich. | Tying Practical Prose to OpenAI-only eval infrastructure. |

Recommendation: use compact target ids, provider-specific args, and simple run
parameters. Built-in presets should be aliases for those parameters, not a second
configuration framework.

## Current Provider Notes

These notes are a documentation snapshot from 2026-05-17 and should be rechecked during
implementation:

- OpenAI model docs list `gpt-5.5` as the recommended flagship model for complex
  reasoning and coding. The model supports the Responses API, Chat Completions, function
  calling, structured outputs, and hosted tools including web search when used through
  Responses.
- OpenAI `gpt-5.5` reasoning effort supports `none`, `low`, `medium`, `high`, and
  `xhigh`; `medium` is the documented default.
- OpenAI Responses web search is available as `web_search` and older preview variants.
  Practical Prose should expose that as a binary source-check capability: off by
  default, on only when selected.
- Anthropic model docs list Claude Opus 4.7 with Claude API ID
  `claude-opus-4-7`. Anthropic Messages API web search uses an Anthropic-defined server
  tool such as `web_search_20250305`.
- The current cross-model target pair for this plan is `openai/gpt-5.5` and
  `anthropic/claude-opus-4-7`. Other target ids may be accepted, but they are not the
  focus of this implementation pass.

## Design

### Core Concepts

Add a thin run-configuration layer with three concepts:

1. **Target:** a model endpoint to call, identified by a compact provider/model id.
2. **Source-check mode:** `none`, `web`, or `manifest`.
3. **Run parameters:** targets, repeat count, concurrency limit, output directory, and
   optional built-in preset.

The first implementation should preserve the current single-run behavior when no config
or flags are provided, while adding OpenAI Responses support and a gated `gpt-5.5` smoke
test.

### Configuration Precedence

Configuration is resolved in this order, from lowest to highest precedence:

1. Built-in defaults.
2. Optional config file for default targets and provider args.
3. Environment variables for secrets and simple defaults.
4. CLI flags.

Proposed config file names, searched from the current directory upward:

- `prose-eval.config.yaml`
- `.prose-eval.yaml`
- `pyproject.toml` under `[tool.prose-eval]` after YAML support is stable.

### Targets

Targets are the replacement for a broad "model profile" schema. They should be small:

```yaml
default_target: openai/gpt-5.5
default_concurrency: 2
comparison_targets:
  - openai/gpt-5.5
  - anthropic/claude-opus-4-7

targets:
  openai/gpt-5.5:
    api: responses
    reasoning:
      effort: medium
    max_output_tokens: 8192

  openai-compatible/local/prose-scorer:
    base_url_env: PROSE_EVAL_OPENAI_COMPAT_BASE_URL
    api_key_env: PROSE_EVAL_OPENAI_COMPAT_API_KEY
    max_output_tokens: 8192

  anthropic/claude-opus-4-7:
    api: messages
    max_tokens: 8192
```

Rules:

- The target id is canonical and should be recorded in run metadata.
- Target config is provider-specific. The adapter validates only fields it owns and
  passes through the rest where the provider SDK safely supports that pattern.
- Secrets are referenced by environment-variable names, not stored directly.
- Built-in examples must prefer `openai/gpt-5.5` and
  `anthropic/claude-opus-4-7`.

Initial CLI:

```bash
prose-eval score artifact.eval.md --target openai/gpt-5.5
prose-eval score artifact.eval.md --target openai/gpt-5.5 --model-arg reasoning.effort=high
prose-eval score artifact.eval.md --target openai-compatible/local/prose-scorer
prose-eval score artifact.eval.md \
  --target openai/gpt-5.5 \
  --target anthropic/claude-opus-4-7
```

Backwards compatibility:

- Keep the existing `--model` flag as a compatibility alias in the current Anthropic
  path for one release.
- Prefer `--target` in new docs.
- If `--model` is used without `--provider`, preserve the current provider default rather
  than silently switching users to OpenAI.

### Source-Check Mode

Source checking is a simple mode, not a profile system:

| Mode | External access | Purpose |
| --- | --- | --- |
| `none` | No | Default scorer behavior; no external validation claims allowed. |
| `web` | Yes | Use the provider's web-search tool for external validation. |
| `manifest` | No network | Use a local evidence manifest or pre-fetched source bundle. |

Initial CLI:

```bash
prose-eval score artifact.eval.md
prose-eval score artifact.eval.md --web
prose-eval score artifact.eval.md --source-check manifest --evidence-manifest sources.yaml
```

Rules:

- `--web` is sugar for `--source-check web`.
- `--no-web` or omitted source-check settings mean `source_check.mode=none`.
- Web source-check is all-or-nothing at the user layer.
- Provider adapters carry the minimal web tool definition required by their API.
- Manifest mode does not grant network access; it only adds provided evidence to the
  scoring context.

Internal provider conversion:

- OpenAI Responses `none`: no `tools` field.
- OpenAI Responses `web`: add `tools=[{"type": "web_search"}]`.
- Anthropic Messages `none`: no `tools` field.
- Anthropic Messages `web`: add the Anthropic server web-search tool definition.
- Manifest mode: do not add provider web tools; add the evidence manifest as an explicit
  artifact/evidence block in the prompt.
- OpenAI-compatible: default to no provider-managed tools unless the adapter declares
  support for a compatible web-search surface.

### Repeat and Multi-Model Runs

Common calibration should be parameter-driven:

```bash
# One closed-world run with the default target.
prose-eval score artifact.eval.md

# Three independent runs with the same target.
prose-eval score artifact.eval.md --repeat 3

# Three independent runs, with up to three provider calls in flight.
prose-eval score artifact.eval.md --repeat 3 --concurrency 3

# One run each across two targets.
prose-eval score artifact.eval.md \
  --target openai/gpt-5.5 \
  --target anthropic/claude-opus-4-7

# Two runs per target, with web source checking enabled.
prose-eval score artifact.eval.md \
  --target openai/gpt-5.5 \
  --target anthropic/claude-opus-4-7 \
  --repeat 2 \
  --concurrency 2 \
  --web \
  --out-dir evals/runs/doc-001
```

Run expansion is deterministic, and concurrency affects only execution scheduling:

```text
runs = targets x repeat
max in-flight provider calls = min(run_count, --concurrency)
```

Default concurrency should be conservative and non-serial for multi-run jobs, with `2`
as the initial default. The effective in-flight call count is still capped by the number
of expanded runs. The runner should preserve deterministic run ids and summary ordering
even when execution is parallel. Failed runs should be recorded individually; one failed
provider call should not hide completed reports from other runs.

Each run writes a normal eval report with a distinct path when the expanded run count is
greater than one:

```text
evals/runs/doc-001/
  openai-gpt-5.5-r1.eval.md
  openai-gpt-5.5-r2.eval.md
  anthropic-claude-opus-4-7-r1.eval.md
  anthropic-claude-opus-4-7-r2.eval.md
  multi-run-summary.md
```

The summary should include:

- per-dimension scores across runs,
- score spread,
- `NA` disagreement,
- violation disagreement,
- source-check mode per run,
- dimensions requiring human review.

The summary should not overwrite a source eval unless the user explicitly asks to
promote one run or an adjudicated result.

### Built-In Presets

Presets should be a small convenience layer over ordinary parameters:

| Preset | Expansion | Purpose |
| --- | --- | --- |
| `standard` | default target, `--repeat 1`, no web, default concurrency | Explicit name for the default run. |
| `calibration` | default target, `--repeat 3`, no web, default concurrency | Check scoring variance on one model. |
| `web-check` | default target, `--repeat 1`, `--web`, default concurrency | Run one externally grounded pass. |
| `cross-model` | configured comparison targets, `--repeat 1`, no web, default concurrency | Compare models without writing target flags each time. |

Example:

```bash
prose-eval score artifact.eval.md --preset calibration
prose-eval score artifact.eval.md --preset cross-model --out-dir evals/runs/doc-001
```

Preset rules:

- Presets expand before CLI overrides.
- Explicit `--target`, `--repeat`, `--concurrency`, `--web`, `--no-web`, and
  `--source-check` flags override the preset expansion.
- The first implementation should ship only a few presets. It should not accept arbitrary
  user-defined run matrices.
- Optional config may set `comparison_targets` for `cross-model`:

```yaml
comparison_targets:
  - openai/gpt-5.5
  - anthropic/claude-opus-4-7
```

### Metadata Changes

Add metadata that records target setup, run parameters, and source-check setup.

Single run example:

```yaml
metadata:
  target:
    id: openai/gpt-5.5
    provider: openai
    api: responses
    model: gpt-5.5
    config:
      reasoning:
        effort: medium
      max_output_tokens: 8192
  run:
    preset: standard
    repeat_index: 1
    repeat_total: 1
    requested_concurrency: 2
    effective_concurrency: 1
  source_check:
    mode: none
    external_validation_performed: false
  usage:
    input_tokens: 29755
    output_tokens: 1800
```

Web source-check example:

```yaml
metadata:
  source_check:
    mode: web
    provider: openai
    tools:
      - type: web_search
    external_validation_performed: true
    usage:
      web_search_calls: 3
      sources_recorded: true
```

Multi-run summary metadata:

```yaml
multi_run:
  preset: cross-model
  artifact_eval: path/to/artifact.eval.md
  source_check: none
  repeat: 1
  requested_concurrency: 2
  effective_concurrency: 2
  runs:
    - id: openai-gpt-5.5-r1
      report: openai-gpt-5.5-r1.eval.md
      target: openai/gpt-5.5
      repeat_index: 1
    - id: anthropic-claude-opus-4-7-r1
      report: anthropic-claude-opus-4-7-r1.eval.md
      target: anthropic/claude-opus-4-7
      repeat_index: 1
```

### Internal Interfaces

Keep the internal models intentionally thin:

```python
class TargetSpec(BaseModel):
    id: str
    config: dict[str, Any] = Field(default_factory=dict)

class SourceCheckSettings(BaseModel):
    mode: Literal["none", "web", "manifest"] = "none"
    evidence_manifest: Path | None = None

class ScoreRunParams(BaseModel):
    targets: list[str]
    repeat: int = 1
    concurrency: int = 2
    source_check: SourceCheckSettings = SourceCheckSettings()
    preset: str | None = None
    out_dir: Path | None = None

class ScoreRun(BaseModel):
    id: str
    target: TargetSpec
    repeat_index: int
    repeat_total: int
    source_check: SourceCheckSettings

class ProviderAdapter(Protocol):
    provider_name: str

    def parse_target(self, target: TargetSpec) -> ParsedTarget: ...
    async def score(self, request: ScoreRequest) -> ScoreResponse: ...
```

### Prompt Behavior

The scorer prompt should receive an explicit capability statement for every run:

- `source_check.mode=none`: "Do not claim external validation. You may assess whether
  citations are specific enough to check and whether the artifact is internally
  consistent."
- `source_check.mode=manifest`: "Use only the provided evidence manifest for external
  corroboration claims."
- `source_check.mode=web`: "You may use web search for external validation. Cite sources
  returned by the tool when claiming corroboration."

### Validation Behavior

Add a semantic validation layer beyond score/violation alignment:

1. If `source_check.external_validation_performed=false`, warn or fail on phrases such
   as:
   - "spot-checked",
   - "URLs resolve",
   - "followed links",
   - "externally corroborated",
   - "confirmed by source lookup".
2. If `source_check.mode=web`, require provider tool-use evidence for any Factuality
   reason that claims external corroboration.
3. If a reason says a candidate metric is not a violation, but the violations list cites
   that same candidate as a violation, flag an internal contradiction.
4. If a multi-run summary has score spread greater than one point on any dimension, mark
   that dimension for human review.

## Components

- `prose_eval.config`: load config files, merge defaults, apply CLI overrides.
- `prose_eval.targets`: parse target ids and target config objects.
- `prose_eval.providers`: provider adapters for OpenAI Responses, Anthropic Messages,
  and OpenAI-compatible endpoints.
- `prose_eval.run_plan`: expand presets, targets, repeat counts, and source-check mode
  into concrete runs.
- `prose_eval.run_executor`: execute independent runs with bounded concurrency and stable
  output ordering.
- `prose_eval.eval_score`: apply run config, pass provider tools when enabled, and write
  metadata.
- `prose_eval.eval_report`: extend metadata schema with target, run, and source-check
  settings.
- `prose_eval.multi_run_summary`: summarize repeated or multi-target scoring runs.
- Runbooks and skills: document default no-web behavior and opt-in external validation.

## API Changes

Add `prose-eval score` flags:

```text
--config PATH
--target PROVIDER/MODEL          # may be repeated
--model-arg KEY=VALUE            # may be repeated
--repeat N
--concurrency N                  # default: 2, capped by run count
--preset standard|calibration|web-check|cross-model
--web
--no-web
--source-check none|web|manifest
--evidence-manifest PATH
--out-dir PATH
```

Keep compatibility flags where already present:

```text
--model MODEL
--temperature FLOAT
```

Compatibility rules:

- `--target` is preferred.
- `--model` maps to the current default provider path for one release.
- `--temperature` becomes a provider arg only when the chosen adapter supports it.
- Provider-specific fields such as OpenAI `reasoning.effort`, OpenAI
  `max_output_tokens`, and Anthropic `max_tokens` should be set through target config or
  `--model-arg`.
- `--preset` expands first; explicit CLI flags override the expanded values.
- `--repeat` controls how many independent runs are created. `--concurrency` controls
  how many of those runs may execute at the same time.
- `--concurrency` must be at least `1`; the effective concurrency is
  `min(run_count, requested_concurrency)`.

No change to `prose-eval report validate` network behavior. It remains local.

## Implementation Plan

### Phase 1: Targets, Adapters, and Metadata

- [ ] Add thin Pydantic config models for targets, source-check settings, and run
      parameters.
- [ ] Add config-file loading and CLI override precedence.
- [ ] Add provider adapter interface.
- [ ] Preserve the existing Anthropic Messages behavior through an Anthropic adapter.
- [ ] Add an OpenAI Responses adapter and make `openai/gpt-5.5` the explicit OpenAI
      smoke target.
- [ ] Make `anthropic/claude-opus-4-7` the explicit Anthropic comparison target.
- [ ] Add run and source-check metadata to eval reports, defaulting to
      `source_check.mode=none`.
- [ ] Add prompt capability text for `source_check.mode=none`.
- [ ] Add validation warnings for external-verification claims when no source-check tool
      ran.
- [ ] Update docs and tests so default behavior is explicitly no-web.

### Phase 2: Web and Manifest Source Checks

- [ ] Add OpenAI Responses web-search conversion for `source_check.mode=web`.
- [ ] Add Anthropic web-search conversion for `source_check.mode=web`.
- [ ] Capture OpenAI web-search calls/sources when available.
- [ ] Capture Anthropic `server_tool_use.web_search_requests` from usage metadata when
      available.
- [ ] Keep user-facing web source-check configuration binary: no web tool or provider
      web tool.
- [ ] Add manifest evidence blocks for `source_check.mode=manifest`.
- [ ] Add tests with fake SDK responses proving tools are absent by default and present
      only for web mode.
- [ ] Add runbook guidance for high-stakes source checks.

### Phase 3: Repeat, Multi-Target, and Presets

- [ ] Add `--repeat`, repeated `--target`, `--concurrency`, and `--out-dir` support.
- [ ] Add built-in presets: `standard`, `calibration`, `web-check`, and `cross-model`.
- [ ] Expand presets to normal run parameters before applying explicit CLI overrides.
- [ ] Add bounded concurrent execution with stable output paths and summary ordering.
- [ ] Record partial failures in the multi-run summary without dropping successful run
      reports.
- [ ] Write one eval report per run, never overwriting the input by default.
- [ ] Generate a multi-run summary with score spread, `NA` disagreement, violation
      disagreement, source-check mode, and human-review flags.
- [ ] Add comparison fixtures for same-target repeated runs and cross-model runs.

## Testing Strategy

- Unit-test target parsing for `openai/gpt-5.5`, `anthropic/claude-opus-4-7`,
  generic `anthropic/<model>`, and `openai-compatible/<name>/<model>`.
- Unit-test config discovery, config parsing, and CLI override precedence.
- Unit-test preset expansion and CLI override behavior.
- Unit-test run expansion for `targets x repeat`.
- Unit-test bounded concurrency with fake slow provider calls.
- Unit-test stable report ordering under concurrent completion.
- Unit-test partial failure reporting when one concurrent run fails.
- Unit-test that default score calls pass no provider tool definitions.
- Unit-test the OpenAI Responses adapter with fake client responses, including a
  `gpt-5.5` request and no default tools.
- Unit-test OpenAI web source-check calls with `web_search` only when `--web` or
  `--source-check web` is selected.
- Unit-test the Anthropic adapter with fake client responses, preserving current
  behavior and covering `claude-opus-4-7`.
- Unit-test Anthropic web source-check calls with Anthropic server-tool definitions only
  when selected.
- Unit-test manifest source-check calls adding evidence context without network tools.
- Unit-test metadata round-tripping for targets, run parameters, source-check mode, and
  tool usage.
- Unit-test validation warnings for unsupported external-verification claims.
- Golden-test multi-run summary rendering.
- Keep network-dependent tests out of the default suite; gate real OpenAI `gpt-5.5`
  smoke tests behind `OPENAI_API_KEY` and an explicit opt-in environment variable such
  as `PROSE_EVAL_RUN_NETWORK_TESTS=1`.

## Rollout Plan

1. Ship target/adapters and metadata with default `source_check.mode=none`.
2. Document that current scoring is closed-world unless `--web` or manifest mode is
   explicitly enabled.
3. Add gated OpenAI `gpt-5.5` and Anthropic `claude-opus-4-7` smoke coverage.
4. Add web source-check as opt-in for OpenAI Responses and Anthropic Messages.
5. Add repeat, multi-target, and concurrency parameters.
6. Add the small built-in preset set.
7. Regenerate baseline evals after the metadata and prompt capability text stabilize.

## Open Questions

- Should the first config-file format be YAML only, or should `pyproject.toml` support
  land in the first implementation?
- Should the canonical target syntax be only `provider/model`, or should we also accept
  Promptfoo-style `provider:model` strings as CLI sugar?
- Should `cross-model` always default to `openai/gpt-5.5` and
  `anthropic/claude-opus-4-7`, or should local config be required before enabling it?
- Should Factuality have separate subfields for source discipline vs externally checked
  truth?
- Should source-check manifests store full excerpts, hashes, URLs, retrieval dates, or
  all of the above?
- Should adapters expose capability discovery, or should capability checks stay static
  and conservative?

## References

- [external-validation-tool-setup-2026-05-17.md](../../../../../research-archive/external-validation-tool-setup-2026-05-17.md)
- [eval_score.py](../../../../../tools/prose-eval/src/prose_eval/eval_score.py)
- [eval_report.py](../../../../../tools/prose-eval/src/prose_eval/eval_report.py)
- [practical-prose-eval-single.runbook.md](../../../../../runbooks/practical-prose-eval-single.runbook.md)
- [OpenAI GPT-5.5 model docs](https://developers.openai.com/api/docs/models/gpt-5.5)
- [OpenAI Responses API reference](https://platform.openai.com/docs/api-reference/responses)
- [OpenAI web search tool docs](https://platform.openai.com/docs/guides/tools-web-search)
- [Anthropic models overview](https://docs.anthropic.com/en/docs/about-claude/models/overview)
- [Anthropic web search tool docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/web-search-tool)
- [Inspect AI model providers docs](https://inspect.aisi.org.uk/providers.html)
- [Promptfoo providers docs](https://www.promptfoo.dev/docs/providers/)
- [Promptfoo configuration reference](https://www.promptfoo.dev/docs/configuration/reference/)
- [lm-evaluation-harness interface docs](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/interface.md)
- [LiteLLM getting started and proxy config docs](https://docs.litellm.ai/)
- [OpenAI Evals repository](https://github.com/openai/evals)
