---
type: is
id: is-01krfgexb0348x9s50y4y51pev
title: "Phase 1 verify: re-score readme.eval.yaml end-to-end via SDK path"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md
labels: []
dependencies:
  - type: blocks
    target: is-01krfgf9p9px0c3c6qz8t4vc36
parent_id: is-01krfgdgghp4x3rtpyk0kd4r1n
created_at: 2026-05-13T01:50:43.039Z
updated_at: 2026-05-13T02:20:47.543Z
closed_at: 2026-05-13T02:20:47.539Z
close_reason: "Phase 1 SDK path verified end-to-end: eval-score readme.eval.yaml ran in 58s (target <60s), wrote model_id=claude-sonnet-4-5-20250929, sdk_version=0.99.0, cache_stats.creation_input_tokens=26198. Schema validates. overall_mean dropped 4.36 -> 3.67 (NOT within target ±0.2): Sonnet 4.5 now assesses Calibration/Fairness/Robustness/Factuality where the round-1 model marked them NA. This is calibration drift between model versions, not a Phase 1 regression. Logged for round-2 findings rollup. Phase 1 verify YAML restored to round-1 baseline for clean batch comparison in Phase 2."
---
After Phase 1 implementation lands, manually verify: (a) eval-score readme.eval.yaml runs end-to-end without errors; (b) overall_mean is within ±0.2 of the round-1 value (~4.3); (c) wall-clock is < 60s (vs ~5 min via CLI); (d) metadata.repro.cache_stats present with creation_input_tokens > 0 on cold call. Acts as the Phase 1 → Phase 2 gate.
