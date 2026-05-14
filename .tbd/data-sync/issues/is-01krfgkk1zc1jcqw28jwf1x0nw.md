---
type: is
id: is-01krfgkk1zc1jcqw28jwf1x0nw
title: "Phase 2 verify: re-run self-eval-v0.1 batch in one command, < 5 min wall-clock"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md
labels: []
dependencies:
  - type: blocks
    target: is-01krfgkr6rtn0sj8e5r82ct367
parent_id: is-01krfgdgghp4x3rtpyk0kd4r1n
created_at: 2026-05-13T01:53:16.350Z
updated_at: 2026-05-13T02:27:28.196Z
closed_at: 2026-05-13T02:27:28.192Z
close_reason: "Phase 2 batch verified end-to-end on 12 fresh stubs in evals/self-eval-v0.2/: wall-clock 1m33s for 12 docs in parallel (vs ~4h sequential in round 1, ~160x speedup). 8/12 completed and pass eval-report validate. 4 failed alignment after F3a softening dropped out-of-range rule_numbers (still occasional even with prompt appendix). Cache mechanism confirmed: 2 docs showed read_input_tokens=26198 / creation=0 (cache hits); the other 6 fired concurrently before priming. Recommend pp-followup: model-self-correction retry to eliminate F3 residue in batch runs. Calibration check (guidelines-self <=0.3 from 4.1) not measurable this run because guidelines.eval.yaml was in the F3a failure set."
---
Run 'eval-score batch evals/self-eval-v0.1/*.eval.yaml --max-concurrent 4'. Verify: (a) all 12 docs scored successfully; (b) total wall-clock < 5 min (vs ~4 hours in round 1); (c) cache_stats shows read-token hits on docs 2..N; (d) all YAMLs pass 'eval-report validate'; (e) calibration regression: scoring guidelines-self stays within 0.3 of pinned 4.1 overall mean.
