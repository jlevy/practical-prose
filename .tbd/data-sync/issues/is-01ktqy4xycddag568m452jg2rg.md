---
type: is
id: is-01ktqy4xycddag568m452jg2rg
title: "lint: lint_detect.py — tier-0 exact + tier-1 fuzzy detection over TextDoc"
kind: task
status: open
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktqxg5g3mepq69ktcmzgdpp0
  - type: blocks
    target: is-01ktqy4y4qmqv45sr1a9h0vk6f
  - type: blocks
    target: is-01ktqy5sajm7e17m7hx1srdhw9
  - type: blocks
    target: is-01ktqy5sx9m5qqb3ekv3s6qq41
created_at: 2026-06-10T04:55:15.147Z
updated_at: 2026-06-10T05:00:18.151Z
---
New file tools/pprose/src/pprose/lint_detect.py. Functions: build_exact_matcher(rules) (case-insensitive multi-pattern; tool per fuzzy-matcher research bead — start with compiled regex union, upgrade per recommendation); detect_exact(text, matcher, rules) -> list[Match]; window_ngrams(sentence, n_range) helper; detect_fuzzy(sentences, rules) -> list[Match] via rapidfuzz partial_ratio against FuzzyPattern.threshold; dedup_overlapping(matches) -> list[Match] (highest-tier wins, then highest score); detect(text: str, rules) -> LintReport orchestrator. USE chopdiff TextDoc (already a pprose dep, ==0.3.1) for Markdown-aware sentence segmentation with exact source spans (sentence_at_offset) and for skipping code blocks + frontmatter — pattern proven in leximetry (wrk/kmd/leximetry evaluate_text.py uses TextDoc; chopdiff textdoc-spec.md documents span inversion).
TOOL PICKS (researched + locally benchmarked 2026-06-09): REVISES the rapidfuzz plan above. build_exact_matcher uses ahocorasick-rs (Apache-2.0, LeftmostLongest, 0.52ms for 500 patterns/10K words) over a casefolded doc with word-boundary post-filter; template patterns via google-re2 (BSD) as individual (?i) finditer regexes (re2.Set prefilter past ~100 templates, 0.24ms); detect_fuzzy uses fuzzysearch.find_near_matches (MIT, true substring-with-edits, ~0.55ms/pattern at d=1) for a curated <=50-pattern fuzzy subset — NOT rapidfuzz cdist (200ms full-bank, CI-tier only). All three have arm64+x64 wheels and pass the 14-day cool-off. Upgrade path: hyperscan 0.8.2 (Vectorscan static, native caseless + approximate) consolidates templates+fuzzy at 1000s of patterns. spaCy Matcher rejected for v1 (tokenization alone blows the 50ms budget); optional extra later for POS templates. New deps to add to pyproject: ahocorasick-rs, google-re2, fuzzysearch.
