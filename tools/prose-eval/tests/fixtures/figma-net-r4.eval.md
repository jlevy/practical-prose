---
artifact:
  label: NET-r4
  path: <external artifact not in this repo>
derived:
  density:
    links_per_1k_words: 4.1999
    links_per_page: 1.1538
    sentences_per_paragraph: 1.8351
    tables_per_1k_words: 3.3599
    tables_per_page: 0.9231
    tags_per_1k_words: 6.7199
    tags_per_page: 1.8462
    words_per_paragraph: 37.9947
    words_per_sentence: 20.7043
  rubric_rollup:
    assessed_dimensions: 11
    expression_mean: 4.5
    grounding_mean: 5.0
    judgment_mean: 5.0
    na_dimensions: 0
    overall_mean: 4.7273
    purpose_mean: 4.0
    reasoning_mean: 5.0
  structure:
    h4_share_of_headings: 0.254
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


    CLEANUP 2026-05-11 (post 20-dim-v1 migration): 4 dim(s) demoted from sub-5 to
    0 (applicable-but-unassessable) because the original 12-dim eval did not enumerate
    per-dim violations satisfying the 20-dim-v1 alignment property: Suitability(4->0),
    Discipline(4->0), Precision(4->0), Robustness(4->0). To restore scores,
    re-eval under 20-dim-v1 with proper violation citations.'
  rubric_version: 18-dim-v1-stale-baseline
  status: complete
qual:
  expression:
    clarity: 4
    coherence: 5
    concision: 5
    formatting: 0
    organization: 4
    consistency: 0
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
    discipline: 0
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
    h2: 10
    h3: 36
    h4: 16
    h5: 0
    h6: 0
    total: 63
  links:
    autolink: 0
    bare_urls: 0
    external: 0
    inline: 30
    internal: 30
    reference: 0
    total: 30
  lint:
    banned_register_hits: 0
  provenance:
    bracket_tags: 48
    footnote_defs: 0
    footnote_refs: 0
  size:
    bytes_kb: 45.3
    lines: 629
    pages_275wpp: 26.0
    paragraphs: 188
    sentences: 345
    words: 7143
  structural:
    code_blocks: 0
    images: 0
    tables: 24
violations:
- description: Compressed phrasing risks ambiguity in §2.4 Strategic-horizon mapping
    ("Acts 1-4")
  dimension: Clarity
  rule_number: 4
- description: 0 external inline links to primary sources
  dimension: Organization
  rule_number: 5
- description: §1.8 pricing section less deep than its strategic relevance
  dimension: Depth
  rule_number: 4
---

# NET-r4

**Source:** `<external artifact not in this repo>`  **Scope:** `—`  **Overall mean (20 dims):** 4.73  **Rubric:** `18-dim-v1-stale-baseline`  **Model:** `—`  **Eval date:** 2026-05-07

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
|  | Concision | 5 |  |
|  | Organization | 4 |  |
|  | Consistency | 0 |  |
|  | Formatting | 0 |  |
|  | **Mean** | **4.50** | |
| **Grounding** | Verifiability | 5 |  |
|  | Factuality | 5 |  |
|  | Relevance | 5 | Sources tied directly to the operational task; no extraneous citations identified. |
|  | **Mean** | **5.00** | |
| **Reasoning** | Discipline | 0 |  |
|  | Soundness | 5 |  |
|  | Precision | 0 |  |
|  | Parsimony | 0 | Applicable but unassessable; soundness scored in r4 but parsimony not reviewed. |
|  | **Mean** | **5.00** | |
| **Judgment** | Calibration | 5 |  |
|  | Fairness | 5 |  |
|  | Robustness | 0 |  |
|  | **Mean** | **5.00** | |
|  | **Overall mean (20 dims)** | **4.73** | |

## Violations

1. **Clarity** (rule 4) — Compressed phrasing risks ambiguity in §2.4 Strategic-horizon mapping ("Acts 1-4")
2. **Organization** (rule 5) — 0 external inline links to primary sources
3. **Depth** (rule 4) — §1.8 pricing section less deep than its strategic relevance

## Quantitative

| Section | Measure | Value |
| --- | --- | ---: |
| Size | Words | 7,143 |
|  | Sentences | 345 |
|  | Paragraphs | 188 |
|  | Lines | 629 |
|  | Pages (275 wpp) | 26.0 |
|  | Bytes (KB) | 45.3 |
| Headings | Total (h1/h2/h3/h4) | 63 (1/10/36/16) |
| Structural | Tables | 24 |
|  | Code blocks | 0 |
|  | Images | 0 |
| Links | Total | 30 |
|  | External | 0 |
|  | Internal | 30 |
|  | Bare URLs | 0 |
| Provenance | Bracket tags | 48 |
|  | Footnote refs | 0 |
|  | Footnote defs | 0 |
| Lint | Banned-register hits | 0 |
| Density | Words / sentence | 20.70 |
|  | Words / paragraph | 37.99 |
|  | Sentences / paragraph | 1.84 |
|  | Links / 1k words | 4.20 |
|  | Links / page | 1.15 |
|  | Tables / 1k words | 3.36 |
|  | Tables / page | 0.92 |
|  | Tags / 1k words | 6.72 |
|  | Tags / page | 1.85 |
| Structure (derived) | h4 share of headings | 0.25 |
