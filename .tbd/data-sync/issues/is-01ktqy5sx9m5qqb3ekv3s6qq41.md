---
type: is
id: is-01ktqy5sx9m5qqb3ekv3s6qq41
title: "lint: optional tier-2 cheap-model detection pass (--detect-model)"
kind: task
status: open
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md
labels: []
dependencies: []
created_at: 2026-06-10T04:55:43.784Z
updated_at: 2026-06-10T04:58:23.153Z
---
detect_model_pass(chunks, rules, model) in lint_detect.py: one call per ~2K-token chunk (chunking via TextDoc paragraphs), prompt = all rules' model_hints lines, output = pydantic list of {rule_id, quote} mapped back to spans via exact-quote search; merges into LintReport at tier=model. Model pick + cost numbers per fast-models research bead. Deferred until tiers 0-1 prove out.
MODEL PICKS (researched 2026-06-09): detect-model default gemini-2.5-flash-lite ($0.10/$0.40, native JSON schema; ~0.3 cents per 5K-word doc) or Groq Llama-3.1-8B ($0.05/$0.08, 840 tok/s) for latency. v2 NON-GENERATIVE path: GLiNER2 (205M, Apache-2.0, CPU, pip-installable) — rule model_hints become zero-shot span-extraction labels, near-constant cost in label count; strong on phrase rules, weak on structural; validate per rule. Local mode opt-in only (--local; 4-bit 4B = 2.5-3GB download). No fine-tuning yet; encoder-side SetFit/ModernBERT pays off once ~50-100 labeled exemplars/category accumulate.
