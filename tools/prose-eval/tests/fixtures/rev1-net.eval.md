---
artifact:
  label: rev1-net
  path: <external artifact not in this repo>
  scope_class: deep_research
derived:
  density:
    links_per_1k_words: 2.4448
    links_per_page: 0.6718
    sentences_per_paragraph: 2.3964
    tables_per_1k_words: 1.4104
    tables_per_page: 0.3876
    tags_per_1k_words: 0.0
    tags_per_page: 0.0
    words_per_paragraph: 47.9054
    words_per_sentence: 19.9906
  rubric_rollup:
    assessed_dimensions: 18
    expression_mean: 4.1667
    grounding_mean: 4.0
    judgment_mean: 3.6667
    na_dimensions: 0
    overall_mean: 4.1111
    purpose_mean: 4.5
    reasoning_mean: 4.0
  structure:
    h4_share_of_headings: 0.3571
metadata:
  eval_date: '2026-05-10'
  evaluator: subagent (Claude Opus 4.7)
  method: 18-dim-v1 re-baseline via parallel subagent
  notes: Re-scored 2026-05-11 under 18-dim-v1 as part of practical-prose v0.4 calibration
    set. Strong baseline overall (overall ~4.0-4.5); Robustness=3 reflects bear-case
    under-treatment. Replaces prior 15-dim-v1-stale-baseline.
  rubric_version: 18-dim-v1
  status: complete
qual:
  expression:
    clarity: 4
    coherence: 5
    concision: 4
    formatting: 4
    organization: 4
    style_consistency: 4
  grounding:
    factuality: 4
    verifiability: 4
  judgment:
    calibration: 4
    fairness: 4
    robustness: 3
  purpose:
    breadth: 4
    depth: 4
    scope: 5
    suitability: 5
  reasoning:
    inference_discipline: 4
    precision: 4
    soundness: 4
qual_reasons:
  expression:
    clarity: Clear, precise prose throughout; one banned-register phrase at §2.6 L983
      'thesis only crystallized'; otherwise strong.
    coherence: Seamless two-phase structure; each paragraph has one job; transitions
      bridge cleanly between Phase 1 fact-gathering and Phase 2 analysis; no backtracking.
    concision: Mostly tight; beat-magnitude series ($6.6M to $25.5M) appears in full
      at §1.3 and is referenced at §2.1, §2.2, §2.8 — redundant across four sections.
    formatting: Markdown renders correctly; tables well-formed; the §1.3 table footnote
      uses a bare asterisk rather than a proper footnote anchor.
    organization: Logical heading hierarchy; tables earn their shape; 26 internal
      links to data files; cross-references to data files name only the filename,
      not what the reader will find.
    style_consistency: Consistent American English, consistent bold conventions; date
      formats mix ISO (2024-08-01) with abbreviated month (Aug 2026) within the same
      sections.
  grounding:
    factuality: Cannot fully verify externally; citations look well-formed; 'Multiple'
      as source for $12.8B AI coding market at §1.8 is not a verifiable citation;
      Anthropic '$4B Amazon investment' is a rounded aggregate without disclosure.
    verifiability: Most quantitative claims cite specific sources (earnings releases,
      10-Qs); Vercel CEO benchmark at §1.7 has no post ID or URL; CF '20% of the web'
      at §1.8 has no source URL.
  judgment:
    calibration: Scenario probabilities sum to 100% (30/50/20); bull probability marked
      'subjective'; but the 30/50/20 split is not anchored in any empirical base rate
      for SaaS earnings outcomes.
    fairness: Bull/base/bear cases present with numerical thresholds; bear case at
      §2.7 receives one row vs bull's fuller development; risk inventory spans macro,
      competitive, execution, capital structure.
    robustness: The 'all narrative, little attribution' bear lens at §2.7 is named
      but not run at depth comparable to the bull case; alternative interpretation
      (DBNRR recovery driven by pool-of-funds deal timing, not AI adoption) is not
      tested.
  purpose:
    breadth: All major case classes covered (financials, product, competitive, AI
      positioning, risk); §1.5d Application Services changelog deferred without full
      standalone treatment, a minor gap within declared scope.
    depth: Key sections (§2.7 AI thesis, §2.8 pre-earnings, §1.3 financials) deeply
      developed with full series and named instances; AI revenue estimate 5-15% lacks
      development of the triangulation inputs.
    scope: Scope explicitly declared with included/excluded lists; body matches throughout;
      out-of-scope items (pre-2024, DCF, investment advice) named.
    suitability: Task clearly stated in Overview; output shape matches (research brief
      with scenario tree, recommendations, workplan); main answer recoverable from
      section headings and §2.9 exec summary.
  reasoning:
    inference_discipline: Rungs generally well-separated; Phase 1 observation vs Phase
      2 interpretation cleanly structured; one fusion at §2.6 L982-983 where 'GitHub
      data was a leading indicator' blends observation with interpretation.
    precision: Domain entities named precisely (specific product names, versioned
      models, filing dates); 'Multiple' and 'Reported' as source attributions at §1.8
      are imprecise where specific publication names exist.
    soundness: Mechanisms named for key claims (DBNRR-to-growth, GM compression from
      GPU inference); the 5-15% AI-revenue estimate at §2.7 is stated as 'triangulated'
      but the method is not shown.
quant:
  bracket_tag_examples: []
  headings:
    h1: 1
    h2: 9
    h3: 26
    h4: 20
    h5: 0
    h6: 0
    total: 56
  links:
    autolink: 0
    bare_urls: 0
    external: 0
    inline: 26
    internal: 26
    reference: 0
    total: 26
  lint:
    banned_register_hits: 0
  provenance:
    bracket_tags: 0
    footnote_defs: 0
    footnote_refs: 0
  size:
    bytes_kb: 71.6
    lines: 1319
    pages_275wpp: 38.7
    paragraphs: 222
    sentences: 532
    words: 10635
  structural:
    code_blocks: 1
    images: 0
    tables: 15
violations:
- description: §1.5d Application Services changelog deferred at P3 without standalone
    treatment; WAF/DDoS/CDN feature releases only partially captured
  dimension: Breadth
  location: §1.5d
  rule_number: 3
- description: AI revenue triangulated estimate 5-15% stated without showing the inputs
    or method, leaving a key claim thin relative to its importance
  dimension: Depth
  location: §2.7 L1062
  rule_number: 1
- description: Banned-register-adjacent phrasing 'thesis only crystallized' uses extravagant
    register for what is simply 'was first articulated'
  dimension: Clarity
  location: §2.6 L983
  rule_number: 4
- description: Beat-magnitude series ($6.6M to $25.5M) duplicated across §1.3, §2.1,
    §2.2, and §2.8
  dimension: Concision
  location: §1.3 L262, §2.1 L835, §2.2 L878, §2.8 L1109
  rule_number: 2
- description: Cross-references to data files name only the filename, not what the
    reader will find
  dimension: Organization
  location: §1.7 L651
  rule_number: 7
- description: Date formats mix ISO (2024-08-01) with abbreviated month (Aug 2026,
    Feb 2026) within the same sections
  dimension: Style Consistency
  location: §1.2, §2.3
  rule_number: 1
- description: Table footnote at §1.3 uses bare asterisk rather than a proper footnote
    anchor that round-trips
  dimension: Formatting
  location: L576
  rule_number: 2
- description: Vercel CEO Rauch benchmark claim and X quote at §1.7 has no post ID
    or URL; CF '20% of the web' at §1.8 has no source URL
  dimension: Verifiability
  location: §1.7 L668-672, §1.8 L785
  rule_number: 2
- description: '''Multiple'' as source for $12.8B AI coding assistant market size
    is not a verifiable citation'
  dimension: Factuality
  location: §1.8 L710
  rule_number: 1
- description: Anthropic '$4B Amazon investment' is a rounded aggregate across multiple
    tranches without disclosure of rounding or aggregation
  dimension: Factuality
  location: §2.7 L1050
  rule_number: 2
- description: Observation (commit cadence preceded earnings narrative) and interpretation
    (leading indicator status) fused in one sentence
  dimension: Inference Discipline
  location: §2.6 L982-983
  rule_number: 2
- description: 5-15% AI-revenue estimate asserted as 'triangulated' without showing
    the triangulation method or contributing data points
  dimension: Soundness
  location: §2.7 L1062
  rule_number: 5
- description: '''Multiple'' and ''Reported'' used as source attributions where specific
    publication names exist'
  dimension: Precision
  location: §1.8 L710, L704
  rule_number: 2
- description: 30/50/20 scenario probabilities not anchored in empirical base rates
    for SaaS earnings outcomes
  dimension: Calibration
  location: §2.8 L1163-1170
  rule_number: 1
- description: Bear case receives one table row at §2.7 while bull case is developed
    across multiple paragraphs with named mechanisms; asymmetry not declared
  dimension: Fairness
  location: §2.7 L1072-1078
  rule_number: 1
- description: Bear-case 'all narrative' lens named but not tested at depth comparable
    to the bull case
  dimension: Robustness
  location: §2.7 L1078, §2.9 L1228
  rule_number: 2
- description: Interpretive lens for DBNRR-AI correlation (§2.9 finding 3) not stated
    explicitly; coincidence-vs-causation frame asserted without naming the lens
  dimension: Robustness
  location: §2.9 L1206-1209
  rule_number: 1
---

# rev1-net

**Source:** `<external artifact not in this repo>`  **Scope:** `deep_research`  **Overall mean (18 dims):** 4.11  **Rubric:** `18-dim-v1`  **Model:** `—`  **Eval date:** 2026-05-10

## Qualitative

| Group | Dimension | Score | Reason |
| --- | --- | ---: | --- |
| Purpose | Suitability | 5 | Task clearly stated in Overview; output shape matches (research brief with scenario tree, recommendations, workplan); main answer recoverable from section headings and §2.9 exec summary. |
| Purpose | Scope | 5 | Scope explicitly declared with included/excluded lists; body matches throughout; out-of-scope items (pre-2024, DCF, investment advice) named. |
| Purpose | Breadth | 4 | All major case classes covered (financials, product, competitive, AI positioning, risk); §1.5d Application Services changelog deferred without full standalone treatment, a minor gap within declared scope. |
| Purpose | Depth | 4 | Key sections (§2.7 AI thesis, §2.8 pre-earnings, §1.3 financials) deeply developed with full series and named instances; AI revenue estimate 5-15% lacks development of the triangulation inputs. |
| **Purpose** | **Mean** | **4.50** | |
| Expression | Clarity | 4 | Clear, precise prose throughout; one banned-register phrase at §2.6 L983 'thesis only crystallized'; otherwise strong. |
| Expression | Coherence | 5 | Seamless two-phase structure; each paragraph has one job; transitions bridge cleanly between Phase 1 fact-gathering and Phase 2 analysis; no backtracking. |
| Expression | Concision | 4 | Mostly tight; beat-magnitude series ($6.6M to $25.5M) appears in full at §1.3 and is referenced at §2.1, §2.2, §2.8 — redundant across four sections. |
| Expression | Organization | 4 | Logical heading hierarchy; tables earn their shape; 26 internal links to data files; cross-references to data files name only the filename, not what the reader will find. |
| Expression | Style Consistency | 4 | Consistent American English, consistent bold conventions; date formats mix ISO (2024-08-01) with abbreviated month (Aug 2026) within the same sections. |
| Expression | Formatting | 4 | Markdown renders correctly; tables well-formed; the §1.3 table footnote uses a bare asterisk rather than a proper footnote anchor. |
| **Expression** | **Mean** | **4.17** | |
| Grounding | Verifiability | 4 | Most quantitative claims cite specific sources (earnings releases, 10-Qs); Vercel CEO benchmark at §1.7 has no post ID or URL; CF '20% of the web' at §1.8 has no source URL. |
| Grounding | Factuality | 4 | Cannot fully verify externally; citations look well-formed; 'Multiple' as source for $12.8B AI coding market at §1.8 is not a verifiable citation; Anthropic '$4B Amazon investment' is a rounded aggregate without disclosure. |
| **Grounding** | **Mean** | **4.00** | |
| Reasoning | Inference Discipline | 4 | Rungs generally well-separated; Phase 1 observation vs Phase 2 interpretation cleanly structured; one fusion at §2.6 L982-983 where 'GitHub data was a leading indicator' blends observation with interpretation. |
| Reasoning | Soundness | 4 | Mechanisms named for key claims (DBNRR-to-growth, GM compression from GPU inference); the 5-15% AI-revenue estimate at §2.7 is stated as 'triangulated' but the method is not shown. |
| Reasoning | Precision | 4 | Domain entities named precisely (specific product names, versioned models, filing dates); 'Multiple' and 'Reported' as source attributions at §1.8 are imprecise where specific publication names exist. |
| **Reasoning** | **Mean** | **4.00** | |
| Judgment | Calibration | 4 | Scenario probabilities sum to 100% (30/50/20); bull probability marked 'subjective'; but the 30/50/20 split is not anchored in any empirical base rate for SaaS earnings outcomes. |
| Judgment | Fairness | 4 | Bull/base/bear cases present with numerical thresholds; bear case at §2.7 receives one row vs bull's fuller development; risk inventory spans macro, competitive, execution, capital structure. |
| Judgment | Robustness | 3 | The 'all narrative, little attribution' bear lens at §2.7 is named but not run at depth comparable to the bull case; alternative interpretation (DBNRR recovery driven by pool-of-funds deal timing, not AI adoption) is not tested. |
| **Judgment** | **Mean** | **3.67** | |
| | **Overall mean (18 dims)** | **4.11** | |

## Violations

1. **Breadth** (rule 3) — §1.5d Application Services changelog deferred at P3 without standalone treatment; WAF/DDoS/CDN feature releases only partially captured *Location:* §1.5d.
2. **Depth** (rule 1) — AI revenue triangulated estimate 5-15% stated without showing the inputs or method, leaving a key claim thin relative to its importance *Location:* §2.7 L1062.
3. **Clarity** (rule 4) — Banned-register-adjacent phrasing 'thesis only crystallized' uses extravagant register for what is simply 'was first articulated' *Location:* §2.6 L983.
4. **Concision** (rule 2) — Beat-magnitude series ($6.6M to $25.5M) duplicated across §1.3, §2.1, §2.2, and §2.8 *Location:* §1.3 L262, §2.1 L835, §2.2 L878, §2.8 L1109.
5. **Organization** (rule 7) — Cross-references to data files name only the filename, not what the reader will find *Location:* §1.7 L651.
6. **Style Consistency** (rule 1) — Date formats mix ISO (2024-08-01) with abbreviated month (Aug 2026, Feb 2026) within the same sections *Location:* §1.2, §2.3.
7. **Formatting** (rule 2) — Table footnote at §1.3 uses bare asterisk rather than a proper footnote anchor that round-trips *Location:* L576.
8. **Verifiability** (rule 2) — Vercel CEO Rauch benchmark claim and X quote at §1.7 has no post ID or URL; CF '20% of the web' at §1.8 has no source URL *Location:* §1.7 L668-672, §1.8 L785.
9. **Factuality** (rule 1) — 'Multiple' as source for $12.8B AI coding assistant market size is not a verifiable citation *Location:* §1.8 L710.
10. **Factuality** (rule 2) — Anthropic '$4B Amazon investment' is a rounded aggregate across multiple tranches without disclosure of rounding or aggregation *Location:* §2.7 L1050.
11. **Inference Discipline** (rule 2) — Observation (commit cadence preceded earnings narrative) and interpretation (leading indicator status) fused in one sentence *Location:* §2.6 L982-983.
12. **Soundness** (rule 5) — 5-15% AI-revenue estimate asserted as 'triangulated' without showing the triangulation method or contributing data points *Location:* §2.7 L1062.
13. **Precision** (rule 2) — 'Multiple' and 'Reported' used as source attributions where specific publication names exist *Location:* §1.8 L710, L704.
14. **Calibration** (rule 1) — 30/50/20 scenario probabilities not anchored in empirical base rates for SaaS earnings outcomes *Location:* §2.8 L1163-1170.
15. **Fairness** (rule 1) — Bear case receives one table row at §2.7 while bull case is developed across multiple paragraphs with named mechanisms; asymmetry not declared *Location:* §2.7 L1072-1078.
16. **Robustness** (rule 2) — Bear-case 'all narrative' lens named but not tested at depth comparable to the bull case *Location:* §2.7 L1078, §2.9 L1228.
17. **Robustness** (rule 1) — Interpretive lens for DBNRR-AI correlation (§2.9 finding 3) not stated explicitly; coincidence-vs-causation frame asserted without naming the lens *Location:* §2.9 L1206-1209.

## Quantitative

| Section | Measure | Value |
| --- | --- | ---: |
| Size | Words | 10,635 |
|  | Sentences | 532 |
|  | Paragraphs | 222 |
|  | Lines | 1,319 |
|  | Pages (275 wpp) | 38.7 |
|  | Bytes (KB) | 71.6 |
| Headings | Total (h1/h2/h3/h4) | 56 (1/9/26/20) |
| Structural | Tables | 15 |
|  | Code blocks | 1 |
|  | Images | 0 |
| Links | Total | 26 |
|  | External | 0 |
|  | Internal | 26 |
|  | Bare URLs | 0 |
| Provenance | Bracket tags | 0 |
|  | Footnote refs | 0 |
|  | Footnote defs | 0 |
| Lint | Banned-register hits | 0 |
| Density | Words / sentence | 19.99 |
|  | Words / paragraph | 47.91 |
|  | Sentences / paragraph | 2.40 |
|  | Links / 1k words | 2.44 |
|  | Links / page | 0.67 |
|  | Tables / 1k words | 1.41 |
|  | Tables / page | 0.39 |
|  | Tags / 1k words | 0.00 |
|  | Tags / page | 0.00 |
| Structure (derived) | h4 share of headings | 0.36 |
