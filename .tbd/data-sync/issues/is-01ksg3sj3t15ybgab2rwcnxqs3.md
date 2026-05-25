---
type: is
id: is-01ksg3sj3t15ybgab2rwcnxqs3
title: "Research: distributional-fit visualization and soft-match phrase linting for prose"
kind: epic
status: closed
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-05-25T17:44:16.757Z
updated_at: 2026-05-25T17:58:31.802Z
closed_at: 2026-05-25T17:58:31.799Z
close_reason: "Phase 2 (5 sub-beads) complete: pp-dc53 (distr-viz tools), pp-gcdj (multi-model diff), pp-81yt (rarity overlay + 4-quadrant matrix), pp-84ya (soft-match phrase linting + 4-tier architecture), pp-xrqd (UI patterns + 3-region composition). All folded into research-2026-05-25-ai-prose-detection.md. CONVERGENT RECOMMENDATION: build a 'GLTR-for-2026' visualization framework, not a classifier (also confirmed by Phase 1 pp-ne5w + pp-3vt3). Architecture: measurement layer (minicons + wordfreq + textdescriptives + Binoculars-ratio) -> soft-match layer (4-tier: regex / ahocorasick_rs+rapidfuzz / BGE-small+FAISS / DependencyMatcher) -> Parquet/JSON storage with provenance -> static-HTML renderer with 3 coordinated regions (rubric overview, document canvas with layer manager + margin ribbon, inspector). Two-axis overlay (hue=Zipf band, saturation=LLM-likelihood band) directly maps to A/B/C/D quadrants. GLTR 4-bucket categorical color > continuous gradient. Grammarly's underline-not-fill lesson lets multiple layers cohabit spans. Minimum-viable slice: single open-weight ref LM + frozen wordfreq + existing ai-prose-corrections.md at T0 + one canvas + 2 toggleable layers. Cross-tokenizer alignment (Claude vs GPT vs Gemini) is the project's most important greenfield primitive. Next step: user reviews Phase 2 results and decides whether to draft a coding-spike bead."
---
Phase-2 research extending pp-ymjj. SCOPE: not only AI detection — also general textual analysis of prose against the distributions captured by LLMs (novelty/originality, stylistic analysis, ESL feedback, literary analysis, comparative stylistics). Five threads on word/sentence/token visual overlays, multi-model comparison, word-rarity overlays, soft-matched phrase linting, and existing prose-visualization UIs. Tracking doc: docs/project/research/research-2026-05-25-ai-prose-detection.md.
