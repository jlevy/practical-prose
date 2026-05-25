---
type: is
id: is-01ksg3sw4apcbvt8c36bn66zdt
title: "Research: per-token / per-word / per-sentence distributional-fit visualization tools and methods"
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01ksg3sj3t15ybgab2rwcnxqs3
created_at: 2026-05-25T17:44:27.017Z
updated_at: 2026-05-25T17:55:25.271Z
closed_at: 2026-05-25T17:55:25.267Z
close_reason: "Per-token/word/sentence distributional-fit visualization survey complete. KEY TOOLS: minicons (kanishkamisra, MIT) is the cleanest per-token surprisal API and best precompute backbone; LIT Sequence Salience (PAIR-code/lit, Apache-2.0, active 2025+, Tenney et al. NAACL 2024 arXiv:2404.07498) is the only mature multi-granularity overlay -- native dynamic aggregation across tokens/words/sentences/paragraphs at the touch of a control; Inseq 0.7.0 (Apache-2.0, Feb 2026) is the standard programmatic backbone with save/reload format; Glitter (UFAL, arXiv:2601.05411) is the cleanest precedent for readability/literary overlay rather than detection overlay; codelion/LogProbsVisualizer HF Space accepts OpenAI logprobs JSON as de-facto schema; MGT-Eval is the unified detector-comparison harness. ECCO (Alammar, BSD-3) is Jupyter-native. PsychFormers, pangoling (R), TextDescriptives are psycholinguistic-tradition adjacent. OpenLogProbs (binary-search recovery from logit-bias APIs) is fragile and mostly blocked now. ARCHITECTURE RECOMMENDED: 4 layers -- (1) precompute via minicons -> Parquet; (2) aggregate (token/word/phrase/sentence/paragraph + Binoculars cross-model ratio) borrowing LIT conventions; (3) Parquet on disk + OpenAI-logprobs-JSON-shape on wire; (4) self-contained static HTML renderer with GLTR 4-bucket coloring, LIT-style granularity switcher, hover top-k, gutter color bar. KEY GAPS: comparable scoring across N reference LMs (no tool does this); static/offline rendering (LIT needs server); phrase-level (chunk-aware) aggregation; granularity-aware tokenization (Oh & Schuler ACL 2025); calibration across reference models; provenance metadata. Bucketed 4-color ordinal scale (GLTR) reads better than continuous gradient."
---
Survey tools and research for visualizing per-unit distributional fit of prose under one or more LLMs at multiple granularities (token, word, phrase, sentence, paragraph). Scope is BROADER than AI detection: includes literary stylistic analysis, ESL feedback, originality/novelty visualization, and any textual analysis where LLM-distributional context is informative. Cover: GLTR + successors; HuggingFace token-prob spaces; Inseq sequence-attribution library; LIT (Language Interpretability Tool); BertViz / AttentionViz; logit-lens; Lens-LLM; surprisal-based linguistic tools (Hale/Levy surprisal; STARS/Surprisal-from-Reading); academic visualization papers. For each: granularity supported, models supported, pre-compute pipeline shape, export/render formats, license. Output: methods-and-tools survey for the visualization section of the research doc.
