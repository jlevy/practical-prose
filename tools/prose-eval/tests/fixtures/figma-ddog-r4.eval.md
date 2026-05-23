---
artifact:
  label: DDOG-r4
  path: <external artifact not in this repo>
derived:
  density:
    links_per_1k_words: 1.9182
    links_per_page: 0.5275
    sentences_per_paragraph: 1.8114
    tables_per_1k_words: 2.5575
    tables_per_page: 0.7033
    tags_per_1k_words: 5.1151
    tags_per_page: 1.4066
    words_per_paragraph: 42.1279
    words_per_sentence: 23.2565
  rubric_rollup:
    assessed_dimensions: 11
    expression_mean: 4.25
    grounding_mean: 5.0
    judgment_mean: 5.0
    na_dimensions: 0
    overall_mean: 4.6364
    purpose_mean: 4.0
    reasoning_mean: 5.0
  structure:
    h4_share_of_headings: 0.3333
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
        Inference Discipline:
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
        Style Consistency:
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
    as placeholder); structure -> organization (rename only); style_consistency and
    formatting added as 0 (cannot assess). Re-score before reuse for regression. Original
    rubric_version: 15-dim-v1.


    CLEANUP 2026-05-11 (post 20-dim-v1 migration): 4 dim(s) demoted from sub-5 to
    0 (applicable-but-unassessable) because the original 12-dim eval did not enumerate
    per-dim violations satisfying the 20-dim-v1 alignment property: Suitability(4->0),
    Inference Discipline(4->0), Precision(4->0), Robustness(4->0). To restore scores,
    re-eval under 20-dim-v1 with proper violation citations.'
  rubric_version: 18-dim-v1-stale-baseline
  status: complete
qual:
  expression:
    clarity: 4
    coherence: 5
    concision: 4
    formatting: 0
    organization: 4
    style_consistency: 0
  grounding:
    factuality: 5
    relevance: 5
    verifiability: 5
  judgment:
    calibration: 5
    fairness: 5
    robustness: 0
  purpose:
    breadth: 0
    depth: 4
    scope: 0
    suitability: 0
  reasoning:
    inference_discipline: 0
    parsimony: 0
    precision: 0
    soundness: 5
qual_reasons:
  expression: {}
  grounding:
    relevance: Sources tied directly to the operational task; no extraneous citations
      identified.
  judgment: {}
  purpose: {}
  reasoning:
    parsimony: Applicable but unassessable; soundness scored in r4 but parsimony not
      reviewed.
quant:
  bracket_tag_examples: []
  headings:
    h1: 1
    h2: 11
    h3: 36
    h4: 24
    h5: 0
    h6: 0
    total: 72
  links:
    autolink: 0
    bare_urls: 7
    external: 0
    inline: 24
    internal: 24
    reference: 0
    total: 24
  lint:
    banned_register_hits: 0
  provenance:
    bracket_tags: 64
    footnote_defs: 0
    footnote_refs: 0
  size:
    bytes_kb: 78.7
    lines: 1389
    pages_275wpp: 45.5
    paragraphs: 297
    sentences: 538
    words: 12512
  structural:
    code_blocks: 0
    images: 0
    tables: 32
violations:
- description: Residual register choice ("the densest innovation in the window")
  dimension: Clarity
  location: L946
  rule_number: 4
- description: Some duplication remains (RPO +53% across §1.3, §2.0, §2.2, §2.8)
  dimension: Concision
  rule_number: 2
- description: 0 external inline links to primary sources
  dimension: Organization
  rule_number: 5
- description: Engineering telemetry section less deep than its strategic relevance
  dimension: Depth
  rule_number: 4
---

# DDOG-r4

**Source:** `<external artifact not in this repo>`  **Scope:** `—`  **Overall mean (20 dims):** 4.64  **Rubric:** `18-dim-v1-stale-baseline`  **Model:** `—`  **Eval date:** 2026-05-07

## Qualitative

| Group | Dimension | Score | Reason |
| --- | --- | ---: | --- |
| **Purpose** | Suitability | 0 |  |
|  | Scope | 0 |  |
|  | Breadth | 0 |  |
|  | Depth | 4 |  |
|  | **Mean** | **4.00** | |
| **Expression** | Clarity | 4 |  |
|  | Coherence | 5 |  |
|  | Concision | 4 |  |
|  | Organization | 4 |  |
|  | Style Consistency | 0 |  |
|  | Formatting | 0 |  |
|  | **Mean** | **4.25** | |
| **Grounding** | Verifiability | 5 |  |
|  | Factuality | 5 |  |
|  | Relevance | 5 | Sources tied directly to the operational task; no extraneous citations identified. |
|  | **Mean** | **5.00** | |
| **Reasoning** | Inference Discipline | 0 |  |
|  | Soundness | 5 |  |
|  | Precision | 0 |  |
|  | Parsimony | 0 | Applicable but unassessable; soundness scored in r4 but parsimony not reviewed. |
|  | **Mean** | **5.00** | |
| **Judgment** | Calibration | 5 |  |
|  | Fairness | 5 |  |
|  | Robustness | 0 |  |
|  | **Mean** | **5.00** | |
|  | **Overall mean (20 dims)** | **4.64** | |

## Violations

1. **Clarity** (rule 4) — Residual register choice ("the densest innovation in the window") *Location:* L946.
2. **Concision** (rule 2) — Some duplication remains (RPO +53% across §1.3, §2.0, §2.2, §2.8)
3. **Organization** (rule 5) — 0 external inline links to primary sources
4. **Depth** (rule 4) — Engineering telemetry section less deep than its strategic relevance

## Quantitative

| Section | Measure | Value |
| --- | --- | ---: |
| Size | Words | 12,512 |
|  | Sentences | 538 |
|  | Paragraphs | 297 |
|  | Lines | 1,389 |
|  | Pages (275 wpp) | 45.5 |
|  | Bytes (KB) | 78.7 |
| Headings | Total (h1/h2/h3/h4) | 72 (1/11/36/24) |
| Structural | Tables | 32 |
|  | Code blocks | 0 |
|  | Images | 0 |
| Links | Total | 24 |
|  | External | 0 |
|  | Internal | 24 |
|  | Bare URLs | 7 |
| Provenance | Bracket tags | 64 |
|  | Footnote refs | 0 |
|  | Footnote defs | 0 |
| Lint | Banned-register hits | 0 |
| Density | Words / sentence | 23.26 |
|  | Words / paragraph | 42.13 |
|  | Sentences / paragraph | 1.81 |
|  | Links / 1k words | 1.92 |
|  | Links / page | 0.53 |
|  | Tables / 1k words | 2.56 |
|  | Tables / page | 0.70 |
|  | Tags / 1k words | 5.12 |
|  | Tags / page | 1.41 |
| Structure (derived) | h4 share of headings | 0.33 |
