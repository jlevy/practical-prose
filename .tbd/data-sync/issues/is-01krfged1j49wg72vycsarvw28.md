---
type: is
id: is-01krfged1j49wg72vycsarvw28
title: Update runbooks to call new entry points (eval-score, eval-report, eval-compare, prose-metrics)
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md
labels: []
dependencies: []
parent_id: is-01krfgdgghp4x3rtpyk0kd4r1n
created_at: 2026-05-13T01:50:26.353Z
updated_at: 2026-05-13T02:10:44.585Z
closed_at: 2026-05-13T02:10:44.581Z
close_reason: Both runbooks updated to use eval-score / eval-report / eval-compare / prose-metrics console scripts. Added Setup sections covering 'cd tools/prose-eval && make install', ANTHROPIC_API_KEY via .env / .env.local, and the evals/<round>/ convention. Pre-emptively documented the --batch flag (lands in Phase 2 / pp-moj6). Fixture-path references updated to ../tools/prose-eval/tests/fixtures/.
---
runbooks/practical-prose-eval-single.runbook.md and runbooks/practical-prose-eval-compare.runbook.md still reference '../scripts/eval_score.py' / '../scripts/eval_report.py' / '../scripts/eval_compare.py'. After Phase 0 these are installed as console scripts. Replace command examples to use the new names (e.g. 'eval-score artifact.eval.yaml --model sonnet'). Note the working-directory assumption changes: the package is installed once via 'cd tools/prose-eval && make install', then commands run from anywhere with the venv active.
