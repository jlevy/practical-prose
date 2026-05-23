---
artifact:
  label: DDOG-r1
  path: <external artifact not in this repo>
derived:
  density:
    links_per_1k_words: 2.6689
    links_per_page: 0.7345
    sentences_per_paragraph: 1.8
    tables_per_1k_words: 0.5132
    tables_per_page: 0.1412
    tags_per_1k_words: 0.0
    tags_per_page: 0.0
    words_per_paragraph: 37.4692
    words_per_sentence: 20.8162
  rubric_rollup:
    assessed_dimensions: 4
    expression_mean: 4.5
    grounding_mean: 0.0
    judgment_mean: 3.5
    na_dimensions: 0
    overall_mean: 4.0
    purpose_mean: 0.0
    reasoning_mean: 0.0
  structure:
    h4_share_of_headings: 0.0
display:
  table_styles:
    palettes:
      practical_prose_dimensions:
        Breadth:
          background: '#eaf2ff'
          foreground: '#173b68'
        Calibration:
          background: '#fff0f3'
          foreground: '#8a1232'
        Clarity:
          background: '#eaf7ec'
          foreground: '#175c36'
        Coherence:
          background: '#eaf7ec'
          foreground: '#175c36'
        Concision:
          background: '#eaf7ec'
          foreground: '#175c36'
        Depth:
          background: '#eaf2ff'
          foreground: '#173b68'
        Factuality:
          background: '#fff6db'
          foreground: '#6b4a03'
        Fairness:
          background: '#fff0f3'
          foreground: '#8a1232'
        Formatting:
          background: '#eaf7ec'
          foreground: '#175c36'
        Discipline:
          background: '#f3ecff'
          foreground: '#4c1d95'
        Organization:
          background: '#eaf7ec'
          foreground: '#175c36'
        Parsimony:
          background: '#f3ecff'
          foreground: '#4c1d95'
        Precision:
          background: '#f3ecff'
          foreground: '#4c1d95'
        Relevance:
          background: '#fff6db'
          foreground: '#6b4a03'
        Robustness:
          background: '#fff0f3'
          foreground: '#8a1232'
        Scope:
          background: '#eaf2ff'
          foreground: '#173b68'
        Soundness:
          background: '#f3ecff'
          foreground: '#4c1d95'
        Consistency:
          background: '#eaf7ec'
          foreground: '#175c36'
        Suitability:
          background: '#eaf2ff'
          foreground: '#173b68'
        Verifiability:
          background: '#fff6db'
          foreground: '#6b4a03'
      practical_prose_groups:
        Expression:
          background: '#eaf7ec'
          foreground: '#175c36'
        Grounding:
          background: '#fff6db'
          foreground: '#6b4a03'
        Judgment:
          background: '#fff0f3'
          foreground: '#8a1232'
        Purpose:
          background: '#eaf2ff'
          foreground: '#173b68'
        Reasoning:
          background: '#f3ecff'
          foreground: '#4c1d95'
      practical_prose_scores:
        '0':
          font_weight: 400
          foreground: '#6b7280'
          opacity: 0.75
        '1':
          font_weight: 800
          foreground: '#991b1b'
        '2':
          font_weight: 650
          foreground: '#92400e'
        '3':
          font_weight: 700
          foreground: '#a16207'
        '4':
          font_weight: 750
          foreground: '#166534'
        '5':
          font_weight: 850
          foreground: '#14532d'
        NA:
          font_weight: 400
          foreground: '#6b7280'
          opacity: 0.65
    tables:
    - encodings:
      - channel: background
        field: Dimension
        palette: practical_prose_dimensions
        source: row
        target: row
      - channel: foreground
        columns:
        - Score
        field: Score
        palette: practical_prose_scores
        source: cell
        target: cell
      - channel: font_weight
        columns:
        - Score
        field: Score
        scale:
          domain:
          - 0
          - 5
          range:
          - 400
          - 850
          type: linear
        source: cell
        target: cell
      headers:
      - match:
          column: Score
        style:
          align: center
          font_weight: 700
      id: practical_prose_single_doc_qualitative
      match:
        columns:
        - Group
        - Dimension
        - Score
        - Reason
    - headers:
      - match:
          column: Value
        style:
          align: right
          font_weight: 700
      id: practical_prose_single_doc_quantitative
      match:
        columns:
        - Section
        - Measure
        - Value
    - encodings:
      - channel: background
        field: Measure
        palette: practical_prose_dimensions
        source: row
        target: row
      headers:
      - match:
          column: Measure
        style:
          font_weight: 700
      id: practical_prose_unified_comparison
      match:
        columns:
        - Approach
        - Aspect
        - Measure
    version: 1
metadata:
  eval_date: '2026-05-07'
  evaluator: figma-eval (Claude Opus 4.7)
  method: 12-dim mechanical migration to 14-dim shape; factuality split duplicated
    to verifiability + factuality; suitability set to mean(expression). Re-score for
    genuine 14-dim baseline.
  notes: 'Scores 1-9 verbatim from a prior 12-dim eval (source not present in this
    repo).

    STALE BASELINE under 20-dim-v1: split coverage -> breadth+depth (same score copied
    as placeholder); structure -> organization (rename only); consistency and
    formatting added as 0 (cannot assess). Re-score before reuse for regression. Original
    rubric_version: 15-dim-v1.


    CLEANUP 2026-05-11 (post 20-dim-v1 migration): 10 dim(s) demoted from sub-5 to
    0 (applicable-but-unassessable) because the original 12-dim eval did not enumerate
    per-dim violations satisfying the 20-dim-v1 alignment property: Suitability(4->0),
    Depth(4->0), Concision(4->0), Organization(4->0), Verifiability(4->0), Factuality(4->0),
    Discipline(4->0), Soundness(4->0), Precision(4->0), Robustness(4->0).
    To restore scores, re-eval under 20-dim-v1 with proper violation citations.'
  rubric_version: 18-dim-v1-stale-baseline
  status: complete
qual:
  expression:
    clarity: 4
    coherence: 5
    concision: 0
    formatting: 0
    organization: 0
    consistency: 0
  grounding:
    factuality: 0
    relevance: 0
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
    discipline: 0
    parsimony: 0
    precision: 0
    soundness: 0
qual_reasons:
  expression: {}
  grounding:
    relevance: Applicable but unassessable in this rebaseline pass; not scored in
      r1 round.
  judgment: {}
  purpose: {}
  reasoning:
    parsimony: Applicable but unassessable in this rebaseline pass; not scored in
      r1 round.
quant:
  bracket_tag_examples: []
  headings:
    h1: 1
    h2: 4
    h3: 20
    h4: 0
    h5: 0
    h6: 0
    total: 25
  links:
    autolink: 0
    bare_urls: 0
    external: 17
    inline: 26
    internal: 9
    reference: 0
    total: 26
  lint:
    banned_register_hits: 1
  provenance:
    bracket_tags: 0
    footnote_defs: 0
    footnote_refs: 0
  size:
    bytes_kb: 67.3
    lines: 1343
    pages_275wpp: 35.4
    paragraphs: 260
    sentences: 468
    words: 9742
  structural:
    code_blocks: 0
    images: 0
    tables: 5
violations:
- description: Extravagant register flourishes (e.g. 'transformative')
  dimension: Clarity
  rule_number: 4
- description: No pre-research priors; no Bayesian shrinkage on probabilities
  dimension: Calibration
  rule_number: 2
- description: No Pass 0 / Pass 1 / Pass 2 structure
  dimension: Calibration
  rule_number: 4
- description: Risk register missing 2 of 5 classes
  dimension: Fairness
  rule_number: 3
- description: Counterintuitive findings all bull-leaning with no tally
  dimension: Fairness
  rule_number: 4
---

# DDOG-r1

**Source:** `<external artifact not in this repo>`  **Scope:** `—`  **Overall mean (20 dims):** 4.00  **Rubric:** `18-dim-v1-stale-baseline`  **Model:** `—`  **Eval date:** 2026-05-07

## Qualitative

| Group | Dimension | Score | Reason |
| --- | --- | ---: | --- |
| **Purpose** | Suitability | 0 |  |
|  | Scope | 0 |  |
|  | Breadth | 0 |  |
|  | Depth | 0 |  |
|  | **Mean** | — | |
| **Expression** | Clarity | 4 |  |
|  | Coherence | 5 |  |
|  | Concision | 0 |  |
|  | Organization | 0 |  |
|  | Consistency | 0 |  |
|  | Formatting | 0 |  |
|  | **Mean** | **4.50** | |
| **Grounding** | Verifiability | 0 |  |
|  | Factuality | 0 |  |
|  | Relevance | 0 | Applicable but unassessable in this rebaseline pass; not scored in r1 round. |
|  | **Mean** | — | |
| **Reasoning** | Discipline | 0 |  |
|  | Soundness | 0 |  |
|  | Precision | 0 |  |
|  | Parsimony | 0 | Applicable but unassessable in this rebaseline pass; not scored in r1 round. |
|  | **Mean** | — | |
| **Judgment** | Calibration | 3 |  |
|  | Fairness | 4 |  |
|  | Robustness | 0 |  |
|  | **Mean** | **3.50** | |
|  | **Overall mean (20 dims)** | **4.00** | |

## Violations

1. **Clarity** (rule 4) — Extravagant register flourishes (e.g. 'transformative')
2. **Calibration** (rule 2) — No pre-research priors; no Bayesian shrinkage on probabilities
3. **Calibration** (rule 4) — No Pass 0 / Pass 1 / Pass 2 structure
4. **Fairness** (rule 3) — Risk register missing 2 of 5 classes
5. **Fairness** (rule 4) — Counterintuitive findings all bull-leaning with no tally

## Quantitative

| Section | Measure | Value |
| --- | --- | ---: |
| Size | Words | 9,742 |
|  | Sentences | 468 |
|  | Paragraphs | 260 |
|  | Lines | 1,343 |
|  | Pages (275 wpp) | 35.4 |
|  | Bytes (KB) | 67.3 |
| Headings | Total (h1/h2/h3/h4) | 25 (1/4/20/0) |
| Structural | Tables | 5 |
|  | Code blocks | 0 |
|  | Images | 0 |
| Links | Total | 26 |
|  | External | 17 |
|  | Internal | 9 |
|  | Bare URLs | 0 |
| Provenance | Bracket tags | 0 |
|  | Footnote refs | 0 |
|  | Footnote defs | 0 |
| Lint | Banned-register hits | 1 |
| Density | Words / sentence | 20.82 |
|  | Words / paragraph | 37.47 |
|  | Sentences / paragraph | 1.80 |
|  | Links / 1k words | 2.67 |
|  | Links / page | 0.73 |
|  | Tables / 1k words | 0.51 |
|  | Tables / page | 0.14 |
|  | Tags / 1k words | 0.00 |
|  | Tags / page | 0.00 |
| Structure (derived) | h4 share of headings | 0.00 |
