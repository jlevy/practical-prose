---
artifact:
  label: NET-r2
  path: <external artifact not in this repo>
derived:
  density:
    links_per_1k_words: 0.0
    links_per_page: 0.0
    sentences_per_paragraph: 1.8524
    tables_per_1k_words: 2.7012
    tables_per_page: 0.7436
    tags_per_1k_words: 3.7258
    tags_per_page: 1.0256
    words_per_paragraph: 39.6162
    words_per_sentence: 21.3865
  rubric_rollup:
    assessed_dimensions: 6
    expression_mean: 4.0
    grounding_mean: 4.0
    judgment_mean: 3.5
    na_dimensions: 0
    overall_mean: 3.8333
    purpose_mean: 0.0
    reasoning_mean: 0.0
  structure:
    h4_share_of_headings: 0.3649
metadata:
  eval_date: '2026-05-07'
  evaluator: figma-eval (Claude Opus 4.7)
  method: 12-dim mechanical migration to 14-dim shape; factuality split duplicated
    to verifiability + factuality; suitability set to mean(expression). Re-score for
    genuine 14-dim baseline.
  notes: 'Scores 1-9 verbatim from a prior 12-dim eval (source not present in this
    repo).

    STALE BASELINE under 18-dim-v1: split coverage -> breadth+depth (same score copied
    as placeholder); structure -> organization (rename only); style_consistency and
    formatting added as 0 (cannot assess). Re-score before reuse for regression. Original
    rubric_version: 15-dim-v1.


    CLEANUP 2026-05-11 (post 18-dim-v1 migration): 8 dim(s) demoted from sub-5 to
    0 (applicable-but-unassessable) because the original 12-dim eval did not enumerate
    per-dim violations satisfying the 18-dim-v1 alignment property: Suitability(4->0),
    Depth(4->0), Clarity(4->0), Verifiability(4->0), Inference Discipline(4->0), Soundness(4->0),
    Precision(4->0), Robustness(4->0). To restore scores, re-eval under 18-dim-v1
    with proper violation citations.'
  rubric_version: 18-dim-v1-stale-baseline
  status: complete
qual:
  expression:
    clarity: 0
    coherence: 5
    concision: 3
    formatting: 0
    organization: 4
    style_consistency: 0
  grounding:
    factuality: 4
    verifiability: 0
  judgment:
    calibration: 3
    fairness: 4
    robustness: 0
  purpose:
    breadth: 0
    depth: 0
    scope: 0
    suitability: 0
  reasoning:
    inference_discipline: 0
    precision: 0
    soundness: 0
qual_reasons:
  expression: {}
  grounding: {}
  judgment: {}
  purpose: {}
  reasoning: {}
quant:
  bracket_tag_examples: []
  headings:
    h1: 1
    h2: 10
    h3: 36
    h4: 27
    h5: 0
    h6: 0
    total: 74
  links:
    autolink: 0
    bare_urls: 0
    external: 0
    inline: 0
    internal: 0
    reference: 0
    total: 0
  lint:
    banned_register_hits: 2
  provenance:
    bracket_tags: 40
    footnote_defs: 0
    footnote_refs: 0
  size:
    bytes_kb: 67.7
    lines: 1284
    pages_275wpp: 39.0
    paragraphs: 271
    sentences: 502
    words: 10736
  structural:
    code_blocks: 0
    images: 0
    tables: 29
violations:
- description: GM compression mentioned 5+ times; DBNRR across 5 places; vinext discussed
    in 7 sections
  dimension: Concision
  rule_number: 2
- description: 0 inline links
  dimension: Organization
  rule_number: 5
- description: Some tags missing source pointer (e.g. SS1.6 GitHub claims)
  dimension: Factuality
  rule_number: 3
- description: No Bayesian shrinkage on probability claims
  dimension: Calibration
  rule_number: 2
- description: Scenario probabilities stated without base-rate triangulation
  dimension: Calibration
  rule_number: 3
- description: 8 counterintuitive findings without bull/bear/neutral count
  dimension: Fairness
  rule_number: 4
---

# NET-r2

**Source:** `<external artifact not in this repo>`  **Scope:** `—`  **Overall mean (18 dims):** 3.83  **Rubric:** `18-dim-v1-stale-baseline`  **Model:** `—`  **Eval date:** 2026-05-07

## Qualitative

| Group | Dimension | Score | Reason |
| --- | --- | ---: | --- |
| Purpose | Suitability | 0 |  |
| Purpose | Scope | 0 |  |
| Purpose | Breadth | 0 |  |
| Purpose | Depth | 0 |  |
| **Purpose** | **Mean** | — | |
| Expression | Clarity | 0 |  |
| Expression | Coherence | 5 |  |
| Expression | Concision | 3 |  |
| Expression | Organization | 4 |  |
| Expression | Style Consistency | 0 |  |
| Expression | Formatting | 0 |  |
| **Expression** | **Mean** | **4.00** | |
| Grounding | Verifiability | 0 |  |
| Grounding | Factuality | 4 |  |
| **Grounding** | **Mean** | **4.00** | |
| Reasoning | Inference Discipline | 0 |  |
| Reasoning | Soundness | 0 |  |
| Reasoning | Precision | 0 |  |
| **Reasoning** | **Mean** | — | |
| Judgment | Calibration | 3 |  |
| Judgment | Fairness | 4 |  |
| Judgment | Robustness | 0 |  |
| **Judgment** | **Mean** | **3.50** | |
| | **Overall mean (18 dims)** | **3.83** | |

## Violations

1. **Concision** (rule 2) — GM compression mentioned 5+ times; DBNRR across 5 places; vinext discussed in 7 sections
2. **Organization** (rule 5) — 0 inline links
3. **Factuality** (rule 3) — Some tags missing source pointer (e.g. SS1.6 GitHub claims)
4. **Calibration** (rule 2) — No Bayesian shrinkage on probability claims
5. **Calibration** (rule 3) — Scenario probabilities stated without base-rate triangulation
6. **Fairness** (rule 4) — 8 counterintuitive findings without bull/bear/neutral count

## Quantitative

| Section | Measure | Value |
| --- | --- | ---: |
| Size | Words | 10,736 |
|  | Sentences | 502 |
|  | Paragraphs | 271 |
|  | Lines | 1,284 |
|  | Pages (275 wpp) | 39.0 |
|  | Bytes (KB) | 67.7 |
| Headings | Total (h1/h2/h3/h4) | 74 (1/10/36/27) |
| Structural | Tables | 29 |
|  | Code blocks | 0 |
|  | Images | 0 |
| Links | Total | 0 |
|  | External | 0 |
|  | Internal | 0 |
|  | Bare URLs | 0 |
| Provenance | Bracket tags | 40 |
|  | Footnote refs | 0 |
|  | Footnote defs | 0 |
| Lint | Banned-register hits | 2 |
| Density | Words / sentence | 21.39 |
|  | Words / paragraph | 39.62 |
|  | Sentences / paragraph | 1.85 |
|  | Links / 1k words | 0.00 |
|  | Links / page | 0.00 |
|  | Tables / 1k words | 2.70 |
|  | Tables / page | 0.74 |
|  | Tags / 1k words | 3.73 |
|  | Tags / page | 1.03 |
| Structure (derived) | h4 share of headings | 0.36 |
