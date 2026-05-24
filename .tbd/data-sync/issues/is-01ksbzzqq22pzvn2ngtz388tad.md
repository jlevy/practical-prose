---
type: is
id: is-01ksbzzqq22pzvn2ngtz388tad
title: "Prompt: rewrite eval-rubric-score.md to distinguish ERR (scorer failure) from NA (dim doesn't engage)"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01ksbzxycfj95nzb0mexrshpp6
created_at: 2026-05-24T03:20:47.074Z
updated_at: 2026-05-24T03:20:47.074Z
---
tools/pprose/src/pprose/prompts/eval-rubric-score.md: in step 2 (line ~20), describe 1-5 + NA + ERR explicitly. In step 4 (~33), 'For every dimension scored 5, ERR, or NA, do not cite any violation.' In the hard requirements (~51-60), 'integer 1-5 or the literal string NA or ERR.' Add a one-line guard so the scorer doesn't reach for ERR when 1 + a rule cite would be honest.
