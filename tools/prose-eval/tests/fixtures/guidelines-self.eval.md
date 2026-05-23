---
artifact:
  label: guidelines-self
  path: docs/practical-prose-guidelines.md
  scope_class: memo
derived:
  density:
    links_per_1k_words: 0.0
    links_per_page: 0.0
    sentences_per_paragraph: 1.795
    tables_per_1k_words: 0.2055
    tables_per_page: 0.0565
    tags_per_1k_words: 0.0
    tags_per_page: 0.0
    words_per_paragraph: 30.2174
    words_per_sentence: 16.8339
  rubric_rollup:
    assessed_dimensions: 15
    expression_mean: 4.0
    grounding_mean: 4.0
    judgment_mean: 0.0
    na_dimensions: 5
    overall_mean: 4.1333
    purpose_mean: 4.5
    reasoning_mean: 4.0
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
  eval_date: '2026-05-10'
  evaluator: subagent (Claude Opus 4.7)
  method: 20-dim-v1 self-eval via parallel subagent
  notes: Re-scored 2026-05-11 under 20-dim-v1 as part of practical-prose v0.4 calibration
    set. Self-eval of practical-prose-guidelines.md. NA on Discipline /
    Calibration / Fairness / Robustness (this is a prescriptive guidelines doc, not
    an analytical artifact). Replaces prior 15-dim-v1-stale-baseline.
  rubric_version: 20-dim-v1
  status: complete
qual:
  expression:
    clarity: 4
    coherence: 4
    concision: 4
    formatting: 4
    organization: 4
    consistency: 4
  grounding:
    factuality: 4
    relevance: 4
    verifiability: 4
  judgment:
    calibration: NA
    fairness: NA
    robustness: NA
  purpose:
    breadth: 5
    depth: 4
    scope: 4
    suitability: 5
  reasoning:
    discipline: NA
    parsimony: NA
    precision: 4
    soundness: 4
qual_reasons:
  expression:
    clarity: Clear, concrete prose throughout; examples are well-chosen (error-rate
      ladder of inference example is excellent); five banned-register words appear
      at L197-198 but only as illustrative examples.
    coherence: Ideas progress logically from Purpose through Judgment; each dimension
      section has consistent structure; Common Pitfalls section introduces concepts
      like 'compliance pressure' without explicit setup from preceding rule sections.
    concision: Scope Rule 2.4 and Breadth Rule 3.4 are near-verbatim duplicates; Pre-Publish
      Self-Audit compresses rules into a checklist that adds organizational value
      but overlaps substantially with rule sections.
    formatting: Markdown renders correctly; tables valid; code spans and emphasis
      used consistently; no YAML frontmatter despite the doc's own Rule 10.5 requiring
      headers/metadata/footers.
    organization: Logical heading hierarchy (h1 > h2 > h3); dimension table provides
      a useful overview; sections arranged by group in rubric order; internal cross-references
      use named § references but none are hyperlinked, making navigation harder in
      an 800-line doc.
    consistency: 'Contractions mixed with formal non-contractions without a
      stated policy: ''can''t'' and ''don''t'' alongside ''does not'', ''cannot'',
      ''should not''; otherwise consistent.'
  grounding:
    factuality: Argyris adaptation honestly stated; alignment claim is design intent
      (low factuality risk); 'Coverage' at L88 is a stale name that no longer matches
      the rubric's terminology.
    relevance: Sources and rules bear on each dimension's scope; one or two cross-references
      stretch toward adjacent topics.
    verifiability: Argyris citation at L485 names the work but omits co-authors (Putnam,
      Smith) and page numbers; alignment claim at L11-12 asserted without a worked
      example or test.
  judgment:
    calibration: 'NA: The document makes no probability, forecast, confidence, or
      uncertainty claims; it states prescriptive rules.'
    fairness: 'NA: The document states rules rather than engaging opposing positions;
      there are no oppositional framings to balance.'
    robustness: 'NA: The document makes no interpretive judgments that could flip
      under an alternative lens; it defines a framework rather than interpreting evidence.'
  purpose:
    breadth: All 18 dimensions covered with rules; Common Pitfalls, Pre-Publish Self-Audit,
      Two-Pass Authoring, and Related Docs provide supporting material; all five groups
      addressed.
    depth: Rules are well-developed with examples and cross-references; some dimensions
      have thinner rule development (Coherence has 4 short rules while Organization
      has 8; Calibration and Robustness rules are somewhat abstract).
    scope: Scope stated as 'prescriptive rules for practical documents' and the 18-dimension
      boundary is explicit; however, out-of-scope material (creative writing, fiction,
      informal communication) is never named, and L88 uses the stale dimension name
      'Coverage' from the prior 15-dim-v1 rubric.
    suitability: Task clearly stated (prescriptive rules for practical documents);
      main output recoverable from section headings and dimension table; output shape
      matches task shape (numbered rules per dimension).
  reasoning:
    discipline: 'NA: The document states prescriptive rules, not inferential
      claims; it does not move from observation to judgment to interpretation to implication.
      The ladder-of-inference section describes the concept but does not itself make
      inferences.'
    parsimony: 'NA: the document states prescriptive rules, not inferential claims;
      no reasoning chains to test for minimality.'
    precision: Dimension names are precise and consistently used; L88 uses the obsolete
      term 'Coverage' where the current term is 'Breadth'.
    soundness: Rules are internally consistent and well-defined; mechanisms named
      where causation is implied; the alignment claim at L11-12 asserted rather than
      argued with a worked demonstration.
quant:
  bracket_tag_examples: []
  headings:
    h1: 1
    h2: 11
    h3: 19
    h4: 0
    h5: 0
    h6: 0
    total: 31
  links:
    autolink: 0
    bare_urls: 0
    external: 0
    inline: 0
    internal: 0
    reference: 0
    total: 0
  lint:
    banned_register_hits: 5
  provenance:
    bracket_tags: 0
    footnote_defs: 0
    footnote_refs: 0
  size:
    bytes_kb: 32.6
    lines: 680
    pages_275wpp: 17.7
    paragraphs: 161
    sentences: 289
    words: 4865
  structural:
    code_blocks: 0
    images: 0
    tables: 1
violations:
- description: Stale dimension name 'Coverage' from the prior 15-dim-v1 rubric used
    instead of current 'Breadth'
  dimension: Scope
  location: L88
  rule_number: 1
- description: Calibration rules (§16) and Robustness rules (§18) are more abstract
    and less developed with worked examples than Clarity (§5) or Discipline
    (§13)
  dimension: Depth
  location: §16 and §18
  rule_number: 1
- description: Five banned-register words (incontrovertibly, monumental, seismic,
    paradigm-shifting, structurally outmaneuvered) appear in prose; though used as
    illustrative examples, a lint pass fires on them
  dimension: Clarity
  location: L197-198
  rule_number: 4
- description: Common Pitfalls section introduces 'compliance pressure crowding out
    self-regulation' and 'anchoring on a source document' without setup from preceding
    rule sections
  dimension: Coherence
  location: L707-728
  rule_number: 4
- description: 'Scope Rule 2.4 and Breadth Rule 3.4 are near-verbatim duplicates:
    both state ''out-of-scope omissions are not breadth failures'' with the same elaboration'
  dimension: Concision
  location: L105-108 and L136-138
  rule_number: 2
- description: 35 internal § cross-references are not hyperlinked, forcing manual
    navigation in an 800-line document
  dimension: Organization
  location: Throughout
  rule_number: 7
- description: Contractions ('can't', 'don't', 'doesn't') mixed freely with formal
    equivalents ('cannot', 'does not') with no stated register convention
  dimension: Consistency
  location: L58, L64, L70, L88, L150, L212, L340
  rule_number: 5
- description: No YAML frontmatter despite the doc's own Rule 10.5 requiring 'required
    headers, metadata, and footers present' and the companion rubric having frontmatter
  dimension: Formatting
  location: L1 (document opening)
  rule_number: 5
- description: Argyris citation omits co-authors (Putnam, Smith), page numbers, and
    publisher; 'Action Science (1985)' is not specific enough to verify the exact
    passage
  dimension: Verifiability
  location: L485-486
  rule_number: 2
- description: L88 refers to 'Coverage' as though it is a current dimension name,
    but 18-dim-v1 replaced Coverage with Breadth and Depth; entity reference does
    not match current rubric
  dimension: Factuality
  location: L88
  rule_number: 3
- description: The alignment claim at L11-12 ('every scoring failure should map to
    a specific rule here') is load-bearing but asserted without a worked example or
    test case
  dimension: Soundness
  location: L11-12
  rule_number: 5
- description: L88 uses the obsolete umbrella term 'Coverage' where the current proper
    names are 'Breadth' and 'Depth'
  dimension: Precision
  location: L88
  rule_number: 2
- description: Bibliography section §Related at L1000 lists references some of which
    stretch toward adjacent topics without one-sentence purpose link.
  dimension: Relevance
  location: §Related
  rule_number: 5
---

# guidelines-self

**Source:** `docs/practical-prose-guidelines.md`  **Scope:** `memo`  **Overall mean (20 dims):** 4.13  **Rubric:** `20-dim-v1`  **Model:** `—`  **Eval date:** 2026-05-10

## Qualitative

| Group | Dimension | Score | Reason |
| --- | --- | ---: | --- |
| **Purpose** | Suitability | 5 | Task clearly stated (prescriptive rules for practical documents); main output recoverable from section headings and dimension table; output shape matches task shape (numbered rules per dimension). |
|  | Scope | 4 | Scope stated as 'prescriptive rules for practical documents' and the 18-dimension boundary is explicit; however, out-of-scope material (creative writing, fiction, informal communication) is never named, and L88 uses the stale dimension name 'Coverage' from the prior 15-dim-v1 rubric. |
|  | Breadth | 5 | All 18 dimensions covered with rules; Common Pitfalls, Pre-Publish Self-Audit, Two-Pass Authoring, and Related Docs provide supporting material; all five groups addressed. |
|  | Depth | 4 | Rules are well-developed with examples and cross-references; some dimensions have thinner rule development (Coherence has 4 short rules while Organization has 8; Calibration and Robustness rules are somewhat abstract). |
|  | **Mean** | **4.50** | |
| **Expression** | Clarity | 4 | Clear, concrete prose throughout; examples are well-chosen (error-rate ladder of inference example is excellent); five banned-register words appear at L197-198 but only as illustrative examples. |
|  | Coherence | 4 | Ideas progress logically from Purpose through Judgment; each dimension section has consistent structure; Common Pitfalls section introduces concepts like 'compliance pressure' without explicit setup from preceding rule sections. |
|  | Concision | 4 | Scope Rule 2.4 and Breadth Rule 3.4 are near-verbatim duplicates; Pre-Publish Self-Audit compresses rules into a checklist that adds organizational value but overlaps substantially with rule sections. |
|  | Organization | 4 | Logical heading hierarchy (h1 > h2 > h3); dimension table provides a useful overview; sections arranged by group in rubric order; internal cross-references use named § references but none are hyperlinked, making navigation harder in an 800-line doc. |
|  | Consistency | 4 | Contractions mixed with formal non-contractions without a stated policy: 'can't' and 'don't' alongside 'does not', 'cannot', 'should not'; otherwise consistent. |
|  | Formatting | 4 | Markdown renders correctly; tables valid; code spans and emphasis used consistently; no YAML frontmatter despite the doc's own Rule 10.5 requiring headers/metadata/footers. |
|  | **Mean** | **4.00** | |
| **Grounding** | Verifiability | 4 | Argyris citation at L485 names the work but omits co-authors (Putnam, Smith) and page numbers; alignment claim at L11-12 asserted without a worked example or test. |
|  | Factuality | 4 | Argyris adaptation honestly stated; alignment claim is design intent (low factuality risk); 'Coverage' at L88 is a stale name that no longer matches the rubric's terminology. |
|  | Relevance | 4 | Sources and rules bear on each dimension's scope; one or two cross-references stretch toward adjacent topics. |
|  | **Mean** | **4.00** | |
| **Reasoning** | Discipline | NA | NA: The document states prescriptive rules, not inferential claims; it does not move from observation to judgment to interpretation to implication. The ladder-of-inference section describes the concept but does not itself make inferences. |
|  | Soundness | 4 | Rules are internally consistent and well-defined; mechanisms named where causation is implied; the alignment claim at L11-12 asserted rather than argued with a worked demonstration. |
|  | Precision | 4 | Dimension names are precise and consistently used; L88 uses the obsolete term 'Coverage' where the current term is 'Breadth'. |
|  | Parsimony | NA | NA: the document states prescriptive rules, not inferential claims; no reasoning chains to test for minimality. |
|  | **Mean** | **4.00** | |
| **Judgment** | Calibration | NA | NA: The document makes no probability, forecast, confidence, or uncertainty claims; it states prescriptive rules. |
|  | Fairness | NA | NA: The document states rules rather than engaging opposing positions; there are no oppositional framings to balance. |
|  | Robustness | NA | NA: The document makes no interpretive judgments that could flip under an alternative lens; it defines a framework rather than interpreting evidence. |
|  | **Mean** | — | |
|  | **Overall mean (20 dims)** | **4.13** | |

## Violations

1. **Scope** (rule 1) — Stale dimension name 'Coverage' from the prior 15-dim-v1 rubric used instead of current 'Breadth' *Location:* L88.
2. **Depth** (rule 1) — Calibration rules (§16) and Robustness rules (§18) are more abstract and less developed with worked examples than Clarity (§5) or Discipline (§13) *Location:* §16 and §18.
3. **Clarity** (rule 4) — Five banned-register words (incontrovertibly, monumental, seismic, paradigm-shifting, structurally outmaneuvered) appear in prose; though used as illustrative examples, a lint pass fires on them *Location:* L197-198.
4. **Coherence** (rule 4) — Common Pitfalls section introduces 'compliance pressure crowding out self-regulation' and 'anchoring on a source document' without setup from preceding rule sections *Location:* L707-728.
5. **Concision** (rule 2) — Scope Rule 2.4 and Breadth Rule 3.4 are near-verbatim duplicates: both state 'out-of-scope omissions are not breadth failures' with the same elaboration *Location:* L105-108 and L136-138.
6. **Organization** (rule 7) — 35 internal § cross-references are not hyperlinked, forcing manual navigation in an 800-line document *Location:* Throughout.
7. **Consistency** (rule 5) — Contractions ('can't', 'don't', 'doesn't') mixed freely with formal equivalents ('cannot', 'does not') with no stated register convention *Location:* L58, L64, L70, L88, L150, L212, L340.
8. **Formatting** (rule 5) — No YAML frontmatter despite the doc's own Rule 10.5 requiring 'required headers, metadata, and footers present' and the companion rubric having frontmatter *Location:* L1 (document opening).
9. **Verifiability** (rule 2) — Argyris citation omits co-authors (Putnam, Smith), page numbers, and publisher; 'Action Science (1985)' is not specific enough to verify the exact passage *Location:* L485-486.
10. **Factuality** (rule 3) — L88 refers to 'Coverage' as though it is a current dimension name, but 18-dim-v1 replaced Coverage with Breadth and Depth; entity reference does not match current rubric *Location:* L88.
11. **Soundness** (rule 5) — The alignment claim at L11-12 ('every scoring failure should map to a specific rule here') is load-bearing but asserted without a worked example or test case *Location:* L11-12.
12. **Precision** (rule 2) — L88 uses the obsolete umbrella term 'Coverage' where the current proper names are 'Breadth' and 'Depth' *Location:* L88.

## Quantitative

| Section | Measure | Value |
| --- | --- | ---: |
| Size | Words | 4,865 |
|  | Sentences | 289 |
|  | Paragraphs | 161 |
|  | Lines | 680 |
|  | Pages (275 wpp) | 17.7 |
|  | Bytes (KB) | 32.6 |
| Headings | Total (h1/h2/h3/h4) | 31 (1/11/19/0) |
| Structural | Tables | 1 |
|  | Code blocks | 0 |
|  | Images | 0 |
| Links | Total | 0 |
|  | External | 0 |
|  | Internal | 0 |
|  | Bare URLs | 0 |
| Provenance | Bracket tags | 0 |
|  | Footnote refs | 0 |
|  | Footnote defs | 0 |
| Lint | Banned-register hits | 5 |
| Density | Words / sentence | 16.83 |
|  | Words / paragraph | 30.22 |
|  | Sentences / paragraph | 1.79 |
|  | Links / 1k words | 0.00 |
|  | Links / page | 0.00 |
|  | Tables / 1k words | 0.21 |
|  | Tables / page | 0.06 |
|  | Tags / 1k words | 0.00 |
|  | Tags / page | 0.00 |
| Structure (derived) | h4 share of headings | 0.00 |
