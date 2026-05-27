---
type: is
id: is-01kshmtgzfyr2ngrg267zgd9p8
title: Update eval_report.py and eval_compare.py for renamed fields
kind: task
status: closed
priority: 1
version: 3
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshmth7p8t647kk3y1qp3agx
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:01:08.590Z
updated_at: 2026-05-27T00:00:53.236Z
closed_at: 2026-05-27T00:00:53.233Z
close_reason: "Superseded by spec rewrite 2026-05-26 (v3). New architecture: chopdiff v0.4.x parses each block once and exposes typed accessors (heading_level, code_language, list_info, table_info, inlines, section_tree). Pprose becomes a thin serializer with no marko import and no per-block re-parse. Replaced by a fresh bead set."
---
In tools/pprose/src/pprose/eval_report.py: SizeBlock pydantic model (~line 86-87) currently has 'sentences', 'paragraphs' fields; rename to sentence_count, paragraph_count. Density math (~line 635-642) reads metrics.sentences / .paragraphs / .words; switch to .sentence_count / .paragraph_count / .word_count. In tools/pprose/src/pprose/eval_compare.py: column lambdas at ~line 120-274 reference r.quant.size.sentences, .paragraphs, and the derived density block — update field accesses to the new names. Run 'pprose report' and 'pprose compare' on a fixture to verify output renders correctly.
