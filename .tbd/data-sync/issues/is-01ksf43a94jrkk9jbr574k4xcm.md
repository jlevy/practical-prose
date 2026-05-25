---
type: is
id: is-01ksf43a94jrkk9jbr574k4xcm
title: "Research: Freeburg 'The Last Fingerprint' em-dash empirics verification"
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01ksf42pfnvczg5nas29yptyg8
created_at: 2026-05-25T08:30:21.987Z
updated_at: 2026-05-25T08:36:34.388Z
closed_at: 2026-05-25T08:36:34.382Z
close_reason: "Freeburg arXiv:2603.27006 verified (E.M. Freeburg, Independent Researcher, 2026-03-27, cs.CL, CC-BY-4.0, code at github.com/emfreeburg/the-last-fingerprint). Per-vendor table confirmed exactly: GPT-4.1 10.62/9.10; Claude Opus 4.6 9.09/0.19; Gemini 2.5 Pro 3.53/0.00; Llama 3.1 8B Instruct and 3.3 70B Instruct both 0.00/0.00; human baseline 3.23 (mean). Markdown-leakage mechanism confirmed verbatim. CRITICAL CAVEAT: paper's 'Altman deliberately tuned em-dash upward' citation does not match the only verifiable Altman em-dash statement (Nov 14 2025 tweet about *suppression* via custom instructions). Bibliography should cite the @sama Nov 14 2025 tweet + TechCrunch directly rather than relay the paper's gloss. Treat Llama 0.00 as fine-tuning signature not base-model tendency (paper itself argues this); cite Claude 9.09->0.19 with the suppression-prompt text since the magnitude is prompt-sensitive."
---
Verify methodology and per-model em-dash rates in arXiv:2603.27006 (Freeburg, Mar 2026) before citing as load-bearing support for the project's em-dash policy. Confirm: rates per 1K words for GPT-4.1, Claude Opus 4.6, Gemini 2.5 Pro, Llama 3.x, human baseline; the markdown-leakage mechanism claim; the Altman public-acknowledgment citation. Output: confirmed/rejected facts + recommended citation language.
