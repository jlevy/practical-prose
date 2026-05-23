---
artifact:
  label: rev2-net
  path: <external artifact not in this repo>
  scope_class: deep_research
derived:
  density:
    links_per_1k_words: 0.0
    links_per_page: 0.0
    sentences_per_paragraph: 2.4315
    tables_per_1k_words: 1.5129
    tables_per_page: 0.416
    tags_per_1k_words: 0.3922
    tags_per_page: 0.1079
    words_per_paragraph: 53.1131
    words_per_sentence: 21.8433
  rubric_rollup:
    assessed_dimensions: 20
    expression_mean: 3.0
    grounding_mean: 2.6667
    judgment_mean: 3.0
    na_dimensions: 0
    overall_mean: 3.1
    purpose_mean: 3.75
    reasoning_mean: 3.0
  structure:
    h4_share_of_headings: 0.3231
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
  method: 20-dim-v1 re-baseline via parallel subagent
  notes: Re-scored 2026-05-11 under 20-dim-v1 as part of practical-prose v0.4 calibration
    set. Weaker baseline (overall ~3.0); pervasive register issues, citation gaps,
    and verbatim duplication. Replaces prior 15-dim-v1-stale-baseline.
  rubric_version: 20-dim-v1
  status: complete
qual:
  expression:
    clarity: 3
    coherence: 3
    concision: 3
    formatting: 3
    organization: 3
    consistency: 3
  grounding:
    factuality: 3
    relevance: 3
    verifiability: 2
  judgment:
    calibration: 3
    fairness: 3
    robustness: 3
  purpose:
    breadth: 4
    depth: 3
    scope: 4
    suitability: 4
  reasoning:
    discipline: 3
    parsimony: 3
    precision: 3
    soundness: 3
qual_reasons:
  expression:
    clarity: Generally readable prose but contains banned-register hits ('crystallized'
      at §2.1 and §2.8a), meta-commentary at L44-46 narrating document lineage, and
      parallel-structure padding.
    coherence: Ideas generally progress well within sections, but verbatim paragraph
      duplication at L1326-1342 is a literal backtrack; §2.7 restates §1.7 findings
      without advancing argument.
    concision: Beat-magnitude series ($6.6M to $25.5M) duplicated across five locations;
      §1.12 Macro [OPTIONAL] adds little beyond §2.10; frontmatter carries substantive
      framing claims.
    formatting: Markdown renders correctly; no broken fences or malformed frontmatter;
      however zero hyperlinks for any citation makes link-resolution vacuous.
    organization: Phase 1/Phase 2 structure logical, but several tables should be
      prose (§1.7, §2.9), Mermaid timeline at §1.4 lacks a caption, and zero cross-reference
      links in a 17.8K-word document.
    consistency: Register mostly holds but 'crystallized/crystallizes' is extravagant
      register inconsistent with the otherwise analytical tone; citation style varies
      between [VERIFIED via X] and bare prose-embedded references.
  grounding:
    factuality: Cannot externally verify sources; claims look well-formed and internally
      consistent, but Anthropic '$4B Amazon investment' is a simplified round number
      for a multi-tranche arrangement, and AI market-size figures cite 'Multiple'
      and 'AgentMarketCap' without URLs or dates.
    relevance: Several cited sources address adjacent topics; the load-bearing thesis
      would survive removing them.
    verifiability: Zero hyperlinks in a 17.8K-word deep-research document; [VERIFIED]
      tags used without filing dates or accession numbers; Vercel CEO benchmark claim
      has no tweet ID or URL.
  judgment:
    calibration: Scenario probabilities 30/50/20 sum to 100% but lack empirical base-rate
      anchors for SaaS earnings scenario distributions; Pass 1 updates lack explicit
      shrinkage or triangulation method.
    fairness: Bull/base/bear cases present with falsification conditions, but §2.12
      counterintuitive findings skew ~5 bull / 1 bear / 2 neutral with no explicit
      count; bear case receives less evidentiary depth than bull case.
    robustness: Base-to-bull lean named but the 'all narrative' bear lens at §2.8
      not run through the same evidence at comparable depth; DBNRR-AI correlation
      finding treats temporal alignment as the obvious reading.
  purpose:
    breadth: Five competitive vectors, eight quarters of financials, product families,
      risk register spanning five classes; gap is missing competitive depth on Akamai/Fastly
      CDN share data and limited SASE benchmarking.
    depth: Key sections like §2.1 quarterly deep-dives well-developed with full series,
      but vague magnitude words persist ('heavy hiring', 'materially', 'modest') and
      AI revenue triangulated estimate 5-15% lacks its method.
    scope: Scope explicitly declared with included/excluded sections, body largely
      matches; one minor drift with §1.12 Macro context tagged [OPTIONAL] but still
      included without scope-statement update.
    suitability: Task stated and output shape matches (research brief with scenario
      tree and recommendations), but central thesis answer and scenario tree buried
      in §2.8, not recoverable from a skim of intro + headings.
  reasoning:
    discipline: 'Several sentences blend observation and judgment in single
      clauses; most sections keep rungs distinct but blending recurs in §2.1 Q1 narrative
      and §2.12 finding #3.'
    parsimony: Multiple intermediate steps could be cut without weakening the conclusion;
      some chains are visibly padded.
    precision: '''Anthropic ($4B Amazon investment)'' uses a round umbrella figure;
      ''heavy hiring'' and ''materially'' used as vague placeholders in §1.9 and multiple
      §2.x sections.'
    soundness: AI-revenue triangulated estimate 5-15% stated without triangulation
      method; verbatim paragraph duplication is an internal-consistency failure; 'financial
      fingerprint of AI is in the gross margin' finding asserted without naming the
      mechanism.
quant:
  bracket_tag_examples:
  - DERIVED
  - OPTIONAL
  - UNVERIFIED
  - VERIFIED
  headings:
    h1: 1
    h2: 9
    h3: 34
    h4: 21
    h5: 0
    h6: 0
    total: 65
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
    bracket_tags: 7
    footnote_defs: 0
    footnote_refs: 0
  size:
    bytes_kb: 117.0
    lines: 2016
    pages_275wpp: 64.9
    paragraphs: 336
    sentences: 817
    words: 17846
  structural:
    code_blocks: 2
    images: 0
    tables: 27
violations:
- description: Central thesis answer and scenario tree buried in §2.8; not recoverable
    from a skim of intro + section headings
  dimension: Suitability
  location: Overview L29-47
  rule_number: 2
- description: §1.12 Macro context tagged [OPTIONAL] but included without flagging
    as mid-document scope expansion
  dimension: Scope
  location: §1.12, L1018-1043
  rule_number: 3
- description: Limited competitive benchmarking data for SASE segment; Akamai/Fastly
    CDN share decline asserted without sourced market-share series
  dimension: Breadth
  location: §1.10 Vector 4, L935-938
  rule_number: 2
- description: 'Vague magnitude words persist without quantification: ''heavy hiring'',
    ''materially'', ''modest'' across §1.9, §2.1, §2.2'
  dimension: Depth
  location: §1.9 L885; §2.1 L1154; §2.2 L1441
  rule_number: 3
- description: AI revenue triangulated estimate 5-15% is a key claim without its triangulation
    method shown
  dimension: Depth
  location: §2.8, L1685-1687
  rule_number: 1
- description: 'Banned-register hit: ''crystallized'' at §2.1 Q3''25 narrative and
    ''crystallizes'' at §2.8a crux table'
  dimension: Clarity
  location: §2.1 L1266; §2.8a L1694
  rule_number: 4
- description: 'Meta-commentary narrating the document''s lineage: ''this rev2 dry-run
    aims to exceed that depth'''
  dimension: Clarity
  location: Overview, L44-46
  rule_number: 3
- description: 'Parallel-structure padding: ''not a CDN/security provider but an essential
    control plane for autonomous AI agents'''
  dimension: Clarity
  location: §2.1 Q4'25, L1309-1310
  rule_number: 5
- description: Verbatim paragraph duplication at L1326-1342 creates a literal copy-paste
    backtrack
  dimension: Coherence
  location: §2.1, L1326-1342
  rule_number: 3
- description: §2.7 customer interpretation largely restates §1.7 findings without
    advancing a distinct analytical job
  dimension: Coherence
  location: §2.7, L1607-1634
  rule_number: 1
- description: Beat-magnitude series ($6.6M to $25.5M) duplicated across five sections
  dimension: Concision
  location: §1.3 L381; §2.0 L1062; §2.1 L1316; §2.2 L1387; §2.9 L1729
  rule_number: 2
- description: §1.12 Macro tagged [OPTIONAL] adds little marginal information beyond
    §2.10 risk register coverage
  dimension: Concision
  location: §1.12, L1018-1043
  rule_number: 1
- description: Frontmatter carries substantive claims (target_decision, event_anchor)
    that are prose framing, not machine-readable metadata
  dimension: Concision
  location: Frontmatter, L1-18
  rule_number: 4
- description: Mermaid timeline code block at §1.4 is a figure without a caption explaining
    what it shows
  dimension: Organization
  location: §1.4, L477-495
  rule_number: 4
- description: Zero hyperlinks in a 17.8K-word document; all citations prose-embedded
    with no stable anchor targets
  dimension: Organization
  location: Document-wide
  rule_number: 6
- description: Several tables have too few meaningful columns to earn tabular shape
    (§1.7 2-row mega-deal table, §2.9 positioning metrics 2-column table)
  dimension: Organization
  location: §1.7 L802-809; §2.9 L1749-1758
  rule_number: 3
- description: Register drifts between analytical and extravagant ('crystallized',
    'essential control plane') without consistent house-style enforcement
  dimension: Consistency
  location: §2.1 L1266; §2.1 L1309
  rule_number: 5
- description: 'Citation style inconsistent: some claims use [VERIFIED via X] bracket
    tags, others use bare prose references'
  dimension: Consistency
  location: §1.7 L820 vs §1.9 L898
  rule_number: 4
- description: Zero reference-style or inline links means the document's link layer
    is entirely absent
  dimension: Formatting
  location: Document-wide
  rule_number: 2
- description: Inconsistent blank-line spacing around the verbatim-duplicated paragraph
    block at L1326-1342
  dimension: Formatting
  location: §2.1, L1325-1343
  rule_number: 3
- description: Zero hyperlinks in a deep-research document; no quantitative claim
    verifiable via a link despite [VERIFIED] tags
  dimension: Verifiability
  location: Document-wide
  rule_number: 1
- description: '[VERIFIED via 10-K cover] at §1.1 L236 does not give filing date or
    accession number; pattern repeats at §1.5b L535, §1.6 L683'
  dimension: Verifiability
  location: §1.1 L236; §1.5b L535; §1.6 L683
  rule_number: 3
- description: Vercel CEO benchmark claim (1.2-5x faster) has no tweet ID or URL
  dimension: Verifiability
  location: §1.10, L911-914
  rule_number: 2
- description: Anthropic '$4B Amazon investment' at §2.8 is a simplified round number;
    actual investment is multi-tranche
  dimension: Factuality
  location: §2.8, L1669
  rule_number: 2
- description: AI market-size figures cite aggregator sources ('Multiple', 'AgentMarketCap')
    without URLs, dates, or verifiable identifiers
  dimension: Factuality
  location: §1.8 AI adoption table
  rule_number: 5
- description: '''GM at peak, op margin at through — typical Q1 seasonality with year-start
    S&M reset'' fuses observed values with interpretive judgment'
  dimension: Discipline
  location: §2.1 Q1 2024, L1107
  rule_number: 2
- description: '''DBNRR re-acceleration and the AI product GA timeline align too tightly
    to be coincidence'' blends observation with interpretation'
  dimension: Discipline
  location: '§2.12 finding #3, L1913-1920'
  rule_number: 2
- description: AI-revenue triangulated estimate 5-15% stated without showing the triangulation
    method or naming the data points
  dimension: Soundness
  location: §2.8, L1685-1687
  rule_number: 3
- description: Verbatim paragraph duplication at L1326-1342 is an internal-consistency
    failure
  dimension: Soundness
  location: §2.1, L1326-1342
  rule_number: 7
- description: '''Financial fingerprint of AI is in the gross margin'' asserted as
    finding without naming the mechanism distinguishing AI-mix-shift from R2/APAC
    effects'
  dimension: Soundness
  location: '§2.12 finding #2, L1904-1911'
  rule_number: 5
- description: '''Anthropic ($4B Amazon investment)'' uses round umbrella figure where
    multi-tranche sub-distinction matters'
  dimension: Precision
  location: §2.5, L1554
  rule_number: 2
- description: '''Heavy hiring'' and ''materially'' used as vague placeholders where
    counts or named specifics are available'
  dimension: Precision
  location: §1.9 L885; §2.1 L1154
  rule_number: 5
- description: Scenario probabilities 30/50/20 stated without empirical base-rate
    anchor for SaaS earnings scenario distributions
  dimension: Calibration
  location: §2.8 scenario tree, L1710-1712
  rule_number: 1
- description: AI-revenue triangulated estimate 5-15% given without showing the triangulation
    method or what data points contribute
  dimension: Calibration
  location: §2.8, L1348-1350
  rule_number: 3
- description: §2.12 counterintuitive findings skew ~5 bull / 1 bear / 2 neutral with
    no explicit count or confirmation-bias acknowledgement
  dimension: Fairness
  location: §2.12, L1889-1965
  rule_number: 4
- description: Bull case argued with three named primitives and numerical thresholds
    while bear case receives a single paragraph without comparable named mechanisms
  dimension: Fairness
  location: §2.8, L1651-1675
  rule_number: 1
- description: 'Base-to-bull lean not tested against most threatening alternative:
    ''all narrative'' bear lens named in §2.8 but not run at comparable depth'
  dimension: Robustness
  location: §2.8, L1706-1712
  rule_number: 2
- description: DBNRR-AI correlation finding treats temporal alignment as the obvious
    reading without naming alternative explanations (GTM rebuild, macro cycle)
  dimension: Robustness
  location: '§2.12 finding #3, L1913-1920'
  rule_number: 1
- description: Several cited sources address adjacent topics rather than the headline
    thesis.
  dimension: Relevance
  location: throughout
  rule_number: 1
- description: Multiple intermediate inferences could be cut without weakening the
    conclusion.
  dimension: Parsimony
  location: throughout
  rule_number: 2
---

# rev2-net

**Source:** `<external artifact not in this repo>`  **Scope:** `deep_research`  **Overall mean (20 dims):** 3.10  **Rubric:** `20-dim-v1`  **Model:** `—`  **Eval date:** 2026-05-10

## Qualitative

| Group | Dimension | Score | Reason |
| --- | --- | ---: | --- |
| **Purpose** | Suitability | 4 | Task stated and output shape matches (research brief with scenario tree and recommendations), but central thesis answer and scenario tree buried in §2.8, not recoverable from a skim of intro + headings. |
|  | Scope | 4 | Scope explicitly declared with included/excluded sections, body largely matches; one minor drift with §1.12 Macro context tagged [OPTIONAL] but still included without scope-statement update. |
|  | Breadth | 4 | Five competitive vectors, eight quarters of financials, product families, risk register spanning five classes; gap is missing competitive depth on Akamai/Fastly CDN share data and limited SASE benchmarking. |
|  | Depth | 3 | Key sections like §2.1 quarterly deep-dives well-developed with full series, but vague magnitude words persist ('heavy hiring', 'materially', 'modest') and AI revenue triangulated estimate 5-15% lacks its method. |
|  | **Mean** | **3.75** | |
| **Expression** | Clarity | 3 | Generally readable prose but contains banned-register hits ('crystallized' at §2.1 and §2.8a), meta-commentary at L44-46 narrating document lineage, and parallel-structure padding. |
|  | Coherence | 3 | Ideas generally progress well within sections, but verbatim paragraph duplication at L1326-1342 is a literal backtrack; §2.7 restates §1.7 findings without advancing argument. |
|  | Concision | 3 | Beat-magnitude series ($6.6M to $25.5M) duplicated across five locations; §1.12 Macro [OPTIONAL] adds little beyond §2.10; frontmatter carries substantive framing claims. |
|  | Organization | 3 | Phase 1/Phase 2 structure logical, but several tables should be prose (§1.7, §2.9), Mermaid timeline at §1.4 lacks a caption, and zero cross-reference links in a 17.8K-word document. |
|  | Consistency | 3 | Register mostly holds but 'crystallized/crystallizes' is extravagant register inconsistent with the otherwise analytical tone; citation style varies between [VERIFIED via X] and bare prose-embedded references. |
|  | Formatting | 3 | Markdown renders correctly; no broken fences or malformed frontmatter; however zero hyperlinks for any citation makes link-resolution vacuous. |
|  | **Mean** | **3.00** | |
| **Grounding** | Verifiability | 2 | Zero hyperlinks in a 17.8K-word deep-research document; [VERIFIED] tags used without filing dates or accession numbers; Vercel CEO benchmark claim has no tweet ID or URL. |
|  | Factuality | 3 | Cannot externally verify sources; claims look well-formed and internally consistent, but Anthropic '$4B Amazon investment' is a simplified round number for a multi-tranche arrangement, and AI market-size figures cite 'Multiple' and 'AgentMarketCap' without URLs or dates. |
|  | Relevance | 3 | Several cited sources address adjacent topics; the load-bearing thesis would survive removing them. |
|  | **Mean** | **2.67** | |
| **Reasoning** | Discipline | 3 | Several sentences blend observation and judgment in single clauses; most sections keep rungs distinct but blending recurs in §2.1 Q1 narrative and §2.12 finding #3. |
|  | Soundness | 3 | AI-revenue triangulated estimate 5-15% stated without triangulation method; verbatim paragraph duplication is an internal-consistency failure; 'financial fingerprint of AI is in the gross margin' finding asserted without naming the mechanism. |
|  | Precision | 3 | 'Anthropic ($4B Amazon investment)' uses a round umbrella figure; 'heavy hiring' and 'materially' used as vague placeholders in §1.9 and multiple §2.x sections. |
|  | Parsimony | 3 | Multiple intermediate steps could be cut without weakening the conclusion; some chains are visibly padded. |
|  | **Mean** | **3.00** | |
| **Judgment** | Calibration | 3 | Scenario probabilities 30/50/20 sum to 100% but lack empirical base-rate anchors for SaaS earnings scenario distributions; Pass 1 updates lack explicit shrinkage or triangulation method. |
|  | Fairness | 3 | Bull/base/bear cases present with falsification conditions, but §2.12 counterintuitive findings skew ~5 bull / 1 bear / 2 neutral with no explicit count; bear case receives less evidentiary depth than bull case. |
|  | Robustness | 3 | Base-to-bull lean named but the 'all narrative' bear lens at §2.8 not run through the same evidence at comparable depth; DBNRR-AI correlation finding treats temporal alignment as the obvious reading. |
|  | **Mean** | **3.00** | |
|  | **Overall mean (20 dims)** | **3.10** | |

## Violations

1. **Suitability** (rule 2) — Central thesis answer and scenario tree buried in §2.8; not recoverable from a skim of intro + section headings *Location:* Overview L29-47.
2. **Scope** (rule 3) — §1.12 Macro context tagged [OPTIONAL] but included without flagging as mid-document scope expansion *Location:* §1.12, L1018-1043.
3. **Breadth** (rule 2) — Limited competitive benchmarking data for SASE segment; Akamai/Fastly CDN share decline asserted without sourced market-share series *Location:* §1.10 Vector 4, L935-938.
4. **Depth** (rule 3) — Vague magnitude words persist without quantification: 'heavy hiring', 'materially', 'modest' across §1.9, §2.1, §2.2 *Location:* §1.9 L885; §2.1 L1154; §2.2 L1441.
5. **Depth** (rule 1) — AI revenue triangulated estimate 5-15% is a key claim without its triangulation method shown *Location:* §2.8, L1685-1687.
6. **Clarity** (rule 4) — Banned-register hit: 'crystallized' at §2.1 Q3'25 narrative and 'crystallizes' at §2.8a crux table *Location:* §2.1 L1266; §2.8a L1694.
7. **Clarity** (rule 3) — Meta-commentary narrating the document's lineage: 'this rev2 dry-run aims to exceed that depth' *Location:* Overview, L44-46.
8. **Clarity** (rule 5) — Parallel-structure padding: 'not a CDN/security provider but an essential control plane for autonomous AI agents' *Location:* §2.1 Q4'25, L1309-1310.
9. **Coherence** (rule 3) — Verbatim paragraph duplication at L1326-1342 creates a literal copy-paste backtrack *Location:* §2.1, L1326-1342.
10. **Coherence** (rule 1) — §2.7 customer interpretation largely restates §1.7 findings without advancing a distinct analytical job *Location:* §2.7, L1607-1634.
11. **Concision** (rule 2) — Beat-magnitude series ($6.6M to $25.5M) duplicated across five sections *Location:* §1.3 L381; §2.0 L1062; §2.1 L1316; §2.2 L1387; §2.9 L1729.
12. **Concision** (rule 1) — §1.12 Macro tagged [OPTIONAL] adds little marginal information beyond §2.10 risk register coverage *Location:* §1.12, L1018-1043.
13. **Concision** (rule 4) — Frontmatter carries substantive claims (target_decision, event_anchor) that are prose framing, not machine-readable metadata *Location:* Frontmatter, L1-18.
14. **Organization** (rule 4) — Mermaid timeline code block at §1.4 is a figure without a caption explaining what it shows *Location:* §1.4, L477-495.
15. **Organization** (rule 6) — Zero hyperlinks in a 17.8K-word document; all citations prose-embedded with no stable anchor targets *Location:* Document-wide.
16. **Organization** (rule 3) — Several tables have too few meaningful columns to earn tabular shape (§1.7 2-row mega-deal table, §2.9 positioning metrics 2-column table) *Location:* §1.7 L802-809; §2.9 L1749-1758.
17. **Consistency** (rule 5) — Register drifts between analytical and extravagant ('crystallized', 'essential control plane') without consistent house-style enforcement *Location:* §2.1 L1266; §2.1 L1309.
18. **Consistency** (rule 4) — Citation style inconsistent: some claims use [VERIFIED via X] bracket tags, others use bare prose references *Location:* §1.7 L820 vs §1.9 L898.
19. **Formatting** (rule 2) — Zero reference-style or inline links means the document's link layer is entirely absent *Location:* Document-wide.
20. **Formatting** (rule 3) — Inconsistent blank-line spacing around the verbatim-duplicated paragraph block at L1326-1342 *Location:* §2.1, L1325-1343.
21. **Verifiability** (rule 1) — Zero hyperlinks in a deep-research document; no quantitative claim verifiable via a link despite [VERIFIED] tags *Location:* Document-wide.
22. **Verifiability** (rule 3) — [VERIFIED via 10-K cover] at §1.1 L236 does not give filing date or accession number; pattern repeats at §1.5b L535, §1.6 L683 *Location:* §1.1 L236; §1.5b L535; §1.6 L683.
23. **Verifiability** (rule 2) — Vercel CEO benchmark claim (1.2-5x faster) has no tweet ID or URL *Location:* §1.10, L911-914.
24. **Factuality** (rule 2) — Anthropic '$4B Amazon investment' at §2.8 is a simplified round number; actual investment is multi-tranche *Location:* §2.8, L1669.
25. **Factuality** (rule 5) — AI market-size figures cite aggregator sources ('Multiple', 'AgentMarketCap') without URLs, dates, or verifiable identifiers *Location:* §1.8 AI adoption table.
26. **Discipline** (rule 2) — 'GM at peak, op margin at through — typical Q1 seasonality with year-start S&M reset' fuses observed values with interpretive judgment *Location:* §2.1 Q1 2024, L1107.
27. **Discipline** (rule 2) — 'DBNRR re-acceleration and the AI product GA timeline align too tightly to be coincidence' blends observation with interpretation *Location:* §2.12 finding #3, L1913-1920.
28. **Soundness** (rule 3) — AI-revenue triangulated estimate 5-15% stated without showing the triangulation method or naming the data points *Location:* §2.8, L1685-1687.
29. **Soundness** (rule 7) — Verbatim paragraph duplication at L1326-1342 is an internal-consistency failure *Location:* §2.1, L1326-1342.
30. **Soundness** (rule 5) — 'Financial fingerprint of AI is in the gross margin' asserted as finding without naming the mechanism distinguishing AI-mix-shift from R2/APAC effects *Location:* §2.12 finding #2, L1904-1911.
31. **Precision** (rule 2) — 'Anthropic ($4B Amazon investment)' uses round umbrella figure where multi-tranche sub-distinction matters *Location:* §2.5, L1554.
32. **Precision** (rule 5) — 'Heavy hiring' and 'materially' used as vague placeholders where counts or named specifics are available *Location:* §1.9 L885; §2.1 L1154.
33. **Calibration** (rule 1) — Scenario probabilities 30/50/20 stated without empirical base-rate anchor for SaaS earnings scenario distributions *Location:* §2.8 scenario tree, L1710-1712.
34. **Calibration** (rule 3) — AI-revenue triangulated estimate 5-15% given without showing the triangulation method or what data points contribute *Location:* §2.8, L1348-1350.
35. **Fairness** (rule 4) — §2.12 counterintuitive findings skew ~5 bull / 1 bear / 2 neutral with no explicit count or confirmation-bias acknowledgement *Location:* §2.12, L1889-1965.
36. **Fairness** (rule 1) — Bull case argued with three named primitives and numerical thresholds while bear case receives a single paragraph without comparable named mechanisms *Location:* §2.8, L1651-1675.
37. **Robustness** (rule 2) — Base-to-bull lean not tested against most threatening alternative: 'all narrative' bear lens named in §2.8 but not run at comparable depth *Location:* §2.8, L1706-1712.
38. **Robustness** (rule 1) — DBNRR-AI correlation finding treats temporal alignment as the obvious reading without naming alternative explanations (GTM rebuild, macro cycle) *Location:* §2.12 finding #3, L1913-1920.

## Quantitative

| Section | Measure | Value |
| --- | --- | ---: |
| Size | Words | 17,846 |
|  | Sentences | 817 |
|  | Paragraphs | 336 |
|  | Lines | 2,016 |
|  | Pages (275 wpp) | 64.9 |
|  | Bytes (KB) | 117.0 |
| Headings | Total (h1/h2/h3/h4) | 65 (1/9/34/21) |
| Structural | Tables | 27 |
|  | Code blocks | 2 |
|  | Images | 0 |
| Links | Total | 0 |
|  | External | 0 |
|  | Internal | 0 |
|  | Bare URLs | 0 |
| Provenance | Bracket tags | 7 |
|  | Footnote refs | 0 |
|  | Footnote defs | 0 |
| Lint | Banned-register hits | 2 |
| Density | Words / sentence | 21.84 |
|  | Words / paragraph | 53.11 |
|  | Sentences / paragraph | 2.43 |
|  | Links / 1k words | 0.00 |
|  | Links / page | 0.00 |
|  | Tables / 1k words | 1.51 |
|  | Tables / page | 0.42 |
|  | Tags / 1k words | 0.39 |
|  | Tags / page | 0.11 |
| Structure (derived) | h4 share of headings | 0.32 |
