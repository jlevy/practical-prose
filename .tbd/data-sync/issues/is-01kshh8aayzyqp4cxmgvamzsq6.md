---
type: is
id: is-01kshh8aayzyqp4cxmgvamzsq6
title: Update eval_report.py and eval_compare.py for new field names
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshh8k0tzbbehs802szk9vwy
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T06:58:46.212Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-05-26T08:00:23.311Z
close_reason: "Superseded by spec rewrite 2026-05-26: pprose now depends on chopdiff BlockDoc (jlevy/chopdiff#8). Replaced by a slimmer pprose-only bead set under the same epic pp-3hg4."
---
In tools/pprose/src/pprose/eval_report.py: the density calculations (words_per_sentence, words_per_paragraph, sentences_per_paragraph at lines ~635-642) currently read metrics.sentences / .paragraphs / .words. Switch to .sentence_count / .paragraph_count / .word_count. Also update the SizeBlock pydantic model field names (lines ~86-87 reference 'sentences', 'paragraphs') and any other field accesses. In tools/pprose/src/pprose/eval_compare.py: column lambdas at lines ~120-274 reference r.quant.size.sentences, .paragraphs, and the derived density block — update field accesses to the new names. Run 'pprose report' and 'pprose compare' on a fixture to verify output renders correctly.
