---
type: is
id: is-01ksg3t2c22yczrmm2zyj5v9hw
title: "Research: multi-model comparison overlays for prose (fast vs. advanced; base vs. instruct; vendor diff)"
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01ksg3sj3t15ybgab2rwcnxqs3
created_at: 2026-05-25T17:44:33.409Z
updated_at: 2026-05-25T17:52:35.890Z
closed_at: 2026-05-25T17:52:35.887Z
close_reason: "Multi-model comparison overlay research complete. KEY: no off-the-shelf tool does exactly the user's ask (fixed document, two arbitrary vendor LLMs, per-token overlay). Closest building blocks: LMDiff (Apache-2.0, dormant, requires shared tokenizer) -- conceptual blueprint; LIT Sequence Salience (Apache-2.0, active, Google PAIR, side-by-side mode for shared-vocab open-weight pairs); Inseq (Apache-2.0, active) as programmatic backbone; Binoculars per-token ratio (signal exists, no UI); Contrastive Decoding / DOLA / Critical Tokens (signals from research); LM Studio's speculative-decoding visualizer (only widely-used tool with token-colored fast-vs-advanced overlay, but for live generation not fixed docs); LLM Comparator (Google CHI 2024) for response-level diff. PATH RECOMMENDED: Option A -- DIY logprob overlay over OpenAI-compatible APIs (vendor-portable, ~200-300 LOC). KEY GAPS: cross-tokenizer alignment for vendor pairs (Claude vs GPT vs Gemini); black-box-friendly cross-PPL; per-document UI (every signal has been published with paper-quality plots only, no deployable web overlay)."
---
Survey tools and research for visualizing the *disagreement* or *comparison* between two LLMs on the same passage at the word / sentence level. Use cases: fast-vs-advanced model comparison for quality-vs-speed tradeoff visualization; base-vs-instruct comparison to see RLHF effect; Claude-vs-GPT-vs-Gemini per-token distributional diff (cf. Bitton et al. 2025 vendor fingerprint paper). Cover: LMDiff (Strobelt et al.); model-disagreement / 'where do models diverge' visualization research; Binoculars' cross-perplexity ratio as a per-token diff signal; logit-lens diff variants; ensemble-disagreement papers; OpenAI/Anthropic playground tooling. Output: methods + tools for cross-model overlays, with UX-pattern notes.
