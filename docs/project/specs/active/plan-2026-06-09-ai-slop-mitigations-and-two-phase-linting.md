# Feature: AI-Slop Mitigations Doc and Two-Phase Prose Linting

**Date:** 2026-06-09 (last updated 2026-06-09)

**Author:** Joshua Levy (github.com/jlevy) with agent assistance

**Status:** Draft

## Overview

Two deliverables that turn the AI-prose research
([research-2026-05-25-ai-prose-detection.md](../../research/research-2026-05-25-ai-prose-detection.md))
into shipped artifacts:

1. **An expanded guidelines doc**,
   [ai-prose-corrections.md](../../../ai-prose-corrections.md) (merged and shipped),
   holding the full catalog: the lexical tells plus drafting-time directives and the
   structural AI-tell patterns that grep cannot catch — false agency, negative listing,
   dramatic fragmentation, rhetorical setups, narrator-from-a-distance — adapted from
   Hardik Pandya’s stop-slop (MIT, credited) with absolutist rules moderated into
   attention flags. A compact digest ships as
   [shortcuts/ai-prose-checklist.md](../../../../shortcuts/ai-prose-checklist.md) for
   loading into drafting contexts.
2. **Machine-readable rule data files plus a two-phase lint pipeline** in pprose: a
   cheap, fast detection pass (regex → fuzzy → optional cheap model) that surfaces
   *candidate* violations, then a parallel verification pass where a stronger model
   judges each candidate against the specific rule and proposes the correction.

The two-phase design is the core architectural bet: handing a long rule list to a single
agent degrades compliance as the list grows; detecting candidates cheaply and fanning
out the much smaller violation set to capable models in parallel is far more reliable,
and each verifier sees only one rule and one span — a small, checkable task.

## Goals

- Ship the merged `docs/ai-prose-corrections.md` (lexical catalog plus structural
  patterns) and the `shortcuts/ai-prose-checklist.md` digest, wired into the
  related-docs graph and the pprose guidelines and shortcuts resources.
- Define a rule-data schema that encodes each tell once, with match specifications at
  multiple tiers (exact / fuzzy / semantic exemplars / structural notes) plus correction
  text and genre exceptions.
- Implement `pprose lint` (name open): phase-A detection producing
  `Match(rule_id, span, tier, score)` records; phase-B verification fanning candidates
  out to a stronger model in parallel, returning confirmed violations with proposed
  corrections.
- Keep rule IDs stable and matched to doc anchors so the lint output and the corrections
  doc never drift apart.

## Non-Goals

- **No AI-vs-human verdict.** The research (pp-ne5w, pp-3vt3) settled this: detection
  classifiers are unreliable and not the project’s job.
  The linter flags *constructions*, never authorship.
- **No voice matching.** Same scope boundary as the rest of the project.
- **Not the visual overlay renderer** (pp-xrqd / pp-dc53 territory).
  The lint pipeline emits records the future overlay can consume, but the renderer is a
  separate effort.
- **No embedding/vector tier in v1.** The pp-84ya research recommends BGE-small + FAISS
  as tier 2; v1 substitutes a cheap-LLM detection pass and leaves the embedding tier as
  a later optimization.

## Background

- Research doc Phase 1 cataloged the tells and concluded the editorial rule-based
  approach beats classifiers; Phase 2 (pp-84ya) designed a four-tier soft-match
  architecture and found that every shipping AI-tell catalog is pure regex — the only
  “soft” matchers (stop-slop itself, claude-slop-detector) just prompt an LLM with the
  whole rule list.
- stop-slop (cloned to `attic/stop-slop`, reviewed 2026-06-09) contributes five
  structural categories we lacked, ~30 throat-clearing/filler phrases, and good
  before/after exemplars.
  MIT-licensed; credited in the corrections doc and bibliography.
- pprose already has the seed of phase A: `metrics.py` ships a `banned-register` regex
  metric with a default word list and `--banned-words-file` override, plus golden-test
  fixtures (`test_fixtures/practical_prose_metrics/expected/banned_register.yaml`).
- The moderation principle (user-approved): absolutist source rules become *attention
  flags* — patterns that deserve a look at high density, not bans.

### Leximetry and chopdiff fit (reviewed 2026-06-09)

[leximetry](https://github.com/jlevy/leximetry) (`wrk/kmd/leximetry`) was reviewed for
reusable pieces.
Verdict: **adopt its patterns, not new dependencies** — its entire stack
(chopdiff, pydantic-ai, aiolimiter `gather_limited`) is already in pprose’s dependency
list.

- **chopdiff `TextDoc` is the document model for the linter.** Already a pprose dep
  (`chopdiff==0.3.1`). Markdown-aware paragraph/sentence segmentation with *exact source
  spans* and offset inversion (`sentence_at_offset`, `block_at_offset`) — precisely what
  Match spans, ±2-sentence verification context, and code-block/frontmatter skipping
  need. See chopdiff’s `textdoc-spec.md`.
- **Per-judgment focused prompts** (leximetry `evaluate_single_metric`): one small Agent
  call per metric, fanned out with `gather_limited` — the proven precedent for phase B’s
  one-call-per-candidate design.
- **Structured output over parse-and-fallback:** leximetry parses `"SCORE (REASON)"`
  strings with regex fallbacks (`Score.parse`); the linter should instead use
  pydantic-ai `output_type` schemas (as pprose’s `eval_score.py` already does) so
  verdicts never need fragile parsing.
- **Rich terminal report** (`report_output.py`, `size_stats.py`): visual precedent for
  `pprose lint` output; pprose’s own `table_styles.py` conventions take precedence.

## Design

### Components

```
docs/
  ai-prose-corrections.md          # the merged catalog: lexical + structural
shortcuts/
  ai-prose-checklist.md            # compact digest for drafting contexts
tools/pprose/src/pprose/
  resources/rules/                 # NEW: machine-readable rule data
    throat-clearing.yaml
    false-agency.yaml
    self-negating-parallel.yaml
    vague-declaratives.yaml
    ... (one file per category, ~10 categories in v1)
  lint_detect.py                   # NEW: phase A — regex + fuzzy detection
  lint_verify.py                   # NEW: phase B — parallel LLM verification
  cli.py                           # gains `pprose lint` command
```

### Rule-data schema

One YAML file per category; one entry per rule.
Schema sketch:

```yaml
# resources/rules/false-agency.yaml
category: false-agency
doc_anchor: ai-prose-corrections.md#false-agency
severity: flag          # flag | cut  (mirrors Flags vs. Bans)
rules:
  - id: false-agency.social-verb
    summary: Inanimate subject performing a social/human action
    correction: >
      Name the human. "The team fixed it that week" beats
      "the complaint becomes a fix."
    exceptions:
      - Technical idiom (the function returns, the test fails)
    detect:
      exact:            # tier 0: literal phrases, case-insensitive
        - "the data tells us"
        - "the decision emerged"
      fuzzy:            # tier 1: fuzzysearch needles, max_l_dist edit tolerance
        - needle: "becomes a fix"
          max_l_dist: 1
      template:         # tier 1a: RE2-compatible (?i) regex for slot patterns
        - 'the \w+ becomes an? \w+'
      model_hints: >    # tier 2 (cheap-model pass): one-line description
        Abstract noun as subject of a verb implying human agency
        (becomes, emerges, decides, rewards, tells, shifts, steers).
      structural: >     # tier 3 (future DependencyMatcher template), notes only in v1
        nsubj is inanimate/abstract noun; verb lemma in agency set.
    examples:           # exemplars for verification context + future tier 2
      bad: "A complaint becomes a fix within the week."
      good: "The team fixed the complaint within the week."
    source: stop-slop   # attribution
    first_flagged: 2026-01
```

Design points:

- `id` and `doc_anchor` are the contract keeping code and prose in sync (the same
  convention pp-zraz recommended for a lint pack).
- `first_flagged` supports the tell-decay finding (Geng & Trotta): rules can age out.
- `severity: flag` vs `cut` carries the Flags-vs-Bans moderation into the data so the
  pipeline can treat them differently (cut-tier hits can ship as errors; flag-tier hits
  only surface above a density threshold or with verifier confirmation).

### Model selection (researched 2026-06-09)

Verified pricing and capability research (see research beads) settles the model choices:

- **Phase B default: Haiku 4.5** (`claude-haiku-4-5`, $1/$5 per MTok, structured output
  GA). The verification task — one rule, one span, ±2 sentences, verdict + fix — is the
  regime where small judges are reliable: the LLM-judge literature finds binary
  per-criterion verdicts far more stable than holistic rubric scoring, and GLIDER
  (arXiv:2412.14140) shows a 3.8B judge matching GPT-4o-mini on focused criteria.
  Output schema includes `confidence`; route `uncertain` verdicts to Sonnet 4.6 (at ~10%
  escalation this adds well under a cent per doc).
- **Phase A optional model pass: Gemini 2.5 Flash-Lite** ($0.10/$0.40, native JSON
  schema) or a Groq-served Llama 3.1 8B ($0.05/$0.08, ~840 tok/s) — both effectively
  free at CI scale.
- **Cost reality:** all-Haiku worst case is ~~3.6¢ per 5K-word doc (~~$11/day at 300
  docs/day); Flash-Lite phase A + Haiku phase B is ~2¢/doc.
  Cost is settled; pick on quality and ops.
- **v2 upgrade path (non-generative): GLiNER2** (205M params, Apache-2.0, CPU-only,
  pip-installable). Each rule’s `model_hints` becomes a zero-shot span-extraction label;
  near-constant cost in label count (bi-encoder precomputes label embeddings); expect
  strong recall on phrase-level rules, weak on structural rules — validate per rule.
  No published open-weight encoder classifies AI-register at sentence level against an
  editorial rule taxonomy; our rule-exemplar data could eventually fine-tune a
  ModernBERT multi-label classifier (build, not buy).
- **Local mode:** opt-in only (`--local`); a 4-bit 4B model is a 2.5–3 GB download —
  hostile as a default for a uvx-installed CLI. Constrained decoding (GBNF / Outlines)
  makes 4B-class models usable for span JSON despite raw-quality limits.
- **Fine-tuning: not yet.** Anthropic has no 4.x tuning; OpenAI is winding down
  self-serve fine-tuning (May 2026); the path that eventually pays is encoder-side
  (SetFit / ModernBERT) once ~50–100 labeled exemplars per category accumulate.
- **Batch APIs** (50% discount, ~24h turnaround) are a skip for v1; adopt only for
  nightly full-corpus re-lints.
- **Caching caveat:** Haiku’s prompt-cache minimum is 4,096 tokens; a ~1K rule-hints
  prompt won’t cache. Either skip caching or fatten the shared prefix past 4K (full rule
  catalog
  + exemplars) to get 0.1× reads.

### Two-phase pipeline

**Phase A — detect (cheap, local, fast).**

Native-matcher selection (researched and locally benchmarked 2026-06-09 on Apple
Silicon; 500 patterns vs.
a ~10K-word doc):

| Engine | Role | Scan time | License | Notes |
| --- | --- | --- | --- | --- |
| `ahocorasick-rs` | literal phrase bank | **0.52 ms** | Apache-2.0 | LeftmostLongest; casefold the doc + patterns yourself (no native CI); post-filter hits for word boundaries (two char checks per hit) |
| `google-re2` | template patterns | **0.24 ms** (Set) | BSD | linear-time, no catastrophic backtracking; `(?i)` per-pattern `finditer` for spans; `re2.Set` as prefilter past ~100 templates |
| `fuzzysearch` | edit-tolerant subset | ~0.55 ms/pattern at d=1 | MIT | true substring-with-edits; keep the fuzzy subset ≤50 patterns (≈30 ms) or pre-gate by AC hits on anchor words |

All three ship macOS arm64 + Linux x64 wheels, are actively maintained (releases Oct
2025 – Nov 2025), and are months past the 14-day supply-chain cool-off.
Upgrade path: **hyperscan** (python-hyperscan 0.8.2, Mar 2026 — statically linked
Vectorscan, real arm64 wheels, native caseless *and* per-pattern approximate matching)
consolidates templates + fuzzy into one pass once banks reach the thousands.
Rejected for v1: spaCy Matcher (heavy dep, tokenization alone costs more than our whole
budget; optional extra later for true POS templates), `rapidfuzz` cdist as the primary
fuzzy pass (~200 ms full-bank vs.
sentences — CI-tier only), flashtext (dead since 2018), stringzilla (single-needle,
wrong shape), rure (dead, no arm64).

1. Tier 0: casefolded `ahocorasick-rs` pass over the whole document for all literal
   phrases (plus the existing `banned-register` regex machinery in `metrics.py` for
   word-level entries).
   Budget: <1 ms.
2. Tier 1a: template patterns as individual `(?i)` RE2 regexes; spans via `finditer`.
   Budget: <5 ms.
3. Tier 1b: `fuzzysearch.find_near_matches` (max_l_dist 1–2) for the curated fuzzy
   subset. Budget: ~30 ms.
4. Tier 2 (optional, `--detect-model`): one cheap-model call per document *chunk* (not
   per rule) with the `model_hints` lines for all rules, returning candidate spans +
   rule IDs. Gemini 2.5 Flash-Lite or Groq-8B per the model research; this replaces the
   embedding tier in v1.

Whole-document detection comfortably fits a 50 ms per-save budget.

Output: list of `Match` records — `rule_id`, char span, matched text, tier, score.
Deduplicate overlapping spans (highest tier wins).

**Phase B — verify and remediate (capable model, parallel).**

For each candidate (typically a handful per document, not hundreds):

- One verification call per candidate, run in parallel (reuse pprose’s existing
  `_concurrency.py`), with a focused prompt containing only: the span in context (±2
  sentences), the one rule’s summary + correction + exceptions, and the bad/good
  exemplar.
- The verifier returns: `verdict` (violation / licensed use / false positive), `reason`,
  and — when a violation — a `proposed_fix` honoring the rule’s correction guidance.
- Flag-severity rules additionally get the density context (how many sibling hits in the
  document) so the verifier can apply the “density is the tell” test.

Output modes: pretty terminal report, `--json` for tooling, and an exit code gated only
on confirmed cut-severity violations (so CI can adopt it without flag-tier noise).

### CLI

```
pprose lint <file.md> [--detect-model MODEL] [--verify/--no-verify]
            [--verify-model MODEL] [--json] [--rules DIR]
```

Default: tiers 0–1 detection + verification on.
`--no-verify` gives the raw candidate list (fast, deterministic, CI-friendly).

## Implementation Plan

### Phase 1: Docs

- [x] Merge the mitigations draft into `docs/ai-prose-corrections.md` (lexical catalog
  plus structural patterns, one coverage map) and ship `shortcuts/ai-prose-checklist.md`
  as the compact drafting digest.
- [ ] Update bibliography: note the stop-slop adaptation in the existing Pandya entry.
- [ ] Wire the doc and shortcut into the pprose-copy-edit and pprose-full-edit skills so
  edit passes load the catalog.

### Phase 2: Rule data

- [ ] Define and document the rule-data YAML schema (above) with a small schema
  validator.
- [ ] Author v1 rule files (~10 categories): throat-clearing, false agency, negative
  listing, dramatic fragmentation, rhetorical setups, narrator-from-a-distance, vague
  declaratives, self-negating parallel, business-jargon swaps, attention-flag densities
  (adverbs, lazy extremes).
- [ ] Golden tests: fixture documents with known violations → expected Match records
  (mirror the existing `practical_prose_metrics` fixture pattern).

### Phase 3: Pipeline

- [ ] `lint_detect.py`: tier 0 + tier 1 over the rule files; Match records; span dedup.
- [ ] `lint_verify.py`: parallel per-candidate verification with focused prompts;
  verdict + proposed fix.
- [ ] `pprose lint` CLI with `--json`, `--no-verify`, exit-code gating.
- [ ] Optional tier 2 cheap-model detection behind `--detect-model`.

## Testing Strategy

- Golden tests for detection: fixture docs covering every rule, plus *licensed-use*
  fixtures that must NOT match (technical idiom for false agency; benchmarked
  *state-of-the-art*; single emphatic fragment).
- Verification tested with recorded-response fixtures (no live calls in CI), plus one
  smoke test behind an env flag.
- Dogfood pass: run the linter over `docs/` itself; the project’s own docs should come
  back clean or with explainable flags.

## Rollout Plan

- Land docs first (Phase 1) — immediately useful to agents via guidelines.
- Rule data + detection (`--no-verify` mode) next — deterministic, CI-safe.
- Verification last — needs API key wiring and cost consideration.

## Open Questions

- Command name: `pprose lint` vs `pprose tells` vs folding into `pprose score` as a
  metric family?
- Where rule data lives: `resources/rules/` inside the package (zero-install friendly)
  vs `data/` at repo root (easier doc-adjacent editing)?
  Spec assumes in-package.
- Should flag-severity densities (adverbs per paragraph) be computed in `metrics.py` as
  numeric metrics instead of lint matches?
  They fit the metrics model better.
- ~~v1 fuzzy tier: is `rapidfuzz` windowing alone good enough?~~ **Answered 2026-06-09**
  by benchmarked research: `ahocorasick-rs` + `google-re2` + `fuzzysearch` from the
  start; rapidfuzz cdist is CI-tier only.
  The schema’s `FuzzyPattern` carries `max_l_dist` for fuzzysearch, not a rapidfuzz
  similarity threshold.
  See *Native-matcher selection* in the pipeline section.

## References

- [ai-prose-corrections.md](../../../ai-prose-corrections.md) (the merged catalog)
- [ai-prose-checklist.md](../../../../shortcuts/ai-prose-checklist.md) (the digest)
- [research-2026-05-25-ai-prose-detection.md](../../research/research-2026-05-25-ai-prose-detection.md)
  — esp. pp-84ya (four-tier soft-match architecture), pp-zraz (rule-ID contract), pp-3vt3
  (no classifier verdicts)
- `attic/stop-slop` — source material (MIT, Hardik Pandya)
- `tools/pprose/src/pprose/metrics.py` — existing banned-register machinery

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
