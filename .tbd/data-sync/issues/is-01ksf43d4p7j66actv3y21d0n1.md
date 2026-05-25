---
type: is
id: is-01ksf43d4p7j66actv3y21d0n1
title: "Research: reader-side perception and AI-text detector reliability ceiling"
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01ksf42pfnvczg5nas29yptyg8
created_at: 2026-05-25T08:30:24.917Z
updated_at: 2026-05-25T08:38:17.750Z
closed_at: 2026-05-25T08:38:17.744Z
close_reason: "Reader-side perception and detector-reliability ceiling synthesis complete. KEY NUMBERS: untrained readers 50% (chance, Clark ACL 2021); trained ~55%; expert linguists 38.9% (Casal & Kessler 2023); Miletić & Falk 2026 experts reported difficulty rather than competence; readers PREFER LLM-edited prose on clarity/excitement (Cohen's d=-0.38/-0.26) while unable to discriminate. RAID independent clean accuracy @ FPR=5%: Originality 85.0%, Binoculars 79.6%, Fast-DetectGPT 73.6%, GPTZero 66.5%. Adversarial: Originality 85.0->9.3% under homoglyph; GPTZero 99.7->60.0% under commercial humanizer; Binoculars 94.2->28.2%. Vendor claims (Pangram ~99%) are in-distribution and not reproducible on RAID. Pudasaini 2026 SHAP shows in-distribution features don't transfer. Xia EACL 2026 verifiable claim: tense + pronoun frequency are cross-domain-robust; passives/sentence-length-variance/subordinate-clause density flagged from PDF extraction (verify before quoting). RECOMMENDATION: stay editorial. Do NOT ship a detector verdict in pprose-eval. Optional middle path: surface structural metrics (passive ratio, sentence-length variance, type-token ratio) as descriptive context, not verdicts."
---
Synthesize Miletić & Falk 2026 (arXiv:2605.19936), Pudasaini et al. 2026 (arXiv:2603.23146), Pegoraro et al. NAACL Findings 2025, and DAMAGE 2025 (arXiv:2501.03437) into a single calibrated statement of what classifiers can and cannot do on current-generation models, and what readers can/cannot perceive. Output: a 'Reliability Ceiling' subsection for the research doc + a recommendation to the project on classifier vs editorial approach.
