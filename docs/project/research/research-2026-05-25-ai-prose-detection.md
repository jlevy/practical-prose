# Research: LLM-Distributional Analysis of Prose — Detection, Visualization, and Soft-Match Linting (2026)

**Date:** 2026-05-25 (last updated 2026-05-25)

**Author:** Joshua Levy (github.com/jlevy) with agent assistance

**Status:** Phase 1 complete; Phase 2 in progress

## Overview

The project’s broader question is: **how do you use the distributions captured by modern
LLMs as a measurement instrument for prose**, at varying levels of granularity (token,
word, phrase, sentence, paragraph), to support multiple analytical use cases?

AI-text detection is one application, and the question that motivated the initial
research pass. But the same measurement primitives — per-token log-probabilities,
cross-model disagreement, word-rarity overlays, soft-matched phrase patterns — support a
wider set of textual-analysis tasks:

- **AI register detection** (the original motivation): flag passages that look unedited
  LLM output.
- **Originality / novelty visualization**: show which spans of a human-written document
  are most *out of distribution* under one or more reference LLMs; use as an aid to
  writing or editing.
- **Stylistic and literary analysis**: locate the most distinctive passages in a text;
  compare authors by where they diverge from a baseline LLM.
- **ESL / writing pedagogy feedback**: surface vocabulary or syntactic patterns that are
  unusually high- or low-rarity compared to a reference corpus.
- **Comparative model fingerprinting**: see where two LLMs disagree on the same passage
  at the word / sentence level (fast-vs-advanced, base-vs-instruct,
  Claude-vs-GPT-vs-Gemini).
- **Phrase-pattern linting**: catch overused or hackneyed constructions with *soft*
  matching that goes beyond literal regex — the next step after proselint / Vale /
  Slopless.

The research is structured in two phases:

- **Phase 1 (complete):** Statistical / corpus studies, detection tools and watermarks,
  practitioner rule sheets, cliché linters, the math of log-prob detection, and the
  reader-side / detector reliability ceiling.
  See *Findings* and *Sub-Bead Deep-Dive Results* below.
- **Phase 2 (in progress):** Visualization and overlay tooling, multi-model comparison,
  word-rarity as a complementary axis, soft-matched phrase linting, and the UX patterns
  for composing multiple overlays on the same document.
  See *Phase 2: Visualization and Soft-Match Tooling* below.

The bibliography update target documents remain
[ai-prose-corrections.md](../../ai-prose-corrections.md) and
[practical-prose-bibliography.md](../../practical-prose-bibliography.md), with the Phase
2 work likely also feeding the pprose-eval renderer and a possible soft-match successor
to the corrections catalog.

## Questions to Answer

**Phase 1 (settled):**

1. What statistical / corpus studies published in late 2025 – mid 2026 advance the
   excess-vocabulary measurement work of Kobak, Juzek, and Liang?
2. What new detection tools, models, or watermarking systems have appeared since the
   bibliography last cited GLTR, Binoculars, Ghostbuster?
3. What practitioner rule sheets have appeared since the listed set (Lehmann, Pandya,
   Cook, Hassid, Orbach, ai-boost)?
4. Are there cliché / hackneyed-prose detectors (beyond AI-specific ones) that overlap
   with the AI-register problem, and has the “no Vale style pack” negative finding
   become out of date?
5. How do log-probability / perplexity / distributional-fit metrics work as detection
   signals, what do they actually measure, what are their known failure modes on
   current-generation models (Claude 4.x, GPT-5, Gemini 2.x), and what does that imply
   for the practical-prose project’s editorial vs.
   classifier approach?

**Phase 2 (in progress):**

6. What tools and methods support **per-token / per-word / per-sentence
   distributional-fit visualization** under one or more LLMs?
   At what granularities?
   With what pre-computation pipelines?
7. What tools and methods support **multi-model comparison overlays** — fast vs.
   advanced, base vs. instruct, vendor-to-vendor diff — at the word / sentence level?
8. What tools support **word and n-gram corpus-frequency / rarity overlays** as a
   *complementary* axis to LLM-likelihood (the two signals are not the same, and the
   difference is informative)?
9. What methods enable **soft / fuzzy / semantic phrase matching** for prose-style
   linting beyond regex — going past proselint / Vale / Slopless to embedding-based,
   fuzzy, or structural matching?
10. What existing **prose-visualization UIs compose multiple overlays** (e.g.,
    Hemingway, Voyant, LIWC, AcaWriter, WriteFull), and what UX patterns could
    pprose-eval adopt?

## Scope

**Included:**

- Peer-reviewed and preprint statistical / corpus studies, late 2025 – May 2026.
- Open-source and commercial detection tools / watermarking systems updated 2025–2026.
- Practitioner rule sheets and cliché / banlist linters that overlap with AI register.
- Mathematical and methodological background on log-prob-based detection.
- **Phase 2:** Tools and research for per-unit distributional-fit visualization at any
  granularity (token / word / phrase / sentence / paragraph), under one or multiple
  LLMs.
- **Phase 2:** Word-rarity and corpus-frequency overlays as a complementary analytical
  axis.
- **Phase 2:** Soft / fuzzy / semantic phrase-matching libraries and prose-linting
  frameworks (spaCy Matcher, sentence-transformers + FAISS, Aho-Corasick, rapidfuzz,
  AutoPhrase, semgrep-for-prose where it exists).
- **Phase 2:** Composable prose-visualization UIs from any tradition — digital
  humanities, stylometry, corpus linguistics, writing pedagogy, literary analysis — not
  only AI-detection UIs.

**Use cases the visualization layer is meant to support (broader than AI detection):**

- AI-register detection (original use case).
- Originality / novelty visualization for human-written work.
- Literary and stylistic analysis (where is the prose most distinctive?).
- ESL and writing-pedagogy feedback (vocabulary rarity, syntactic complexity).
- Cross-model comparison (where do two LLMs disagree?).
- Phrase-pattern linting that catches motifs regex cannot.

**Excluded:**

- General “is AI text good or bad” opinion pieces.
- Vendor marketing copy without methodology.
- Pre-2025 material unless directly load-bearing on a 2026 finding.
- Voice-matching for individual authors (still out of scope for the project).

## Findings

> The findings below come from an initial broad research pass on 2026-05-25. Each
> section flags items where a deeper sub-investigation has been opened as a bead under
> the epic (see *Methodology*).

### Statistical / corpus studies (new since the bibliography’s last refresh)

- **Galpin, Anderson & Juzek, “Exploring the Structure of AI-Induced Language Change in
  Scientific English”** (FLAIRS-38, June 2025). arXiv:2506.21817. Direct successor to
  *Why Does ChatGPT ‘Delve’ So Much?*. Moves beyond per-word frequency to
  **semantic-cluster shifts** (synonym groups rise together), POS-tagged forms
  (separates noun *potential* from adjective *potential*), and a previously
  under-reported phenomenon: the systematic **decline of common words like
  *important***. Implies LLM influence is pragmatic, not lexical-substitution.
  <https://arxiv.org/abs/2506.21817>
- **Anderson, Galpin & Juzek, “Model Misalignment and Language Change: Traces of
  AI-Associated Language in Unscripted Spoken English”** (AIES 2025). arXiv:2508.00238.
  22.1M-word science/tech podcast corpus, pre- vs.
  post-Nov 2022. First study to document **AI-marker vocabulary leaking into spontaneous
  human speech** while control synonyms stay flat — meaning the project’s tell catalog
  cannot assume a writer using *delve* drafted with an LLM.
  <https://arxiv.org/abs/2508.00238>
- **Geng & Trotta, “Human-LLM Coevolution: Evidence from Academic Writing”** (Feb 2025).
  arXiv:2502.09606. Empirical evidence for **active human counter-adaptation**: *delve*
  declines sharply once publicly named in early 2024, while *significant* keeps
  climbing. Adds a temporal-dynamics lens — tells decay once flagged.
  <https://arxiv.org/abs/2502.09606>
- **Kousha & Thelwall, “How much are LLMs changing the language of academic papers after
  ChatGPT? A multi-database and full-text analysis”** (Sept 2025, rev.
  Mar 2026). arXiv:2509.09596. First **full-text** rather than abstract-only Kobak-style
  analysis (2.4M+ PMC papers).
  Introduces **term co-occurrence as a tell**: in 2024 *underscore* correlates 0.449
  with *pivotal* and 0.311 with *delve*, vs.
  ~0.02 pre-ChatGPT. Implies cluster scoring beats per-word matching.
  <https://arxiv.org/abs/2509.09596>
- **Lin & Zhu, “Divergent LLM Adoption and Heterogeneous Convergence Paths in Research
  Writing”** (Apr 2025). arXiv:2504.13629. 627K+ arXiv papers; quantifies who adopts
  LLMs (junior, male, non-native English, early adopters) and reports a
  **stylistic-diversity collapse** as LLM use spreads.
  <https://arxiv.org/abs/2504.13629>
- **Liu et al., “AI-Assisted Writing Is Growing Fastest Among Non-English-Speaking and
  Less Established Scientists”** (Nov 2025). arXiv:2511.15872. Distributional-GPT
  framework on 2M+ PMC full-text papers.
  Quantifies ~400% growth in non-native contexts; sharpens the equity dimension of the
  *delve* literature and shows where false positives are most likely to hurt.
  <https://arxiv.org/abs/2511.15872>
- **Vansteenhuyse, “ChatGPT, is this real?
  The influence of generative AI on writing style in top-tier cybersecurity papers”**
  (Apr 2026). arXiv:2604.09316. NDSS, USENIX Security, IEEE S&P, ACM CCS, 2000–2025.
  Domain-specific replication outside biomed; adds **word-length distribution shift**
  and confirms *enhancing* alongside *delve* in security writing.
  <https://arxiv.org/abs/2604.09316>
- **Miletić & Falk, “What Are LLMs Doing to Scientific Communication?
  Measuring Changes in Writing Practices and Reading Experience”** (May 2026).
  arXiv:2605.19936. 37K+ ACL Anthology NLP papers + 20-reader pilot.
  Adds **reader-side measurement**: readers rate LLM-improved text “more understandable
  and exciting” but cannot reliably tell which version is AI. Names new syntactic tells
  (adverbial clauses, negation rates, proper-noun and punctuation-variation increases)
  and a lexical substitution table (*use* → *utilize*, *improve* → *enhance*).
  <https://arxiv.org/abs/2605.19936>
- **Rallapalli et al., “Interpretable Stylistic Variation in Human and LLM Writing
  Across Genres, Models, and Decoding Strategies”** (CMU, 2026). arXiv:2604.14111. 67
  Biber linguistic features across RAID’s 11 LLMs × 8 genres × 4 decoding strategies.
  Most thorough **syntactic** characterization to date.
  Top LLM-overused features: **nominalizations, that-clauses as subject, past
  participial clauses**. Empirical finding: model identity matters more than decoding
  strategy, and **genre overwhelms author-type** — a Kobak word list calibrated on
  biomed will mis-fire elsewhere.
  <https://arxiv.org/abs/2604.14111>
- **Bitton, Bitton & Nisan, “Detecting Stylistic Fingerprints of Large Language
  Models”** (Mar 2025). arXiv:2503.01659. LLM fingerprints distinguish **Claude vs.
  Gemini vs. Llama vs.
  OpenAI** at 99.88% precision (FPR 0.0004) and persist across prompt-induced style
  changes. Per-vendor tells exist below the level the practitioner sheets capture.
  <https://arxiv.org/abs/2503.01659>
- **Keck, “The Rise of the Em Dash in Ecology Abstracts”** (blog, 8 July 2025).
  OpenAlex-based; 10K ecology abstracts, 2021 vs.
  2025. First **quantitative** report that em-dash relative frequency more than doubled
  post-ChatGPT in a single discipline, with other punctuation flat — direct empirical
  support for the project’s em-dash policy.
  <https://www.pieceofk.fr/the-rise-of-the-em-dash-in-ecology-abstracts/>
- **Freeburg, “The Last Fingerprint: How Markdown Training Shapes LLM Prose”** (Mar
  2026). arXiv:2603.27006. Per-vendor em-dash rates per 1K words (unconstrained /
  plain-prose-constrained): GPT-4.1 10.62 / 9.10; Claude Opus 4.6 9.09 / 0.19; Gemini
  2.5 Pro 3.53 / 0.00; Llama 3.x 0.00 / 0.00; human baseline 3.23. Mechanism:
  markdown-as-formatting leaking when models cannot emit headers/bullets.
  Cites Altman’s public acknowledgment of a deliberate em-dash adjustment in ChatGPT.
  *Deep-dive bead open: confirm methodology and numbers before citing.*
  <https://arxiv.org/abs/2603.27006>
- **Ahmed & Hammond, “DependencyAI: Detecting AI Generated Text through Dependency
  Parsing”** (Feb 2026). arXiv:2602.15514. Pushes detection from lexical/perplexity
  features to **dependency-tree patterns** — evidence that grammatical-skeleton
  regularity is a real signal, complementing the Biber-features work.
  <https://arxiv.org/abs/2602.15514>

### Detection tools and models (new or updated)

- **RAID (Dugan et al., ACL 2024) and COLING 2025 Shared Task.** arXiv:2405.07940. 6M+
  generations across 11 models, 8 domains, 11 adversarial attacks, 4 decoding
  strategies. De-facto **benchmark substrate** behind nearly every 2025–2026 detector
  paper above. Reports that **Binoculars is the strongest open zero-shot detector at low
  FPR**; Pangram and Leidos top the shared task (99.3% clean, 97.7% adversarial).
  MIT-licensed.
- **Pangram Text Classifier — technical report v3.** Emi & Spero, arXiv:2402.14873v3
  (latest revision 2025). Documents the **hard-negative-mining with synthetic mirrors**
  training method; reports 99% accuracy across 10 text domains and 8 model families with
  claimed 1-in-10,000 FPR (independently checked at UChicago and Maryland).
  Closed-source commercial but the methods paper is public.
- **Fast-DetectGPT (Bao et al.).** arXiv:2310.05130, ICLR 2024. Drop-in zero-shot
  successor to DetectGPT (~75% better, dramatically cheaper).
  Standard free baseline in 2025–2026 papers.
- **SynthID-Text (Dathathri et al., *Nature* 634, 8035, 818–823, Oct 2024).** DOI
  10.1038/s41586-024-08025-4. Code Apache-2.0. First **production-scale text watermark**
  (deployed in Gemini).
  Tournament-Sampling algorithm.
  <https://github.com/google-deepmind/synthid-text>
- **Pasquini et al., “On Google’s SynthID-Text LLM Watermarking System”** (Mar 2026).
  arXiv:2603.03410. Proves SynthID’s mean-score is **vulnerable as tournament layers
  increase**; designs a working layer-inflation attack.
  First peer-style theoretical break.
- **SynGuard / robustness assessment** (Aug 2025). arXiv:2508.20228. Quantifies
  SynthID’s collapse under paraphrasing/back-translation (F1 1.0 clean → 0.884 under
  synonym attack).
- **DAMAGE: Detecting Adversarially Modified AI-Generated Text** (Jan 2025).
  arXiv:2501.03437. Best public account of how “humanizers” beat detectors and what
  residual signal survives.
- **Pudasaini et al., “Why AI-Generated Text Detection Fails”** (Mar 2026).
  arXiv:2603.23146. **Negative-result paper** using XAI to show benchmark accuracy hides
  distributional brittleness; detector features differ per source model.
  Useful corrective for vendor marketing copy.
- **Xia, Stańczak & Roth, “Explaining Generalization of AI-Generated Text Detectors
  Through Linguistic Analysis”** (EACL 2026). arXiv:2601.07974. Benchmarks 6 prompting
  strategies × 7 LLMs × 4 domains.
  Finds **passive-voice ratio and short-sentence ratio** are the most reliably
  cross-domain-generalizing features.

### Practitioner rule sheets (2026, beyond the listed set)

- **Wikipedia, “Wikipedia:Signs of AI writing”** (live community page; English Wikipedia
  banned undisclosed AI content additions in March 2026). Now the **largest
  community-maintained tell catalog**, with seven categories (content inflation,
  language patterns, style quirks, communication markers, markup problems, citation
  failures, tone shifts).
  Adds tells not in our existing set: **curly-vs-straight quote inconsistencies**,
  **title-case heading habit**, **excessive boldface**, **vertical lists with inline
  headers**, the **“Despite its [positive claims], faces challenges…” formula**, and
  “rule-of-three” listing habit.
  CC-BY-SA-4.0. *Deep-dive bead open.*
  <https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing>
- **Bouchard, “Stop Sounding Like ChatGPT: An Editor’s Cleanup System”** (Substack, 16
  Jan 2026). Editor-workflow framing (raw material → cleanup); ships an upstream prompt
  template intended to prevent slop rather than scrub it post-hoc.
  <https://louisbouchard.substack.com/p/how-to-edit-ai-writing-so-it-sounds>
- **Vollmer, “I Asked the Machine to Tell on Itself: A Field Guide to AI Tells”**
  (Substack). Writer-craft framing (literary, not marketing); enumerates tells in
  MFA-program register the engineering-flavored sheets miss.
  <https://matthewvollmer.substack.com/p/i-asked-the-machine-to-tell-on-itself>
- **Guo, “The Field Guide to AI Slop”** (*Ignorance.AI* Substack).
  Domain-spanning taxonomy (text, image, video, code “slop”); cross-modal vocabulary
  like “slop loop” and “slop-as-default.”
  <https://www.ignorance.ai/p/the-field-guide-to-ai-slop>
- **Hills & Illingworth, “AI Slop”** (*MarTech AI* Substack).
  Editor/marketer crossover; specific banned-construction list including **copula
  avoidance** (*serves as*, *stands as*, *marks a*), **false-range constructions**
  (*from X to Y, from A to B*), and **superficial -ing analyses**.
  <https://charliehills.substack.com/p/ai-slop>
- **Foote, “The Anti-AI Slop Skill”** (Substack, 2026). Packaged as a Claude skill
  (sibling to Pandya stop-slop).
  <https://biggerandbetter.substack.com/p/the-anti-ai-slop-skill>
- **Hassid, “It’s not [X], it’s [Y]”** (*How to AI* Substack).
  Follow-up to “Ban”; drills down on the self-negating-parallel construction with
  quantified cross-LLM frequency.
  <https://ruben.substack.com/p/its-not-x-its-y>

### Hackneyed-phrase / cliché detectors (and an update to the “no Vale pack” finding)

The bibliography’s “no Vale style pack” negative finding is **now partially out of
date**. A textlint-based pack now exists, plus a meta-index of related tools.
*Deep-dive bead open: verify Slopless’s rule coverage and maintenance.*

- **Slopless** (`agent-quality-controls/slopless`, MIT, v0.2.14 May 2026). 50+
  deterministic textlint rules across seven families: LLM vocabulary, generic
  signposting, prohibited AI-typical words and phrases, negation reframing, semantic
  thinness, Flesch-Kincaid scoring.
  Emits structured JSON findings.
  First publicly hosted, durably maintained rule pack explicitly targeting AI register.
  <https://github.com/agent-quality-controls/slopless>
- **avoid-slop** (`shannhk/avoid-slop`, MIT). Curated directory of open-source anti-slop
  tooling (humanizer, stop-slop, unslop, impeccable).
  <https://github.com/shannhk/avoid-slop>
- **anti-slop-writing** (`adenaufal/anti-slop-writing`). Universal system-prompt rule
  pack engineered to work across Claude Code, Codex, Cursor, Gemini CLI, Copilot;
  tool-agnostic counterpart to Orbach’s meta-prompt.
  <https://github.com/adenaufal/anti-slop-writing>
- **Word.Studio Cliché Finder.** Browser tool; baseline for plain-old-cliché matching.
  <https://word.studio/tool/cliche-finder/>
- **Readable buzzword/cliché module** (commercial; pairs with Hemingway and
  ProWritingAid as the bibliography already notes).
- **Lake Superior State University Banished Words List** (50th edition, 2026).
  Cultural-cliché list, not LLM-specific; longest-running banished-phrase tradition.
  <https://www.lssu.edu/resources/about-lssu/traditions/banishedwords/>

### Log-probability and distributional-fit metrics (new scope)

> This section is the explicit focus of one deep-dive sub-bead.
> The list below is a placeholder map; the bead will produce a methodological write-up
> covering the math, what each score actually measures, comparative reliability on
> Claude 4.x / GPT-5 / Gemini 2.x, and what the practical-prose project can and cannot
> reuse from these methods.

Initial map:

- **GLTR** (Strobelt et al., 2019). Visualizes per-token rank under a reference LM
  (originally GPT-2). The earliest distributional-fingerprint tool; primarily a teaching
  and visualization aid today.
- **DetectGPT** (Mitchell et al., ICML 2023). Curvature-based: under a small
  perturbation, machine-generated text shows a characteristic log-prob *drop* on the
  reference model that human text does not.
- **Fast-DetectGPT** (Bao et al., ICLR 2024). Replaces perturbation with conditional
  independence; faster and more accurate.
- **Binoculars** (Hans et al., ICML 2024). Scores the **ratio** of perplexity under one
  model to the cross-perplexity under a closely related model; robust because it cancels
  prompt-difficulty effects that confuse single-model perplexity.
- **Ghostbuster** (Verma et al., 2023). Trains a classifier on token-probability
  features passed through weaker LMs.
- **Pangram** (Emi & Spero, arXiv:2402.14873). Supervised classifier with hard-negative
  mining; commercial but methods public.
- **Distributional-GPT framework** (Liu et al., 2025, arXiv:2511.15872).
  Population-scale rather than per-document; estimates the LLM-mixture proportion in a
  corpus by fitting a distribution model.
- **Watermark detection** (SynthID-Text, Aaronson/OpenAI-style).
  Not strictly likelihood-based, but the same kind of probabilistic signal.

Questions for the bead: do any of these expose the specific tokens / phrases that drive
detection (and could those drive editor-style corrections), or are they purely
classification systems?

## Key Insights

- **The “delve” tell is decaying.** Geng & Trotta 2025 and Kousha & Thelwall 2025/26
  together show that *delve* is in measurable decline while less-flagged terms
  (*underscore*, *significant*) keep climbing.
  Practical implication: tell catalogs need a **first-flagged date** and a half-life
  expectation, not a static rule.
- **Em-dash is now empirically a vendor-specific fingerprint, not just an “AI tell.”**
  Freeburg (2026) gives clean per-model rates; Keck (2025) gives clean ecology data.
- **Tells cluster.** Kousha & Thelwall’s co-occurrence finding (*underscore* × *pivotal*
  r = 0.449) means single-word tells are far less informative than 2-of-N or 3-of-N
  tell-cluster rules. pprose-eval and the anti-slop linters should consider cluster
  scoring.
- **Detection generalization is feature-conditional.** Xia, Stańczak & Roth 2026 finds
  passive-voice ratio and short-sentence ratio are the closest to universal signals
  across LLMs. Implication: prefer **structural** rules (passives, sentence-length
  burstiness, that-clause-subjects) over **lexical** rules where you want longevity.
- **Marker words have leaked into speech.** Anderson, Galpin & Juzek 2025. Catalogs
  cannot assume a writer who uses *delve* drafted with an LLM; humans are now genuinely
  importing the register.
- **The “no Vale pack” negative finding is partially out of date.** Slopless exists and
  ships 50+ textlint rules.
  The bibliography note should be updated.

## Gaps and Uncertainty

- **Log-prob / distributional methods have not been rigorously surveyed against
  current-generation models** (Claude 4.x, GPT-5, Gemini 2.x) in a way the project can
  cite — this is the bead 1 deliverable.
- **No 2026 paper directly extends Kobak’s excess-vocabulary methodology to non-English
  corpora.** German/Spanish/French corpora exist in the Mosbach detection benchmark
  (arXiv:2312.04882) but as detection datasets, not excess-vocab measurements.
- **No public benchmark shows any 2026 detector reliably catching humanizer-laundered
  text from current-generation models.** Practical implication: the project’s editorial
  / rule-based approach is currently the more reliable route than classifier detection.
- **Most 2026 commercial-detector accuracy numbers come from self-reported vendor
  blogs.** Treat 99%+ claims with the skepticism Pudasaini 2026 documents.

## Methodology

Initial broad-pass research conducted 2026-05-25 via a single research agent run.
Specific deeper investigations are tracked as beads under an epic so progress can be
parallelized across sub-agents:

- **Epic:** `pp-ymjj` — Research: AI-prose detection and characterization (2026 update).
  Blocked until the five sub-beads complete.
- **Sub-beads** (one per area needing a deeper independent dive):
  1. `pp-ne5w` — Log-probability / distributional-fit detection methods.
     Math, what each score actually measures, robustness on current-generation models.
  2. `pp-zraz` — Slopless and the open-source AI-tell linting ecosystem.
     Verify rule coverage, license, maintenance; assess the “no Vale pack” gap.
  3. `pp-1by0` — Wikipedia *Signs of AI writing*. Extract tells not in
     ai-prose-corrections.md; note licensing and maintenance cadence.
  4. `pp-t496` — Freeburg “The Last Fingerprint” em-dash empirics.
     Confirm methodology and numbers before citing them as load-bearing for the em-dash
     policy.
  5. `pp-3vt3` — Reader-side perception and detector-reliability ceiling.
     Synthesize Miletić & Falk, Pudasaini, Pegoraro, DAMAGE into a single calibrated
     statement of what classifiers can and cannot do on current-generation models.

## Sub-Bead Deep-Dive Results

> Each subsection below is the condensed output of one sub-bead.
> Full source reports are in the tbd close-reason for the corresponding bead.

### pp-zraz — Slopless and the open-source AI-tell linting ecosystem

**Verified tool inventory (May 2026):**

- **Slopless** (`agent-quality-controls/slopless`). textlint, MIT, **v0.2.14 released 23
  May 2026**. SLSA v1 provenance attestations since v0.2.13. 50+ deterministic rules
  across seven families: generic signposting, prohibited phrases, LLM vocabulary,
  prohibited words, negation reframe, Flesch-Kincaid readability, semantic thinness.
  Emits structured JSON. Never calls an LLM. 352 stars, active CI, pre-commit hooks,
  signed releases.
- **textlint-rule-preset-ai-writing** (`textlint-ja/textlint-rule-preset-ai-writing`).
  textlint preset, npm `@textlint-ja/textlint-rule-preset-ai-writing`, MIT, v1.7.0 (May
  2026). 5 rules; **Japanese-language target** but ships an MCP server for live AI-tool
  feedback loops.
- **unslop** (`MohamedAbdallah-14/unslop`). Hybrid regex + optional LLM, v0.6.2 (Apr
  2026), MIT. 20+ pattern groups; ships across six agent surfaces.
- **anti-slop-writing** (`adenaufal/anti-slop-writing`). System-prompt / skill pack,
  MIT, v2.1.0 (Apr 2026). Six agent surfaces (Claude Code, Codex, Cursor, Gemini CLI,
  Copilot, ChatGPT); English + Indonesian.
- **avoid-slop** (`shannhk/avoid-slop`). Curated meta-index of the ecosystem.
- **sloplint** (`dannote/sloplint`). ast-grep over real syntax trees; targets
  AI-generated *code* slop, not prose.
  Listed only to disambiguate from Slopless.

**Vale / proselint status answer:** **No dedicated Vale style pack and no proselint
module for AI tells exists as of May 2026.** Confirmed via the Vale official package
registry, GitHub topic searches (`anti-slop`, `anti-ai-slop`, `ai-slop`,
`slop-detector`, `ai-slop-detection`), and direct searches for `vale ai tells`,
`vale slop`, `vale llm register`.

**Implication for the bibliography:** the *no Vale pack* negative finding is correct on
Vale and proselint but stale on the broader linting ecosystem, which now contains two
confirmed textlint packs (Slopless for English, preset-ai-writing for Japanese) plus the
broader anti-slop tool family.
Drafted drop-in replacement wording for lines ~564–567 of the bibliography is held in
the sub-bead’s close-reason; the *Tools* section needs two new entries (Slopless and the
Japanese preset).

**Recommendation:** the project should ship a textlint or Vale pack derived from
`ai-prose-corrections.md`, with rule IDs that match anchor IDs in the corrections doc
(the rule-ID contract is what keeps lint and prose from drifting).
Lower-cost interim: publish `ai-prose-corrections.md` as a portable agent skill the way
`anti-slop-writing` does.

### pp-1by0 — Wikipedia *Signs of AI writing* as a tell catalog

**Page metadata.** Status: **advice page maintained by WikiProject AI Cleanup**, not a
guideline or policy.
The page itself says: “This is not a Wikipedia policy, as it has not been reviewed by
the community.” License: CC-BY-SA-4.0.

**March 2026 policy context (separate page).** What was upgraded is **Wikipedia:Writing
articles with large language models** (WP:LLM). The RfC closed **~20 March 2026 under
SNOW, 44–2**. Operative language: “the use of LLMs to generate or rewrite article
content is prohibited,” with two narrow exceptions (suggesting copyedits to one’s own
writing after human review; first-pass translation).
**The policy explicitly states that stylistic or linguistic characteristics alone do not
justify sanctions**, which mirrors the *flag, not removal* posture of
ai-prose-corrections.md.
The narrowest deletion criterion is **WP:G15** ("LLM-generated content without human
review"), which the *Signs of AI writing* page is calibrated to support.

**Page structure.** Eight top-level sections: Content, Language and Grammar, Style,
Markup, Citations, Communication Intended for the User, Indicators of AI-Written
Comments, Miscellaneous.
The page also tracks an **era taxonomy** (*delve / tapestry* era → *align with /
showcasing* era → mid-2025+ attribution-language era) — implicit acknowledgment that any
tell list decays.

**15 tells not in the current ai-prose-corrections.md catalog**, organized into five
candidate new sections / additions:

1. **Significance and Notability Padding** (new section).
   *stands as a testament*, *serves as a reminder*, *plays a crucial / vital / pivotal
   role*, *marks a pivotal moment*, *leaves an indelible mark*, *symbolizes its enduring
   [X]*, *reflects broader [trends]*. Importance asserted without naming the specific
   contribution.
2. **Canned attribution** (new section item).
   *Industry reports suggest*, *Observers have noted*, *Experts argue*, *According to
   independent coverage*. Bare attribution without a named source.
3. **Trailing *-ing* analyses** (new section item).
   *… contributing to the broader movement*, *… highlighting the importance of*, *…
   underscoring its role in*. Participial codas that gesture at causation without
   arguing it.
4. **Conclusion-section formula** (additions to Mechanical Transitions).
   *Despite its [X], it faces several challenges …*, *Looking ahead*, *Its legacy
   continues to influence …*.
5. **Syntactic Tells** (new section): copulative avoidance (*serves as* / *stands as* /
   *acts as* / *functions as* in place of plain *is*), forced rule-of-three lists,
   elegant variation (reaching for synonyms to avoid repetition).
6. **Vocabulary additions to the existing list:** *intricate / intricacies*, *tapestry*,
   *testament*, *pivotal*, *underscore*, *garner*, *meticulous(ly)*, *embolden*, *align
   with*, *showcase / showcasing*, *highlighting*.
7. **Format and Markup Tells** (new section): Title Case headings in a document
   otherwise using sentence case; mechanical bolded lead-ins on every bullet; mixed
   straight/curly quotes; **paste-artifact strings** (`contentReference`, `oaicite`,
   `oai_citation`) — diagnostic of unedited paste.
8. **Direct-Address Tells** (new section): knowledge-cutoff disclaimers (*As of my
   knowledge cutoff …*); collaborative-offer endings (*I’m happy to discuss further*,
   *Please let me know if you’d like me to …*).

**Caveats.** Wikipedia’s catalog is calibrated to encyclopedic third-person prose; some
tells misfire in other practical-prose genres (*serves as* is genuinely overused in
encyclopedias but is normal in API docs: *this endpoint serves as the canonical write
path*). The genre carve-out principle in F2.6 / the existing file’s *Exception* notes is
the right shape for adoption.

**Cross-check.** Our existing *Engagement Bait* section covers ground the Wikipedia page
does not (the Twitter / Substack / Medium *Here’s why X matters* register).
The two catalogs are complementary, not redundant.

### pp-t496 — Freeburg “The Last Fingerprint” em-dash empirics verification

**Paper verification.** arXiv:2603.27006 confirmed real (arXiv API `id_list=2603.27006`
returns `totalResults=1`; control bogus ID `2603.99999` returns 0). Author: **E. M.
Freeburg, Independent Researcher**. Submitted **2026-03-27**, cs.CL primary, CC-BY-4.0.
Code and data at
[github.com/emfreeburg/the-last-fingerprint](https://github.com/emfreeburg/the-last-fingerprint).
14 pages, 3 tables.

**Per-vendor table confirmed verbatim** (em dashes per 1K words, unconstrained /
markdown-suppressed):

| Model | Unconstrained | Suppressed |
| --- | --- | --- |
| GPT-4.1 (OpenAI) | 10.62 | 9.10 |
| Claude Opus 4.6 (Anthropic) | 9.09 | 0.19 |
| Gemini 2.5 Pro (Google) | 3.53 | 0.00 |
| Llama 3.1 8B Instruct (Meta) | 0.00 | 0.00 |
| Llama 3.3 70B Instruct (Meta) | 0.00 | 0.00 |
| Human baseline | 3.23 (mean) | — |

**Mechanism confirmed verbatim:** the paper proposes em dash is *markdown leaking into
prose — the smallest surviving unit of the structural orientation that LLMs acquire from
markdown-saturated training corpora.* Suppression prompt used: *“Write in flowing prose
paragraphs only. Do not use any markdown formatting, headers, bullet points, bold text,
or lists.”* A base-vs-instruct comparison on Llama 3.1 8B is cited as evidence the
latent tendency is pre-RLHF.

**⚠ Critical caveat on the Altman citation.** The paper cites a 2024 “@sama” post and
frames it as Altman acknowledging *em-dash frequency was deliberately tuned upward in
ChatGPT*. The only Altman em-dash statement verifiable in public sources is the **14
November 2025** @sama tweet *“Small-but-happy win: if you tell ChatGPT not to use
em-dashes in your custom instructions, it finally does what it’s supposed to do!”*
(TechCrunch coverage same date).
This is about ChatGPT now *respecting suppression instructions*, not about a deliberate
upward adjustment. The paper’s “deliberately tuned upward” framing does not match this
tweet and the dates (2024 vs.
2025) do not match. **The bibliography should source the @sama 2025-11-14 tweet directly
rather than relaying the paper’s gloss.**

**Other caveats** (from the paper’s own *Limitations* section):

- Treat Llama 0.00 as a fine-tuning signature, **not** as evidence that base models lack
  em-dash tendency — the paper itself makes this distinction.
- Numbers are single-run measurements at the sample sizes reported; the paper flags
  prompt sensitivity and sample size.
- The Claude 9.09 → 0.19 drop (47×) is the headline finding and is the most
  prompt-sensitive single number in the table; cite alongside the suppression-prompt
  text rather than as a context-free figure.

**Recommended bibliography wording** is held in the bead’s close-reason.

### pp-ne5w — Log-probability and distributional-fit detection methods

**Framing.** The “is this LLM text?”
detectors that do *not* require a separate classifier all measure one thing in different
guises: how well a passage sits in the high-likelihood basin of a reference language
model. The earliest tool (GLTR) read this off per-token ranks directly; DetectGPT
formalized it as local curvature of `log p`; Fast-DetectGPT replaced expensive
perturbation with a single forward pass; Binoculars normalized perplexity by a sibling
model’s *cross-perplexity* to defeat prompt-difficulty confounds.
Supervised classifiers (Ghostbuster, Pangram) sit on top, often using weaker-LM
probabilities as features.
A separate line, watermarking (SynthID-Text), looks like likelihood detection but
actually measures a pseudo-random tournament signature.

**Per-method summary.**

- **GLTR** (Strobelt, Gehrmann & Rush, ACL 2019). Per-token rank under an open reference
  LM (originally GPT-2), with top-10 / top-100 / top-1000 fraction overlays.
  No longer competitive as a standalone classifier (modern decoding is no longer peaky
  enough), but the underlying signal still underlies most later methods and is the most
  editorially actionable: tokens are highlighted by rank bucket.
  **Per-token salience: yes.**
- **DetectGPT** (Mitchell et al., ICML 2023, arXiv:2301.11305). Curvature:
  `d(x) = log p_θ(x) − E[log p_θ(x̃)]` over T5 mask-fill perturbations.
  At a model-sampled point, `log p_θ` is near a local max so neighbors are almost always
  less likely. 100 forward passes per document; superseded by Fast-DetectGPT.
- **Fast-DetectGPT** (Bao et al., ICLR 2024, arXiv:2310.05130). Replaces perturbation
  with the *sampling* distribution `q_φ` of a reference model.
  Under conditional independence across positions the moments are closed-form, so two
  forward passes suffice.
  ~340× faster than DetectGPT, +75% relative AUROC. Score decomposes additively per
  token. **Per-token salience: yes (additive).**
- **Binoculars** (Hans et al., ICML 2024, arXiv:2401.12070).
  `B(s) = log PPL_M1(s) / log X-PPL_{M1,M2}(s)` where M1 = observer (e.g. Falcon-7B), M2
  = performer (Falcon-7B-Instruct).
  The denominator captures baseline surprise that any LLM would have produced on the
  same prompt — the *capybara problem* fix.
  Currently the strongest open zero-shot detector on RAID at low FPR. **Per-token
  salience: yes (token-level ratios; under-documented in the paper but in the reference
  implementation).**
- **Ghostbuster** (Verma et al., ACL 2024). Logistic regression over arithmetic
  combinations of weaker-LM probability features.
  Black-box on the generator.
  Features are per-token internally but the trained classifier collapses them; **no
  native per-token explanation exposed.**
- **Pangram v3** (Emi & Spero, arXiv:2402.14873v3). Transformer classifier with
  hard-negative-mining via synthetic mirrors.
  Domain-weighted FPR 0.02% after HNM; recall > 97% at 1% FPR on GPT-4 Turbo; 99.76% on
  Claude 3 (July 2024). **AUROC on GPT-5, Claude 4.x, or Gemini 2.x not publicly
  reported as of v3.** No per-token salience.
- **Distributional / mixture-proportion estimation** (Liu et al., 2025,
  arXiv:2511.15872). Population-level only — models a corpus as `π·f_AI + (1−π)·f_human`
  and estimates π. Not a per-document detector; useful as a corpus-drift signal.
- **SynthID-Text** (Dathathri et al., *Nature* 2024). Watermark, not likelihood:
  tournament-sampling tilts the distribution by a pseudo-random `g`-function.
  Detection computes mean `g`-value across observed tokens.
  TPR ≈ 0.88 at 100+ tokens with 30 layers on Gemma-7B. **Pasquini et al.
  2026** (arXiv:2603.03410): layer-inflation attack misclassifies 87% of watermarked
  prompts as unwatermarked.
  **SynGuard** (arXiv:2508.20228): F1 collapses to 0.711 under Chinese back-translation,
  0.842 under DIPPER aggressive paraphrase.
  Per-token, but hash-keyed — not editorially meaningful.
- **Burstiness / Gini of `log p`.** Variance of token or sentence-level log-probs.
  Pangram itself argues perplexity and burstiness alone are no longer sufficient on
  current models, but as a *feature* alongside the editorial catalog it remains cheap
  and informative. **Per-token salience: yes.**

**Comparative table.**

| Method | Access required | Per-token salience | Clean AUROC (current-gen) | Paraphrase robustness |
| --- | --- | --- | --- | --- |
| GLTR | Open ref LM | Yes (visual) | Not a competitive classifier | Low |
| DetectGPT | White-box + T5 | Possible, noisy | 0.72–0.85 on GPT-4-class; not on GPT-5/Claude 4 | Low–med |
| Fast-DetectGPT | White-box / surrogate | Yes (additive) | 0.85–0.93 on GPT-4/ChatGPT; ≈0.43 under StealthRL | Low under RL |
| Binoculars | Two open LMs | Yes (ratio per tok) | 0.92–1.00 clean; 0.42 GPT-4 FNR; ≈0.43 under StealthRL | Low under RL |
| Ghostbuster | Black-box | Internal only | F1 ≈ 0.99 self; lower elsewhere | Med |
| Pangram v3 | Black-box | None | Recall > 97% @ 1% FPR GPT-4 Turbo; 99.76% Claude 3 | Not reported; degrades per RAID |
| Distributional / MPE | Corpus stats | None | Not per-doc | N/A |
| SynthID-Text | Provider integration | Per-tok hash-keyed | TPR ≈ 0.88 @ 100+ tokens | Low (Pasquini, SynGuard) |
| Burstiness / Gini | Open ref LM | Yes | Insufficient alone | Low |

**Honest 2026 bottom-line.** On medium-to-long unedited single-shot LLM output in
English, Binoculars + Fast-DetectGPT with a Llama-3-8B + instruct sibling give AUROC ≈
0.85–0.95 and TPR > 90% at FPR ≈ 1%. That is good enough to **flag a paragraph as
suspicious**, not to confidently accuse a human writer.
Three reasons it does not get better: (1) frontier models (Claude 4.x, GPT-5, Gemini
2.x) are not the scoring models you have white-box access to, so every method becomes a
proxy-perplexity under an open model; the proxy bounds the signal; (2) RLHF/DPO-trained
outputs have moved the high-likelihood basin closer to the human-likelihood basin; (3)
adversarial paraphrase (DIPPER, StealthRL, humanizers) and short-text regimes collapse
AUROC to near-random.

**Recommendation for the practical-prose project.** Do **not** ship a “this is AI”
classifier (Pangram is better than we can replicate; the user-facing claim is
contested).
Integrate a per-token *LLM-distributional-fit overlay* as an auxiliary signal
next to the existing editorial rule catalog.
Concrete, in order of effort:

1. **GLTR-style overlay** in pprose-eval output, computed under a single open reference
   LM (Llama-3.1-8B is the practical pick: small, English-strong, well-tokenized).
   Render the per-token rank bucket as a heatmap alongside the rubric scores.
   Editorial value: spans dominated by green/yellow are where the Expression and Form
   dimensions are most likely already capturing real issues.
2. **Token-level Binoculars as a secondary scalar.** Same reference LM + instruct
   sibling; expose `log PPL / log X-PPL` at the document level and per sentence.
   Treat sentence-level Binoculars as a continuous register-flatness signal, not yes/no.
3. **Burstiness / Gini of `log p` as a metric.** Falls out of step 1 for free;
   explicitly addresses the mechanical-transitions and overused-words tells the project
   already tracks.
4. **Do not integrate watermark detection.** Requires generator cooperation; editorially
   uninformative.
5. **Do not integrate DetectGPT itself.** Fast-DetectGPT strictly dominates on cost and
   accuracy.

Framing in pprose-eval should be explicit: these signals are **complementary forensic
overlays, not verdicts**. The editorial rule catalog remains the source of truth; the
log-prob overlay tells you where to look.

### pp-3vt3 — Reader-side perception and detector-reliability ceiling

**Reader-side ceiling (peer-reviewed).**

| Study | Population | Discrimination rate |
| --- | --- | --- |
| Clark et al. (ACL 2021), *“All That’s ‘Human’ Is Not Gold”* | Untrained, three domains | ~**50% — chance** |
| Same, with training interventions | Trained | **~55%**, not significant across domains |
| Jakesch, Hancock & Naaman (PNAS 2023), 4,600 participants | Across professional / dating / hospitality | Misleading heuristics; AI often *more human than human* |
| Casal & Kessler (2023), *Applied Linguistics* | 72 trained linguists / top-journal reviewers | **38.9% positive identification — below chance** |
| Miletić & Falk (2026), arXiv:2605.19936 | 20-expert pilot, 200 paired excerpts | Experts reported *difficulty*; on Wilcoxon tests **readers preferred LLM-edited text** on clarity (Cohen’s d = −0.38), excitement (d = −0.26), authenticity (d = −0.12) |

**Detector ceiling, clean current-generation text.**

Independent — RAID (Dugan et al., ACL 2024), accuracy at FPR = 5%:

- Originality **85.0%**
- Binoculars **79.6%**
- Fast-DetectGPT **73.6%**
- RADAR 70.9%
- GPTZero 66.5%
- GLTR 62.6%

Vendor self-report — Pangram v3:

- ~99% accuracy claimed; 100% recall at 1% FPR on GPT-4o; 99.76% on Claude 3.
- Not reproducible on independent benchmarks; Pangram’s own report *strongly
  discourages* using the classifier as a sole arbiter.
- **AUROC on Claude 4.x, GPT-5, or Gemini 2.x not publicly reported as of v3.**

Pegoraro et al.
(NAACL Findings 2025): on out-of-distribution model–domain pairs, **TPR @
FPR = 1% drops as low as 0%**.

**Detector ceiling, adversarial text.** Every independently-evaluated detector loses
30–75 points of TPR under cheap, off-the-shelf attacks:

| Attack | Detector | Clean | Attacked | Drop |
| --- | --- | --- | --- | --- |
| Homoglyph (RAID) | Originality | 85.0% | **9.3%** | −75.7 |
| Homoglyph | Binoculars | — | — | −41.9 |
| Homoglyph | GLTR | — | — | −38.3 |
| BERT synonym sub | Binoculars | — | — | −36.1 |
| Commercial humanizer (DAMAGE) | GPTZero | 99.73% | **60.04%** | −39.7 |
| Commercial humanizer | Binoculars | 94.15% | **28.23%** | −65.9 |

DAMAGE retrained on humanized samples recovers to 98.26% — a *calibration* result, not
evidence any deployed detector is robust.

**Why detectors fail (Pudasaini et al.
2026, arXiv:2603.23146, SHAP analysis).** In-domain: F1 = 0.9734 reachable with
engineered features.
Out-of-domain: *“the most influential features differ markedly between datasets,
indicating that detectors often rely on dataset-specific stylistic cues rather than
stable signals of machine authorship.”* The features most discriminative in-distribution
are precisely the features most susceptible to domain shift, formatting variation, and
text-length effects.
Pangram’s own blog acknowledges the ESL false-positive bias: **non-native English
speakers have systematically lower perplexity and burstiness**.

**What does hold up across domains (Xia, Stańczak & Roth, EACL 2026).** Abstract-level
verifiable claim: generalization is significantly associated with **tense usage and
pronoun frequency** shifts.
A PDF-extraction surfaces **passive constructions, sentence-length variance, and
subordinate-clause density** as additional structural transfer features — **verify
against the published text before quoting**. Miletić & Falk independently corroborate
the direction of these shifts (longer / more complex words; lower lexical diversity;
more negations and adverbial clauses; more commas; fewer brackets), with corpus-level
AUC = 0.65 — large enough to measure at population scale, weak per-document.

**Calibrated bottom line for the project.** On clean text from current-generation models
the best independent detector benchmark shows top detectors at 66–85% accuracy at FPR =
5% (Originality 85.0%, Binoculars 79.6%); vendor self-reports go higher but are not
reproducible.
On adversarially-modified text every independently-evaluated detector loses
30–75 points of TPR. Humans sit at 50% untrained, ~55% with training, and 38.9% even for
trained linguists on their own genre.

**Recommendation.** **Do not add classifier-style AI-vs-human scoring to pprose-eval.**
Three reasons:

1. The ceiling is materially below useful (RAID 66–85% clean, collapsing under cheap
   attacks; Pudasaini shows in-distribution validation overstates real performance).
2. The task is not what readers care about.
   Miletić & Falk show readers *prefer* LLM-edited prose on clarity and excitement while
   being unable to discriminate.
   The project’s job is reader-outcome quality, not authorship adjudication.
3. The vendor-claim ecosystem is hostile to defensible scoring (Pangram’s self-reported
   numbers do not reproduce on RAID; documented ESL false-positive bias).

**Defensible middle path** (matches the pp-ne5w recommendation): compute the
*structural* features Xia et al.
flag as cross-domain-robust — **passive-voice ratio, sentence-length variance /
burstiness, subordinate-clause density, lexical diversity / type-token ratio** — and
**surface them as descriptive metrics in the report, not as a verdict**. The metrics
describe what the prose looks like; the editorial rule catalog in
ai-prose-corrections.md judges whether it serves the reader; the agent does not pretend
to know who wrote it.

## Recommendations

The five deep-dive sub-beads converge on a single editorial line: **stay editorial;
surface forensic / structural metrics as context, not verdicts; update the bibliography
for the 2026 corpus.**

**For the bibliography
([practical-prose-bibliography.md](../../practical-prose-bibliography.md)):**

1. **Add a *Statistical and Corpus Studies* subsection update** to the *Critique of
   AI-Authored Prose* section, citing the strongest 2025–2026 work that extends Kobak /
   Juzek / Liang: Galpin, Anderson & Juzek 2025; Anderson, Galpin & Juzek 2025; Geng &
   Trotta 2025 (tell decay); Kousha & Thelwall 2025/26 (full-text + co-occurrence);
   Rallapalli et al. 2026 (Biber-features syntactic characterization); Miletić & Falk
   2026 (reader-side measurement); Bitton, Bitton & Nisan 2025 (per-vendor
   fingerprints); Keck 2025 + Freeburg 2026 (em-dash empirics; cite Freeburg with the
   qualifications from `pp-t496` close-reason).
2. **Add a *Log-probability detection methods* subsection** to the *Tools* section,
   citing DetectGPT, Fast-DetectGPT, Binoculars, Ghostbuster, Pangram v3 (with
   vendor-claim caveat), distributional / MPE (Liu et al.
   2025), and the SynthID-Text + Pasquini break + SynGuard chain.
3. **Update the *no Vale pack* negative finding** to acknowledge Slopless (textlint,
   MIT, May 2026, 50+ rules) and the Japanese `textlint-rule-preset-ai-writing` sibling;
   drop-in replacement paragraph is in the `pp-zraz` close-reason.
4. **Add a *Reliability ceiling* paragraph** anchoring the project’s editorial framing:
   cite RAID + DAMAGE + Pudasaini + Pegoraro for the adversarial collapse, and Clark /
   Jakesch / Casal & Kessler / Miletić & Falk for the human reader ceiling.

**For [ai-prose-corrections.md](../../ai-prose-corrections.md):**

5. **Tag each entry with a first-flagged date.** Geng & Trotta 2025 and Kousha &
   Thelwall 2025/26 establish that named tells decay; the catalog should distinguish
   2023-era *delve* from 2025-era *underscore* / *significant*.
6. **Add the 15 Wikipedia-derived tells from `pp-1by0`** as five new sections:
   *Significance and Notability Padding*, *Canned Attribution*, *Trailing -ing
   Analyses*, *Syntactic Tells* (copulative avoidance, rule-of-three, elegant
   variation), *Format and Markup Tells* (Title Case headings, bolded lead-ins,
   paste-artifact strings), and *Direct-Address Tells* (knowledge-cutoff disclaimers,
   collaborative-offer endings).
7. **Add structural / syntactic tells as a new section**, calibrated to what Xia /
   Rallapalli / Miletić show is durable across models: passive-voice rate,
   sentence-length variance, subordinate-clause density, nominalizations,
   adverbial-clause rate, lexical diversity.
   Treat these as **metrics** (numerical features) rather than as grep-flagged phrases.

**For pprose-eval (the tool):**

8. **Do not ship an AI-vs-human classifier verdict.** Pangram is better than we can
   reproduce; the underlying signal collapses under cheap attacks; the user-facing claim
   is contested. (`pp-ne5w` and `pp-3vt3` converge.)
9. **Optionally** add three forensic overlays as descriptive context next to the rubric
   scores: GLTR-style per-token rank heatmap under Llama-3.1-8B; sentence-level
   Binoculars (`log PPL / log X-PPL`) under Llama-3.1-8B + Instruct sibling; burstiness
   / Gini of token `log p`. Frame as **complementary forensic overlays, not verdicts**.
10. **Optionally** compute the structural metrics from step 7 as machine-checkable
    features and expose them in the report.

**For the em-dash policy in `feedback_em_dashes.md` (local agent memory note):**

11. Cite Keck 2025 and Freeburg 2026 (with the Altman-citation caveat from `pp-t496`) as
    empirical support; treat the cited per-vendor numbers with the suppression-prompt
    context attached.

## Next Steps

- [x] `pp-ne5w` Log-prob / distributional-fit detection methods deep dive.
- [x] `pp-zraz` Slopless and the open-source AI-tell linting ecosystem.
- [x] `pp-1by0` Wikipedia *Signs of AI writing* extraction.
- [x] `pp-t496` Freeburg em-dash empirics verification.
- [x] `pp-3vt3` Reader-side perception and detector-reliability ceiling.
- [x] Integrate sub-bead findings back into this document.
- [ ] Draft proposed edits to
  [practical-prose-bibliography.md](../../practical-prose-bibliography.md) and
  [ai-prose-corrections.md](../../ai-prose-corrections.md).
  *(Recommendations section above is the source; the actual file edits await user review
  of this doc.)*

## Phase 2: Visualization and Soft-Match Tooling

> Phase 2 reframes the project’s view of the same underlying primitives — LLM token
> probabilities, corpus frequencies, and pattern matching — as a *general
> textual-analysis toolkit*, of which AI-text detection is one application.
> The motivating use case is **a per-document overlay UI** that, for any given document,
> shows at a glance which words / phrases / sentences are most out of distribution under
> one or more reference LLMs, alongside complementary axes like word rarity and
> soft-matched phrase tells.
> Pre-computation is acceptable; the goal is the *visualization*, not classification
> latency.

### Use cases driving Phase 2

- **AI register detection** (carried over from Phase 1): flag passages that look
  unedited LLM output.
- **Originality / novelty visualization** for human-written work: spans *most out of
  distribution* are candidates for “most distinctive.”
- **Stylistic / literary analysis**: locate the most distinctive passages; compare
  authors against a baseline LLM.
- **ESL / pedagogy feedback**: vocabulary or syntactic patterns of unusually high or low
  rarity vs. a reference corpus.
- **Cross-model fingerprinting**: where do two models disagree on the same passage
  (fast-vs-advanced; base-vs-instruct; per-vendor).
- **Soft-matched phrase linting**: catch hackneyed constructions with fuzzy / semantic
  tolerance — the successor to grep-based Slopless / proselint / Vale.

### Phase 2 sub-beads

- **Epic:** `pp-4gnd` — Research: distributional-fit visualization and soft-match phrase
  linting for prose.
- **Sub-beads:**
  - `pp-dc53` — Per-token / per-word / per-sentence distributional-fit visualization
    tools and methods. GLTR + successors; Inseq; LIT; BertViz / AttentionViz; logit-lens;
    surprisal-based linguistic tools; academic visualization papers; pre-compute
    pipeline shape.
  - `pp-gcdj` — Multi-model comparison overlays.
    LMDiff; model-disagreement research; Binoculars’ cross-perplexity ratio as a
    per-token diff signal; logit-lens-diff; OpenAI / Anthropic playground tooling.
  - `pp-81yt` — Word and n-gram corpus-frequency / rarity overlays.
    wordfreq; Zipf; Google Books Ngram; COCA / SUBTLEX / OEC; TAALES; Coh-Metrix; CEFR /
    EVP vocabulary-difficulty tools; concordance UIs.
    Distinguishes corpus-frequency from LLM-likelihood.
  - `pp-84ya` — Soft / fuzzy / semantic phrase matching for prose-style linting beyond
    regex. spaCy Matcher / PhraseMatcher / DependencyMatcher; sentence-transformers +
    FAISS; AutoPhrase / ToPMine; Aho-Corasick; rapidfuzz; semgrep-style structural
    matching for prose if any.
  - `pp-xrqd` — Existing prose-visualization UIs that compose multiple overlays.
    Hemingway; ProWritingAid; Grammarly; Voyant; LIWC; AcaWriter; WriteFull; Stylo;
    AntConc / Sketch Engine; annotation tooling (BRAT / INCEpTION / Doccano).
    Goal: identify UX patterns the project could adopt.

### Phase 2 deep-dive results

> Sub-bead results will be folded in below as each agent completes.

#### pp-gcdj — Multi-model comparison overlays

**Headline:** no off-the-shelf tool produces the user’s exact ask — fixed document, two
arbitrary vendor LLMs (e.g. fast Sonnet vs.
advanced Opus, or Claude vs.
GPT-5 vs. Gemini), per-token color overlay.
The signal-side methods exist and are mature; the UI-side is universally greenfield.

**Direct multi-model comparison tools.**

- **LMDiff** (Strobelt et al., EMNLP 2021). Apache-2.0,
  [HendrikStrobelt/LMdiff](https://github.com/HendrikStrobelt/LMdiff), demo at
  [lmdiff.net](http://lmdiff.net).
  Token-level divergence overlay (KL, top-k overlap, rank shift) for any two HuggingFace
  causal/MLM models with **identical tokenizers**. Designed for base-vs-finetune or
  same-family size pairs; **not** for cross-vendor.
  The most direct conceptual match to the user’s ask, but the repo is dormant (~44
  stars, no releases, tied to older Transformers APIs).
- **LIT — Learning Interpretability Tool** (Google PAIR), Apache-2.0,
  [PAIR-code/lit](https://github.com/PAIR-code/lit).
  **Actively maintained as of 2025.** Sequence Salience module (Tenney et al.,
  arXiv:2404.07498) gives token-level salience heatmaps for KerasNLP and HuggingFace
  LLMs, with hierarchical roll-up to word / sentence / paragraph.
  Side-by-side / pin-and-compare mode supports two models or two prompts.
  **Best off-the-shelf path for two open-weight, shared-tokenizer models.**
- **Inseq** (Sarti et al., ACL 2023; active),
  [inseq-team/inseq](https://github.com/inseq-team/inseq), Apache-2.0. Programmatic
  attribution framework; produces `FeatureAttributionOutput` objects you can diff
  downstream. Not a user-facing side-by-side UI, but the cleanest **programmatic
  backbone** for building one.
- **LLM Comparator** (Kahng et al., CHI 2024, arXiv:2402.10524, Google Research).
  Side-by-side comparison of two LLM **responses** with judge-summarized rationale,
  slice analysis, n-gram diff.
  Operates on *outputs*, not on token logprobs of a fixed input — not exactly the user’s
  ask but the slice-and-rationale UI is a strong reference design.
- **AllenNLP Interpret** — archived 2022; not viable for new work.

**Cross-perplexity / per-token disagreement methods (signal-side).**

- **Binoculars** (Hans et al., ICML 2024, arXiv:2401.12070; BSD-3-Clause in repo, check
  release for non-commercial-research clause).
  The ratio `log PPL_observer(x) / log X-PPL_{observer,performer}(x)` is **intrinsically
  per-token**; the reference implementation reduces it to a scalar via `.mean()`, but a
  per-token vector is one line away.
  No shipped per-token visualizer.
  Requires shared-tokenizer pair (canonical: Falcon-7B + Falcon-7B-Instruct).
- **DetectGPT** (Mitchell et al.
  2023) and **Fast-DetectGPT** (Bao et al., ICLR 2024). Curvature signals exist per
  token; released code outputs document-level AUROC only.
- **Contrastive Decoding** (Li et al., ACL 2023) and **Critical Tokens** (Lin et al.,
  arXiv:2411.19943). Subtract amateur-LM logits from expert-LM logits during generation;
  the per-token difference is exactly the user’s “where do they disagree” signal.
  No comparison UI shipped.
- **DOLA** (Chuang et al., ICLR 2024). Cross-*layer* contrast within one model; the
  published token × layer heatmaps are a reusable rendering template.
- **Logit-lens / Tuned-Lens** (Belrose et al., 2023;
  [AlignmentResearch/tuned-lens](https://github.com/AlignmentResearch/tuned-lens), MIT,
  active). Per-layer for one model; no canonical cross-model lens but an obvious
  extension.

**Per-vendor fingerprinting.**

- **Bitton, Bitton & Nisan 2025** (arXiv:2503.01659). Three-classifier ensemble
  distinguishes Claude / Gemini / Llama / OpenAI at the **document** level; no per-token
  public visualizer. The per-vendor *word-level* view is essentially unexplored as a
  public tool.

**Speculative decoding as a built-in two-model overlay (the user’s “fast vs.
advanced” framing).**

- **LM Studio (proprietary local app).** Implements speculative decoding with
  **“Visualize accepted draft tokens”** — green tokens for accepted draft proposals,
  plain otherwise. Shipped in LM Studio 0.3.10 (Feb 2025). **The only widely-used product
  today with a token-colored fast-vs-advanced overlay**, but for *live generation*, not
  arbitrary fixed documents.
  Repurposable by force-decoding a target document.
- **vLLM / TGI / llama.cpp / TensorRT-LLM** — all support speculative decoding; expose
  acceptance statistics in logs only.
- **EAGLE** ([SafeAILab/EAGLE](https://github.com/SafeAILab/EAGLE), Apache-2.0, active)
  and **Medusa** ([FasterDecoding/Medusa](https://github.com/FasterDecoding/Medusa),
  Apache-2.0, active).
  Framework-level; UI left to consumers.

**Cleanest off-the-shelf paths today (ranked by build cost).**

1. **DIY over OpenAI-compatible APIs that return `logprobs`.**
   `bradsjm/logprob-visualizer` (single-model) and the OpenAI cookbook `logprobs`
   example are the starting points; render two parallel token streams colored by
   per-model logprob and a Binoculars-style ratio.
   Caveats: Anthropic’s public API has only intermittently supported logprobs, not for
   all models (community shim `anerli/anthropic-logprobs` is partial); ~23% of
   OpenRouter endpoints honor logprob requests (arXiv:2512.03816); different tokenizers
   force alignment at the **whitespace-delimited word or sentence** level when vendors
   disagree.
2. **LIT in side-by-side mode**, two open-weight models with shared tokenizer (e.g.
   Llama-3.2-1B vs. Llama-3.3-70B, Mistral base vs.
   instruct). Best fidelity / lowest custom code for that case.
3. **Binoculars as scoring backend + bespoke GLTR-style renderer.** Strip `.mean()`,
   render per-token ratio.
   Constrained to shared-vocab pairs.
4. **Force-decode through speculative-decoding plumbing** (llama.cpp / vLLM with draft +
   target). Highest engineering cost; cleanest semantic match to “fast vs.
   advanced.”

**Gaps the project would need to build:**

1. **Cross-tokenizer alignment** for vendor pairs (Claude vs.
   GPT vs. Gemini) — the single most important missing piece.
2. **Black-box-friendly cross-PPL** for API-only vendors without full logprobs
   (token-forcing via constrained generation, or a Fast-DetectGPT-style sampling
   estimate).
3. **A per-document overlay UI.** Every relevant signal (Binoculars, Contrastive
   Decoding, Critical Tokens, DetectGPT) has been published with **paper-quality plots
   only**; nothing ships as a deployable web overlay.
4. **Sentence- and phrase-level roll-up logic** with a defensible aggregation rule (mean
   / max / length-normalized perplexity / entropy).
5. **A two-vendor agreement metric** for tokenizer-mismatched pairs — a word-aligned KL
   or rank-disagreement is the natural primitive and does not appear to be a published
   artifact.

#### pp-81yt — Word and n-gram corpus-frequency / rarity overlays

**Headline insight.** Corpus-frequency overlays measure `P(w)` marginalized over a
reference corpus; LLM-likelihood overlays measure `P(w | context)` under a specific
model. The two signals are independent enough to be informative when overlaid, and the
most important 2024–2026 fact for the project is that **`wordfreq` was retired on
2024-09-19** by Robyn Speer, with the explicit reason that *“the open Web (via OSCAR)
was one of wordfreq’s data sources.
Now the Web at large is full of slop generated by large language models … Including this
slop in the data skews the word frequencies.”* Similarly, **Google Books Ngram v3**
stopped updating at the 2020 release covering through **2019**. For the project these
are features, not bugs: frozen pre-LLM snapshots are exactly the clean human-baseline
that the rarity overlay needs.

**The four-quadrant matrix** (the conceptual core of this bead):

| Quadrant | Corpus freq | LLM likelihood | Editorial reading | Example |
| --- | --- | --- | --- | --- |
| **A** | High | High | Unremarkable, fluent | *“The system uses a database to store user accounts.”* |
| **B** | High | Low | **Stylistically marked** — everyday vocabulary doing unusual work | *“The endpoint returns the **doom** of every request.”* — *doom* is corpus-common but unexpected in API docs. Often where editorial decisions live. |
| **C** | Low | High | **Domain-signaling jargon** — correctly used | *“The transformer applies **RoPE** to query and key projections.”* — *RoPE* is corpus-rare but contextually expected in an ML paper. Register, not “fancy word.” |
| **D** | Low | Low | **Genuinely striking** — novel coinage, error, or distinctive voice | *“He gazumped the indifferent gloaming.”* Either literary register or mistake worth flagging. |

LLM-only overlays cannot distinguish B from D (both LLM-unlikely).
Corpus-only overlays cannot distinguish C from A (both LLM-likely).
**The combined two-axis overlay is the smallest tool that supports all four readings** —
and it is exactly the use case the user described ("originality / novelty visualization"
for human writing as well as AI detection).
Mismatch quantification: `Δ(w) = z(log P(w|context)) − z(log P_corpus(w))`; highest
`|Δ|` are precisely B and C.

**Frequency libraries and corpora (frozen pre-LLM = feature).**

- **`wordfreq` 3.1.1** (Apache-2.0). Zipf scale across 40+ languages.
  Last release pre-retirement; **the clean frozen baseline.**
- **SUBTLEX-US / SUBTLEX-UK** (Brysbaert & New; Van Heuven et al.). ~51M film/TV
  subtitle tokens; **SUBTLEXcd** contextual-diversity column (% films containing the
  word) is itself a useful axis.
  CC-BY-NC-SA.
- **Google Books Ngram Corpus v3** (Feb 2020 release, through 2019). 1–5-grams in 8
  languages; `orgtre/google-books-ngram-frequency` repackages as flat per-language
  lists.
- **COCA** (Davies, BYU). 1B+ words; commercial; web API.
- **BNC / BNC2014 / OEC**, **NLTK FreqDist on Brown** — research and pedagogical
  comparators.

**Lexical-sophistication / readability lineage.**

- **TAALES 2.8** (Kyle, Crossley).
  400+ indices: word frequency (SUBTLEX/BNC/COCA), n-gram association (MI / T-score /
  ΔP), academic register (AWL/NGSL), psycholinguistic norms.
  Free, GUI-only.
- **Coh-Metrix** (Memphis).
  200+ cohesion / diversity / complexity indices; free web UI, no released codebase.
- **textstat** (PyPI, MIT, active 2025 with Py3.12). Flesch-Kincaid / SMOG / Gunning-Fog
  / Dale-Chall / Coleman-Liau / etc.
  The cheap robust default.
- **textdescriptives** (Aarhus, Apache-2.0, current 2.8.4, spaCy v3 plugin).
  Readability + lexical diversity (TTR, MATTR, MTLD, HD-D) + dependency distance +
  quality filters. **Best modern Python option** for combined readability + diversity +
  structure metrics in one pipeline.

**ESL / pedagogy precedent — the closest existing “color each word” prototype:**

- **Lextutor / VocabProfile** (Cobb).
  The canonical K1/K2/AWL color-overlay tool since the early 2000s; CEFR inferential
  profiler since 2018.
- **VocabKitchen** ([vocabkitchen.com/profile](https://www.vocabkitchen.com/profile)).
  Paste-text web tool, instant CEFR (A1–C2) or AWL/NAWL band coloring + percent-by-band
  breakdown. Free, active.
  **Closest direct UX precedent for a per-word overlay.**
- **English Vocabulary Profile** (Cambridge), via Text Inspector.
- **CEFR-J Wordlist v1.6** (Tono, TUFS). CC-licensed for research and commercial use
  with citation. Mirrored as `openlanguageprofiles/olp-en-cefrj`.
- **NGSL** (Browne, Culligan, Phillips), CC-BY-SA, 2,809 lemmas covering ~92% of general
  English; updated 2023, v1.2.
- **AWL** (Coxhead 2000) → **NAWL** (2013) — academic register lists.

**Stylometric / literary tools.**

- **stylo R package**
  ([computationalstylistics/stylo](https://github.com/computationalstylistics/stylo),
  GPL, **CRAN 2025-07-23**). Burrows’s Delta / Eder’s Delta / kNN / oppose / rolling /
  imposters. Still actively maintained.
- **Voyant Tools** (Sinclair & Rockwell).
  Free, browser-based, multi-panel DH workbench (Cirrus, Trends, KWIC, Bubblelines,
  TF-IDF distinctive words).
  **Cleanest multi-overlay DH visualization precedent for UX patterns.**

**Concordance UIs.**

- **AntConc 4.4.0** (Anthony, Waseda) — 4.3.1 released **2025-11-14**, free,
  all-platform, **actively maintained reference free concordancer**.
- **Sketch Engine** — commercial; word sketches give one-page grammar-and-collocation
  summary per lemma.
- **WordSmith Tools**, **CQPweb / BNCweb**, **#LancsBox X**.

**N-gram-level rarity.**

- **kenlm** (Heafield, LGPL, [kpu/kenlm](https://github.com/kpu/kenlm)). C++ + Python
  bindings; modified Kneser-Ney smoothing.
  Train a small frozen 5-gram on Wikipedia + pre-2022 Common Crawl to get an
  `log p(w | context)` that **bridges unigram corpus frequency and full-LLM
  likelihood**.
- **AutoPhrase**, **ToPMine**, **PhraseBERT**, **KeyBERT**, **YAKE!** for phrase mining
  — feed the soft-match tier in `pp-84ya`.

**Visual design recommendation for the combined overlay.**

- Hue = corpus-frequency Zipf band (5-bin Lextutor-style palette).
- Saturation / background opacity = LLM-likelihood band (GLTR-style top-10 / top-100 /
  top-1000 / tail).
- Quadrant matrix becomes directly readable: A washed out, B colored but pale (everyday
  word in surprising spot), C saturated in a frequent-word hue (jargon), D saturated in
  a rare-word hue (striking).
- Toggleable single-axis views: frequency-only (ESL / VocabKitchen mode), LLM-only
  (matches `pp-dc53`), |Δ| delta mode.
- Sentence-level rollups: mean Zipf, TTR, mean LLM-surprisal, Binoculars ratio.
- Reference selectability: corpus ∈ {wordfreq-frozen, SUBTLEX-US, Google Ngram 2019,
  NGSL/AWL/EVP CEFR band}; LLM ∈ {Llama-3.1-8B, Llama-3.1-8B-Instruct sibling for
  Binoculars}.

**Cleanest fully-redistributable English stack:** NGSL + wordfreq 3.1.1 + SUBTLEX-US +
Google Ngram 2019.

**Gaps.**

- **No actively-maintained `wordfreq` successor** that meets Speer’s pre-LLM-data
  integrity bar. Either freeze a pre-2022 snapshot and refuse to update, or accept that
  the signal partially measures LLM influence on the open web.
  This is a *structural* constraint for the project, not just a tooling gap.
- **No public tool ships a true two-axis overlay** (corpus × LLM) as of May 2026.
  VocabKitchen / Lextutor are one-axis (corpus); GLTR / Inseq / LMDiff are one-axis
  (LLM). Composing the two is open territory.
- **Phrase-level rarity above 5-gram** is not practically available outside
  research-grade phrase miners — the soft-match phrase tools (`pp-84ya`) and a small
  kenlm partially fill it.
- **No standard sense-disambiguated frequency overlay** — *bank* (river) vs.
  *bank* (financial) collapse in `wordfreq` / SUBTLEX. EVP partially solves this via
  CEFR sense assignment but is not exposed as a Python library.
- **License heterogeneity** — wordfreq Apache-2.0, SUBTLEX CC-BY-NC-SA, Google Ngram
  bespoke, COCA commercial, EVP commercial-ish, NGSL CC-BY-SA, CEFR-J
  research-and-commercial-with-citation.
  Any shipped tool must mix-and-match carefully.

#### pp-dc53 — Per-token / per-word / per-sentence distributional-fit visualization

**Headline.** The landscape has bifurcated since GLTR (Gehrmann, Strobelt & Rush, ACL
2019\) into AI-detection UIs (verdict-focused), mechanistic interpretability libraries
(researcher-focused, richer per-token signals), and psycholinguistic surprisal toolkits
(per-word, but render to scatterplots for cognitive scientists, not overlays for
writers). The closest existing tool to the user’s “color each word by how
out-of-distribution it is, for any document” framing is **Glitter** (UFAL Prague,
arXiv:2601.05411) — a lexical-surprisal heat overlay explicitly designed for
*readability of administrative text* rather than AI detection.

**Best off-the-shelf components.**

- **minicons** ([kanishkamisra/minicons](https://github.com/kanishkamisra/minicons),
  MIT). Cleanest “give me per-token surprisal under model X” API.
  `LMScorer.token_score()` / `sequence_score()`. Handles sub-word merging into words.
  Used in dozens of psycholinguistics papers.
  **Strongest candidate as the precompute backbone.**
- **LIT Sequence Salience** (Tenney et al., NAACL 2024 demo, arXiv:2404.07498;
  [PAIR-code/lit](https://github.com/PAIR-code/lit), Apache-2.0, active 2025+). **The
  only mature multi-granularity overlay** — native dynamic aggregation across tokens /
  words / sentences / paragraphs at the touch of a control.
  Best UX precedent for what the user described.
- **Inseq 0.7.0** ([inseq-team/inseq](https://github.com/inseq-team/inseq), Apache-2.0,
  Feb 2026 release, active).
  Programmatic backbone with a standardized save/reload format
  (`FeatureAttributionOutput`) and HTML / JSON / `rich` renderers.
  PyTorch + HF Transformers; covers Llama, Mistral, Qwen, Gemma, T5, mBART, NLLB.
- **codelion/LogProbsVisualizer** (HF Space).
  Reads OpenAI-`logprobs`-JSON shape; the de-facto interchange schema.
- **MGT-Eval** ([Liyuuuu111/MGT-Eval](https://github.com/Liyuuuu111/MGT-Eval), ACL/ICLR
  2026, arXiv:2604.25152). Unified detector-comparison harness — runs DetectGPT,
  Fast-DetectGPT, Binoculars, GLTR and more on the same input.
- **Ecco** ([jalammar/ecco](https://github.com/jalammar/ecco), BSD-3-Clause).
  Jupyter-native; inline rendering of “the model’s predicted token distribution at each
  step” — exactly suited to a literary or originality-analysis notebook.
- **PsychFormers**, **pangoling** (rOpenSci, R, MIT), **TextDescriptives** (Apache-2.0).
  Psycholinguistic-tradition tools that are quietly the closest to the user’s framing of
  “originality / novelty visualization for human prose.”

**Commercial AI-detection visualizers (closed, not reusable as infra).**

- **GPTZero Premium** — color-coded sentence highlights on Deep Scan; no per-token
  exposure.
- **Pangram v3.0** (Dec 2025) — “AI Phrases” phrase-level highlights with frequency
  counts + four-tier ordinal classification per region (Fully Human / Lightly /
  Moderately / Fully AI). The four-tier ordinal scale is a useful architectural lesson:
  **bucketed outputs read better than continuous gradients even at sentence tier.**

**Closed-weight reference points.** `OpenLogProbs`
([justinchiu/openlogprobs](https://github.com/justinchiu/openlogprobs)) recovers full
next-token vectors by binary-search over logit-bias APIs but is fragile and now mostly
blocked by providers; **assume the project’s reference-LM column needs open-weight
models running locally**, with optional augmentation by whatever vendor logprobs are
exposed.

**Granularity-aware tokenization caveat (Oh & Schuler, ACL 2025, arXiv:2502.xxxxx).**
Token granularity (vocab size ≈ 8K optimal) materially affects how well surprisal
matches reader behavior.
Practical Prose should standardize on a granularity — most likely whitespace-words with
sub-word merge by sum — regardless of the underlying LM’s BPE.

**Four-layer architecture for a multi-granularity overlay.**

1. **Precompute** (open-weight reference LMs).
   For each `(document, reference_model)` pair, compute per-token log-probability, rank,
   top-k alternatives. **Use minicons** as the API. Cache to **Parquet** keyed by
   `(doc_id, model_id)`.
2. **Aggregate.** Token, word (sub-word sum), phrase (n-gram or chunk-aware via spaCy),
   sentence (mean + max + top-k bucket counts; keep all three), paragraph (mean +
   burstiness variance).
   Borrow LIT’s aggregation conventions.
   Add **Binoculars-style cross-model ratio** as a derived metric.
3. **Storage / interchange.** Parquet on disk, **OpenAI-logprobs-JSON shape on the
   wire** so existing tools (LogProbsVisualizer, Inseq) interop.
   Schema:
   `(doc_id, token_idx, char_start, char_end, model_id, logprob, rank, top_k_alts)`.
4. **Renderer.** Self-contained static HTML; 4-bucket categorical color (GLTR’s discrete
   choice reads better than continuous gradients at body text); LIT-style granularity
   switcher; hover top-k; gutter color bar.

**Gaps.**

- No tool ships **comparable scoring across N reference LMs**. Binoculars does two in a
  fixed ratio; nothing supports arbitrary N with user-selected aggregation.
- No tool ships **static / offline rendering** suitable for a one-file report.
  LIT needs a server; Inseq HTML is functional but not polished; Ecco is Jupyter-only.
- **Phrase-level (syntactic-chunk-aware) aggregation** is not rolled into any surveyed
  surprisal overlay.
- **Calibration across reference models** (high-surprisal under Llama-3 vs.
  high-surprisal under GPT-2 are not commensurable in raw nats) requires normalization
  (z-score, percentile rank, or rank-based à la GLTR). No surveyed tool does this
  explicitly.
- **Provenance trail** — no tool writes “scored against Llama-3.1-70B-Instruct@<sha> on
  YYYY-MM-DD” into the artifact.
  This is the project’s inspectability principle and would have to be designed in.

#### pp-xrqd — Existing prose-visualization UIs that compose multiple overlays

**Five recurring UX patterns** across writing aids / DH / stylometry / pedagogy /
annotation / AI-text detection:

1. **Pattern A — Inline color + hover detail + summary sidebar.** Hemingway, Grammarly,
   GLTR, Sapling, Lextutor.
   Works when there’s ≤1 dominant overlay; ceiling at 4–5 categorical colors before the
   page becomes unreadable.
   **Grammarly’s choice of *thin underline* rather than background fill** is what makes
   multiple categories cohabit the same span.
2. **Pattern B — Toggleable layers over one canvas.** ProWritingAid (reports), Microsoft
   Editor, INCEpTION (layer manager), BRAT. The right answer when categories would
   visually collide.
3. **Pattern C — Coordinated multi-panel views.** Voyant (skins), AntConc, Sketch
   Engine, BertViz, exBERT. Architecturally simple — a small reactive store of “current
   selection” feeds all panels — but costs vertical space.
4. **Pattern D — Global / overview → instance drill-down.** LMDiff (Global View →
   Instance View), GPTZero, Stylo `rolling.classify()`, AntConc Concordance Plot,
   Pangram.
5. **Pattern E — Per-position ribbon / margin heatmap.** AntConc’s Concordance Plot bar
   code, Stylo’s rolling-stylometry strip, GitHub-style code-minimap scroll views,
   GPTZero’s overview bar.
   The cleanest *navigator* (Pattern D’s overview) when the signal is scalar over
   document position.

**Patterns that don’t work** and to avoid:

- Stacked background fills for multiple categories on the same span (unreadable past 2
  categories).
- Dense inline numerical badges (push to hover or sidebar).
- Continuous color ramps at body-text scale (humans read at most ~4 saturation levels at
  small sizes — bucket discretely, GLTR / Lextutor style).
- More than 5 panels at once (Voyant’s default 5-panel skin already feels tight).

**Strongest single body of prior art.** The **Strobelt corpus** — **GLTR** + **LMDiff**
\+ **LIT** — is the most coherent body of prose-overlay design work, with a consistent
design vocabulary: bucketed categorical color, side ranking panel, hover-driven detail,
global→instance flow.
Cite all three.

**Recommended composition for pprose-eval** — hybrid of patterns **B + D + E + A** in
three coordinated regions:

- **Top region — rubric / dimension overview (Pattern D overview).** The 20-dimension
  rubric scoring as a compact header; the *Global View* in LMDiff terms.
  Reuses the existing design system’s `dim-name` chips and group accent colors.
- **Center region — document canvas (Pattern B layer-toggled single canvas).** One
  canonical document view.
  A small fixed **layer manager** widget (checkbox row, not a sidebar tree) controls
  visibility for: AI-tell phrase matches (span, category color, ≤5 from
  `ai-prose-corrections.md`); LLM surprisal (per-token, GLTR-style 4-bucket categorical
  green → purple); Word rarity (per-word, Lextutor-style 4-bucket); Cross-model
  disagreement (per-token, LMDiff-style signed diverging color); Structural features
  (passive, long sentence — Hemingway-style).
  Default: **one layer active at a time** as background fill; *other enabled layers
  render as thin underline or margin dot* — the Grammarly-underline-not-fill lesson.
  Per-paragraph aggregate ribbon down the left margin (Pattern E): thin colored strip
  whose color encodes the active layer’s aggregate for that paragraph (AntConc
  Concordance Plot, rotated).
- **Right region — inspector (Pattern A detail).** Side panel showing **all overlays’
  values for the selected span** at once: rubric tags, AI-tell match with quoted rule,
  LLM surprisal (numeric + bucket), corpus Zipf band, cross-model diff.
  Stacking is cheap here; canvas does not.

**Multi-model views:** prefer LMDiff signed-diff color on the same canvas; side-by-side
panels only for >2 models.

**Architectural notes.**

- Pre-compute everything; static HTML; coordinated-state store
  `{selectedSpan, activeLayer, enabledLayers}` (Voyant pattern, scaled down to one
  document).
- All overlay palettes go through the existing design system
  ([tools/design-system/design-system.md](../../../tools/design-system/design-system.md))
  and reuse the group accents.
  GLTR’s 4-bucket ramps map naturally to the existing 4–5 step lightness ramps in HSL —
  **reuse, don’t invent**.

#### pp-84ya — Soft / fuzzy / semantic phrase matching for prose linting

**Headline.** Every current AI-tell catalog (Slopless, Slop Cop, stop-slop, Prose
Polisher, slop-guard, proselint, Vale, write-good, and `ai-prose-corrections.md` itself)
is essentially **regex with token affordances**. Soft matching is the next step.
A four-tier architecture covers the space; each tier emits the same
`Match(rule_id, span, tier, score, detail)` record so renderers and CI gates can pick
the precision/recall point per consumer.

**Tooling by tier.**

- **Token-attribute / dependency matchers.** **spaCy Matcher** (Apache-2.0; `LEMMA` /
  `POS` / `DEP` / regex over `TEXT` / sets / quantifiers; the workhorse for “verb in
  {delve, dive, unpack, explore} + into + NOUN” without enumerating conjugations).
  **spaCy DependencyMatcher** — the **de-facto semgrep-for-prose**: pattern matching
  over the dependency parse via Stanford Semgrex operators.
  Slower (~2K–10K tokens/sec, parser-bound) but the right primitive for syntactic
  constructions like *self-negating parallel* regardless of surface words.
  **spaCy PhraseMatcher** for tens-of-thousands literal phrases (internal Aho-Corasick
  trie). **Stanford TokensRegex / Stanza** — equivalent capability with JVM dependency;
  for Python-first stacks, spaCy is the easier default.
- **Fuzzy / multi-pattern automata.** **`ahocorasick_rs`** (Apache/MIT, G-Research,
  **1.5–7× faster than `pyahocorasick`**; current best pick).
  **`rapidfuzz`** (MIT, active) for similarity scoring including Jaro-Winkler, Hamming,
  Levenshtein. **`fuzzysearch`** (MIT) for sub-string approximate match.
  **Intel hyperscan / Vectorscan** (BSD-3) when the catalog grows past a few thousand
  patterns.
- **Semantic / embedding-based matching.** **`sentence-transformers` v5.x** (Apache-2.0,
  joined HF Oct 2025). Encoder pick: **`BAAI/bge-small-en-v1.5`** (Apache-2.0,
  MTEB-leading at ~33M params, ~10ms/sentence on CPU) for default; `bge-base-en-v1.5`
  for batch; `bge-m3` for multilingual.
  **FAISS `IndexFlatIP`** (exact cosine) for the realistic 250–1000-vector exemplar bank
  — zero dependency, fast, no daemon.
  **ColBERTv2 / Jina-ColBERT-v2** (MIT) for late-interaction span localization within
  long sentences. **SimCSE / DiffCSE** for domain-specific encoder training if needed.
  **SetFit** (Apache-2.0) for few-shot per-rule binary classification.
- **Phrase mining (the *supply* side).** **AutoPhrase** (Apache, aging Java code),
  **KeyBERT** (MIT, active), **YAKE!** (MIT, statistical, fast), **PatternRank**
  (KeyBERT + POS filter), **LMPhrase** (research artifact; uses BERT as silver-label,
  BART as generator). Use against unedited-LLM-output archives ranked by Kobak-style
  post-LLM / pre-LLM frequency ratio to surface candidate new rules for human review.
- **LLM-as-judge** as advisory T4 only; cite the 2025 EMNLP “Opportunities and
  Challenges of LLM-as-a-judge” survey on position, verbosity, and shortcut bias.
  Useful for catch-all but not for CI gating.

**Current state of AI-tell catalogs:** every shipping catalog is pure regex;
**stop-slop** and **claude-slop-detector** lean on the LLM’s general competence rather
than an explicit paraphrase-exemplar bank.
**No catalog yet runs a precomputed embedding bank** — this is the clear next
contribution.

**Recommended four-tier minimal architecture.**

| Tier | Engine | When it fires | Block in CI? |
| --- | --- | --- | --- |
| **T0 regex** | Python `re` (or `hyperscan` if rules > ~1000) | Literal hits | Yes |
| **T1 fuzzy** | `ahocorasick_rs` + `rapidfuzz` windowed n-grams | Spelling / contraction / 1–2 edit variants | Yes |
| **T2 semantic** | `bge-small-en-v1.5` + FAISS `IndexFlatIP` over 5–20 hand-curated paraphrase exemplars per rule, cosine ≥ ~0.78 | Novel paraphrases of the construction | Advisory |
| **T3 structural** | spaCy `DependencyMatcher` against `en_core_web_lg` | Constructions like *self-negating parallel*, *meta-commentary opener*, *imperative direct-address* — words-be-damned | Yes |
| **T4 LLM-judge** (optional) | Haiku-class model | Catch-all for uncovered paragraphs | Advisory only |

**Unified record.** All tiers emit `Match(rule_id, span, tier, score, detail)`; the
renderer (per `pp-xrqd`) colors by tier; the CI gate picks which tiers block.

**Authoring loop.** Mine candidate rules from an archive of unedited LLM output via
AutoPhrase or KeyBERT; rank by Kobak-style frequency-ratio; human-author the regex (T0);
generate 5–20 paraphrase exemplars (T2; seed with LLM paraphrase generation, then
human-review); decide if a structural template (T3) is warranted.

**Gaps.**

- **No off-the-shelf semgrep-for-prose with YAML/captures ergonomics.**
  `DependencyMatcher` is the capability; a thin wrapper translating a YAML pattern DSL
  to Matcher patterns is a real contribution and does not exist.
- **No public AI-tell exemplar bank** as an HF dataset — every catalog ships regex only.
- **No open cross-model AI-tell drift dataset** for general prose (Kobak/Juzek-style
  work exists for biomedical abstracts).
- **LLM-judge bias controls** specific to span-flagging are under-studied.
- **CPU latency at keystroke tier** is tight (BGE-small ~10ms/sentence is fine for
  paragraph-on-save, marginal for keystroke).
  ONNX quantization / `fastembed` is the path.

### Phase 2 consolidated recommendations

The five sub-beads converge on a single architecture and a single strategic call.

**Strategic call: build a “GLTR-for-2026” overlay framework, not a classifier.** Both
`pp-ne5w` (math) and `pp-3vt3` (reliability ceiling) from Phase 1 said do not ship a
verdict; Phase 2 says the genuine opportunity is in a *visualization primitive* that
supports multiple use cases (AI detection, originality / novelty, literary stylistics,
ESL pedagogy, comparative author analysis, cross-model fingerprinting).

**Architecture (cross-cutting across sub-beads):**

1. **Measurement layer** (`pp-dc53` + `pp-81yt` + `pp-gcdj`).
   - Per-token / per-word log-probability + rank under one *or more* open-weight
     reference LMs (Llama-3.1-8B as default; minicons as API).
   - Per-word corpus-frequency Zipf band from `wordfreq` (frozen), SUBTLEX-US, Google
     Ngram 2019.
   - Per-document structural metrics (passive ratio, sentence-length variance,
     subordinate-clause density, type-token ratio) via **textdescriptives** (Apache-2.0,
     spaCy plugin).
   - Cross-model agreement signal (Binoculars-style ratio for shared-vocab pairs;
     word-aligned KL or rank-disagreement for vendor-mismatched pairs — *the project’s
     greenfield primitive*).
2. **Soft-match layer** (`pp-84ya`). Four-tier matcher emitting unified `Match` records:
   T0 regex / T1 fuzzy (`ahocorasick_rs` + `rapidfuzz`) / T2 semantic (BGE-small + FAISS
   over per-rule paraphrase exemplars) / T3 structural (`DependencyMatcher`). Rule IDs
   match anchors in `ai-prose-corrections.md`.
3. **Storage / interchange.** Parquet on disk for the measurement tables;
   OpenAI-logprobs-JSON shape on the wire for renderer interop; provenance metadata
   (`scored against Llama-3.1-8B-Instruct@<sha> on YYYY-MM-DD`) baked into every
   artifact.
4. **Renderer** (`pp-xrqd`). Self-contained static HTML, three regions: top rubric
   overview, center document canvas with layer manager + margin ribbon, right inspector
   showing all overlays for selected span.
   Layer-toggle one-at-a-time as fill, other layers as underline / margin dot.
   GLTR-style **4-bucket categorical** color (not gradients); design-system HSL palette;
   coordinated-state store.

**Two-axis overlay** (the conceptual contribution from `pp-81yt`): hue =
corpus-frequency Zipf band; saturation = LLM-likelihood band; quadrants A/B/C/D directly
readable. Toggleable single-axis views for ESL-only or LLM-only use cases.

**Multi-model overlay** (the conceptual contribution from `pp-gcdj`): LMDiff-style
signed-diff color per token on the same canvas for two models; side-by-side panels only
past two. Cross-tokenizer alignment (Claude vs.
GPT vs. Gemini) is the project’s single most important greenfield primitive.

**Minimum-viable first slice** (if the project ships a prototype):

- Single open-weight reference LM (Llama-3.1-8B) under **minicons**.
- Single corpus-frequency reference (`wordfreq` 3.1.1, frozen).
- Existing `ai-prose-corrections.md` rules at T0 only.
- Renderer with one document canvas, two toggleable layers (LLM surprisal + AI-tell
  matches), per-paragraph ribbon, hover inspector.
  Built on existing design-system HSL palette.

This slice answers the user’s framing ("color words by how out-of-distribution they are"
\+ “linting for prose with soft matching”) and adds nothing the project would have to
throw away to extend to multi-model, semantic matching, or structural rules.

## References

> Full citations are inline above; this is a quick index.

- Galpin, Anderson & Juzek 2025: <https://arxiv.org/abs/2506.21817>
- Anderson, Galpin & Juzek 2025: <https://arxiv.org/abs/2508.00238>
- Geng & Trotta 2025: <https://arxiv.org/abs/2502.09606>
- Kousha & Thelwall 2025/26: <https://arxiv.org/abs/2509.09596>
- Lin & Zhu 2025: <https://arxiv.org/abs/2504.13629>
- Liu et al. 2025: <https://arxiv.org/abs/2511.15872>
- Vansteenhuyse 2026: <https://arxiv.org/abs/2604.09316>
- Miletić & Falk 2026: <https://arxiv.org/abs/2605.19936>
- Rallapalli et al. 2026: <https://arxiv.org/abs/2604.14111>
- Bitton, Bitton & Nisan 2025: <https://arxiv.org/abs/2503.01659>
- Keck 2025: <https://www.pieceofk.fr/the-rise-of-the-em-dash-in-ecology-abstracts/>
- Freeburg 2026: <https://arxiv.org/abs/2603.27006>
- Ahmed & Hammond 2026: <https://arxiv.org/abs/2602.15514>
- RAID (Dugan et al.) 2024: <https://arxiv.org/abs/2405.07940>
- Pangram (Emi & Spero) 2024, v3 2025: <https://arxiv.org/abs/2402.14873>
- Fast-DetectGPT (Bao et al.)
  ICLR 2024: <https://arxiv.org/abs/2310.05130>
- SynthID-Text (Dathathri et al.)
  *Nature* 2024: <https://www.nature.com/articles/s41586-024-08025-4>
- Pasquini et al. 2026: <https://arxiv.org/abs/2603.03410>
- SynGuard 2025: <https://arxiv.org/abs/2508.20228>
- DAMAGE 2025: <https://arxiv.org/abs/2501.03437>
- Pudasaini et al. 2026: <https://arxiv.org/abs/2603.23146>
- Xia, Stańczak & Roth EACL 2026: <https://arxiv.org/abs/2601.07974>
- Pegoraro et al. NAACL Findings 2025:
  <https://aclanthology.org/2025.findings-naacl.271/>
- Wikipedia *Signs of AI writing*:
  <https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing>
- Bouchard 2026:
  <https://louisbouchard.substack.com/p/how-to-edit-ai-writing-so-it-sounds>
- Vollmer: <https://matthewvollmer.substack.com/p/i-asked-the-machine-to-tell-on-itself>
- Guo: <https://www.ignorance.ai/p/the-field-guide-to-ai-slop>
- Hills & Illingworth: <https://charliehills.substack.com/p/ai-slop>
- Foote: <https://biggerandbetter.substack.com/p/the-anti-ai-slop-skill>
- Hassid: <https://ruben.substack.com/p/its-not-x-its-y>
- Slopless: <https://github.com/agent-quality-controls/slopless>
- avoid-slop: <https://github.com/shannhk/avoid-slop>
- anti-slop-writing: <https://github.com/adenaufal/anti-slop-writing>
- Word.Studio Cliché Finder: <https://word.studio/tool/cliche-finder/>
- LSSU Banished Words 2026:
  <https://www.lssu.edu/resources/about-lssu/traditions/banishedwords/>

<!-- This document follows common-doc-guidelines.md.
Review guidelines before editing.
-->
