---
artifact:
  label: DDOG-r2
  path: <external artifact not in this repo>
derived:
  density:
    links_per_1k_words: 0.0
    links_per_page: 0.0
    sentences_per_paragraph: 1.7069
    tables_per_1k_words: 2.6439
    tables_per_page: 0.7264
    tags_per_1k_words: 2.2914
    tags_per_page: 0.6295
    words_per_paragraph: 39.1276
    words_per_sentence: 22.9232
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
    h4_share_of_headings: 0.3611
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
    h3: 35
    h4: 26
    h5: 0
    h6: 0
    total: 72
  links:
    autolink: 0
    bare_urls: 11
    external: 0
    inline: 0
    internal: 0
    reference: 0
    total: 0
  lint:
    banned_register_hits: 1
  provenance:
    bracket_tags: 26
    footnote_defs: 0
    footnote_refs: 0
  size:
    bytes_kb: 70.7
    lines: 1371
    pages_275wpp: 41.3
    paragraphs: 290
    sentences: 495
    words: 11347
  structural:
    code_blocks: 0
    images: 0
    tables: 30
violations:
- description: Heavy duplication of canonical numbers across §1.x and §2.x
  dimension: Concision
  rule_number: 2
- description: Zero inline links
  dimension: Organization
  rule_number: 5
- description: Some confidence tags missing source pointers
  dimension: Factuality
  rule_number: 3
- description: No Bayesian shrinkage on probability claims
  dimension: Calibration
  rule_number: 2
- description: Counterintuitive findings 6 bull / 2 neutral / 0 bear with no count
  dimension: Fairness
  rule_number: 4
---

# DDOG-r2

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

1. **Concision** (rule 2) — Heavy duplication of canonical numbers across §1.x and §2.x
2. **Organization** (rule 5) — Zero inline links
3. **Factuality** (rule 3) — Some confidence tags missing source pointers
4. **Calibration** (rule 2) — No Bayesian shrinkage on probability claims
5. **Fairness** (rule 4) — Counterintuitive findings 6 bull / 2 neutral / 0 bear with no count

## Quantitative

| Section | Measure | Value |
| --- | --- | ---: |
| Size | Words | 11,347 |
|  | Sentences | 495 |
|  | Paragraphs | 290 |
|  | Lines | 1,371 |
|  | Pages (275 wpp) | 41.3 |
|  | Bytes (KB) | 70.7 |
| Headings | Total (h1/h2/h3/h4) | 72 (1/10/35/26) |
| Structural | Tables | 30 |
|  | Code blocks | 0 |
|  | Images | 0 |
| Links | Total | 0 |
|  | External | 0 |
|  | Internal | 0 |
|  | Bare URLs | 11 |
| Provenance | Bracket tags | 26 |
|  | Footnote refs | 0 |
|  | Footnote defs | 0 |
| Lint | Banned-register hits | 1 |
| Density | Words / sentence | 22.92 |
|  | Words / paragraph | 39.13 |
|  | Sentences / paragraph | 1.71 |
|  | Links / 1k words | 0.00 |
|  | Links / page | 0.00 |
|  | Tables / 1k words | 2.64 |
|  | Tables / page | 0.73 |
|  | Tags / 1k words | 2.29 |
|  | Tags / page | 0.63 |
| Structure (derived) | h4 share of headings | 0.36 |
