---
artifact:
  label: NET-r1
  path: <external artifact not in this repo>
derived:
  density:
    links_per_1k_words: 7.6117
    links_per_page: 2.0909
    sentences_per_paragraph: 2.2181
    tables_per_1k_words: 1.1031
    tables_per_page: 0.303
    tags_per_1k_words: 0.0
    tags_per_page: 0.0
    words_per_paragraph: 48.2181
    words_per_sentence: 21.7386
  rubric_rollup:
    assessed_dimensions: 6
    expression_mean: 4.6667
    grounding_mean: 4.0
    judgment_mean: 3.5
    na_dimensions: 0
    overall_mean: 4.1667
    purpose_mean: 0.0
    reasoning_mean: 0.0
  structure:
    h4_share_of_headings: 0.0
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
    Depth(4->0), Concision(4->0), Verifiability(4->0), Inference Discipline(4->0),
    Soundness(4->0), Precision(4->0), Robustness(4->0). To restore scores, re-eval
    under 18-dim-v1 with proper violation citations.'
  rubric_version: 18-dim-v1-stale-baseline
  status: complete
qual:
  expression:
    clarity: 4
    coherence: 5
    concision: 0
    formatting: 0
    organization: 5
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
    h2: 16
    h3: 16
    h4: 0
    h5: 0
    h6: 0
    total: 33
  links:
    autolink: 0
    bare_urls: 0
    external: 34
    inline: 69
    internal: 35
    reference: 0
    total: 69
  lint:
    banned_register_hits: 3
  provenance:
    bracket_tags: 0
    footnote_defs: 0
    footnote_refs: 0
  size:
    bytes_kb: 62.5
    lines: 514
    pages_275wpp: 33.0
    paragraphs: 188
    sentences: 417
    words: 9065
  structural:
    code_blocks: 0
    images: 0
    tables: 10
violations:
- description: Register flourishes ("the most narratively charged name", "the most
    violent macro event")
  dimension: Clarity
  rule_number: 4
- description: Zero confidence tags; many derived figures lack inline derivation
  dimension: Factuality
  rule_number: 3
- description: No committed pre-research priors; no Bayesian shrinkage
  dimension: Calibration
  rule_number: 2
- description: No Predictions Registry; scenario probabilities stated without base-rate
  dimension: Calibration
  rule_number: 4
- description: 8 counterintuitive findings without bull/bear/neutral count
  dimension: Fairness
  rule_number: 4
---

# NET-r1

**Source:** `<external artifact not in this repo>`  **Scope:** `—`  **Overall mean (18 dims):** 4.17  **Rubric:** `18-dim-v1-stale-baseline`  **Model:** `—`  **Eval date:** 2026-05-07

## Qualitative

| Group | Dimension | Score | Reason |
| --- | --- | ---: | --- |
| Purpose | Suitability | 0 |  |
| Purpose | Scope | 0 |  |
| Purpose | Breadth | 0 |  |
| Purpose | Depth | 0 |  |
| **Purpose** | **Mean** | — | |
| Expression | Clarity | 4 |  |
| Expression | Coherence | 5 |  |
| Expression | Concision | 0 |  |
| Expression | Organization | 5 |  |
| Expression | Style Consistency | 0 |  |
| Expression | Formatting | 0 |  |
| **Expression** | **Mean** | **4.67** | |
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
| | **Overall mean (18 dims)** | **4.17** | |

## Violations

1. **Clarity** (rule 4) — Register flourishes ("the most narratively charged name", "the most violent macro event")
2. **Factuality** (rule 3) — Zero confidence tags; many derived figures lack inline derivation
3. **Calibration** (rule 2) — No committed pre-research priors; no Bayesian shrinkage
4. **Calibration** (rule 4) — No Predictions Registry; scenario probabilities stated without base-rate
5. **Fairness** (rule 4) — 8 counterintuitive findings without bull/bear/neutral count

## Quantitative

| Section | Measure | Value |
| --- | --- | ---: |
| Size | Words | 9,065 |
|  | Sentences | 417 |
|  | Paragraphs | 188 |
|  | Lines | 514 |
|  | Pages (275 wpp) | 33.0 |
|  | Bytes (KB) | 62.5 |
| Headings | Total (h1/h2/h3/h4) | 33 (1/16/16/0) |
| Structural | Tables | 10 |
|  | Code blocks | 0 |
|  | Images | 0 |
| Links | Total | 69 |
|  | External | 34 |
|  | Internal | 35 |
|  | Bare URLs | 0 |
| Provenance | Bracket tags | 0 |
|  | Footnote refs | 0 |
|  | Footnote defs | 0 |
| Lint | Banned-register hits | 3 |
| Density | Words / sentence | 21.74 |
|  | Words / paragraph | 48.22 |
|  | Sentences / paragraph | 2.22 |
|  | Links / 1k words | 7.61 |
|  | Links / page | 2.09 |
|  | Tables / 1k words | 1.10 |
|  | Tables / page | 0.30 |
|  | Tags / 1k words | 0.00 |
|  | Tags / page | 0.00 |
| Structure (derived) | h4 share of headings | 0.00 |
