---
type: is
id: is-01ksg3tgzg1rker37jxn32zfmm
title: "Research: soft / fuzzy / semantic phrase matching for prose-style linting beyond regex"
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01ksg3sj3t15ybgab2rwcnxqs3
created_at: 2026-05-25T17:44:48.367Z
updated_at: 2026-05-25T17:56:07.019Z
closed_at: 2026-05-25T17:56:07.016Z
close_reason: "Soft/fuzzy/semantic phrase matching survey complete. KEY TOOLS: spaCy DependencyMatcher (Apache-2.0) is the de-facto semgrep-for-prose -- only mature rule-authorable structural matcher with permissive license, using Stanford Semgrex operators over dependency trees. spaCy Matcher/PhraseMatcher for token-attribute and large literal-phrase lists. ahocorasick_rs (Apache/MIT, G-Research, active 2025-2026, 1.5-7x faster than pyahocorasick) is the current best multi-pattern automaton. rapidfuzz (MIT, active) for similarity scoring; fuzzysearch (MIT) for sub-string Levenshtein. hyperscan/Vectorscan for thousands-of-patterns regex. sentence-transformers v5.x (joined HF Oct 2025) with BGE-small-en-v1.5 (Apache-2.0, MTEB-leading at its size, ~33M params, ~10ms/sentence on CPU) as default encoder + FAISS IndexFlatIP for 250-1000 vector exemplar bank. ColBERTv2 (MIT) / Jina-ColBERT-v2 for late-interaction span localization. SimCSE/DiffCSE for domain training. AutoPhrase (Apache, stale Java), KeyBERT (MIT, active), YAKE!, LMPhrase for phrase mining. CURRENT CATALOGS (Slopless, Slop Cop, Prose Polisher, slop-guard, proselint, Vale, write-good) all pure regex; stop-slop and claude-slop-detector use LLM-as-judge prompting -- the only shipping 'soft matching' today is LLM-on-prompt. RECOMMENDED ARCHITECTURE: 4 tiers each emitting same Match(rule_id, span, tier, score, detail) record: T0 regex (deterministic, blocking CI), T1 fuzzy (ahocorasick_rs + rapidfuzz windowed n-grams), T2 semantic (BGE-small + FAISS exact-cosine over 5-20 hand-curated paraphrase exemplars per rule, threshold ~0.78), T3 structural (DependencyMatcher for self-negating-parallel, meta-commentary openers, imperative direct-address). Optional T4 LLM-judge advisory only (cite 2025 EMNLP bias survey). AUTHORING LOOP: AutoPhrase/KeyBERT over unedited-LLM-output corpus to surface candidates; rank by Kobak-style post-LLM/pre-LLM frequency ratio. GAPS: no off-the-shelf semgrep-for-prose with YAML/captures ergonomics; no public AI-tell exemplar bank as HF dataset; no cross-model AI-tell drift open dataset; LLM-judge bias controls for span-flagging under-studied; phrase-mining license coverage uneven; CPU latency tight at keystroke tier."
---
Survey methods for going BEYOND grep-based AI-tell catalogs to soft / fuzzy / semantic phrase matching. The user's framing: 'soft matching on particular phrases... almost like a linting for prose.' Cover: spaCy Matcher / PhraseMatcher / DependencyMatcher; sentence-transformers + FAISS for semantic phrase matching; AutoPhrase / ToPMine / PhraseLM for phrase mining; fuzzy-search libraries (rapidfuzz, fuzzysearch, hyperscan); Aho-Corasick multi-pattern automata; semgrep-style structural matching for prose (semgrep has prose support? check); the prose-linting niche between proselint/Vale (regex) and full classifiers; existing AI-tell catalogs that have already shipped soft-matching (Slopless, stop-slop, anti-slop-writing, humanizer). Output: methods + libraries + a recommendation for how the project could ship a soft-matched extension of ai-prose-corrections.md.
