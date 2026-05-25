---
type: is
id: is-01ksg3t9qrhhskerk0ayn5jpgj
title: "Research: word and n-gram corpus-frequency / rarity overlays as a complementary view"
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01ksg3sj3t15ybgab2rwcnxqs3
created_at: 2026-05-25T17:44:40.951Z
updated_at: 2026-05-25T17:53:53.530Z
closed_at: 2026-05-25T17:53:53.526Z
close_reason: "Word/n-gram corpus-frequency overlay research complete. KEY INSIGHT: wordfreq retired 2024-09-19 (Speer cited LLM-polluted Common Crawl) and Google Books Ngram v3 frozen at 2019 -- BOTH are now FEATURES not bugs: clean pre-LLM-era baselines for human-reference frequency. Cleanest stack: wordfreq 3.1.1 (Apache-2.0) + SUBTLEX-US (CC-BY-NC-SA) + Google Ngram 2019 + NGSL/AWL/EVP CEFR bands + kenlm for n-gram-LM rarity bridging the unigram and LLM axes. CONCEPTUAL CORE: four-quadrant matrix of corpus-frequency x LLM-likelihood gives editorially distinct readings: A common+likely (unremarkable), B common+unlikely (stylistically marked - 'where editorial decisions live'), C rare+likely (domain-signaling jargon), D rare+unlikely (genuinely striking). LLM-only overlays cannot distinguish B from D; corpus-only cannot distinguish C from A. VISUAL DESIGN: hue=Zipf band, saturation=LLM-likelihood band; quadrants directly readable. Active tooling: textdescriptives (Apache-2.0, spaCy plugin), stylo R package (CRAN 2025-07-23), AntConc 4.4.0, VocabKitchen, Lextutor. License-clean English stack: NGSL + wordfreq + SUBTLEX + Google Ngram 2019. Phrase-level rarity above 5-gram is a gap; sense-disambiguated overlays missing."
---
Word-rarity overlays as a complementary metric to LLM-likelihood (the user's 'pure word rarity' axis). NOT model-based — corpus-frequency based. Cover: wordfreq Python package; Zipf-frequency tools; Google Books Ngram Viewer; COCA/SUBTLEX/OEC word lists; lexical-sophistication / readability tools (TAALES, Coh-Metrix, Lexile, Flesch-Kincaid); ESL vocabulary-difficulty visualizers (CEFR-J Wordlist, English Vocabulary Profile); KWIC / concordance tools (Voyant, AntConc); stylometric tools (JGAAP, Stylo R package). Distinguish corpus-frequency from LLM-likelihood — they are NOT the same signal and the difference is informative (an LLM-likely word can be corpus-rare and vice versa). Output: tool inventory + the conceptual distinction between the two axes for the research doc.
