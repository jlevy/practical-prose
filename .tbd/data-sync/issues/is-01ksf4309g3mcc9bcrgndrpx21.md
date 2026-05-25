---
type: is
id: is-01ksf4309g3mcc9bcrgndrpx21
title: "Research: log-prob / distributional-fit AI-text detection methods"
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01ksf42pfnvczg5nas29yptyg8
created_at: 2026-05-25T08:30:11.759Z
updated_at: 2026-05-25T08:37:09.216Z
closed_at: 2026-05-25T08:37:09.211Z
close_reason: "Methodological deep dive on 9 log-prob/distributional-fit detection methods complete. Covered GLTR, DetectGPT, Fast-DetectGPT, Binoculars, Ghostbuster, Pangram v3, distributional/MPE (Liu et al.), SynthID-Text + attacks (Pasquini, SynGuard), and burstiness/Gini. Honest 2026 answer to user's framing: only partial reliability; Binoculars + Fast-DetectGPT with Llama-3-8B + instruct sibling give AUROC ~0.85-0.95 on medium-long clean English, but collapse under DIPPER/StealthRL paraphrase and humanizers; AUROC on Claude 4.x and GPT-5 specifically not publicly reported by any method as of May 2026. Recommendation: do NOT ship a classifier; integrate a per-token LLM-distributional-fit overlay (GLTR-style ranks + sentence-level Binoculars + burstiness/Gini) as auxiliary forensic signals in pprose-eval next to the editorial rule catalog. Concrete 5-step proposal in close-reason."
---
Methodological deep dive on GLTR, DetectGPT, Fast-DetectGPT, Binoculars, Ghostbuster, Pangram, Distributional-GPT (Liu et al. 2025), and watermark-detection scoring. What does each score actually measure? What is the math? What are known FPR/TPR / robustness on current-generation Claude 4.x / GPT-5 / Gemini 2.x? Do any expose the specific tokens/phrases driving detection (so they could feed editorial rules)? Output: write-up that can be folded into the research doc and used as basis for a new bibliography subsection.
