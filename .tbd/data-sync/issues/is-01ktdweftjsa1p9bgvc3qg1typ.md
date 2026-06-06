---
type: is
id: is-01ktdweftjsa1p9bgvc3qg1typ
title: "Scoring reliability: run-to-run variance + stubborn Breadth alignment miss"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01ktdvk2r21qw63cg34kvas59d
created_at: 2026-06-06T07:13:06.897Z
updated_at: 2026-06-06T07:13:06.897Z
---
Discovered during the calibration pass (pp-zk05). Two residual issues with single-shot Opus scoring:
1) Run-to-run variance: re-scoring the same document with the same prompt shifted ~6 Bush dimensions by ±1 (overall_mean 3.5 -> 3.25 across runs). Consider multi-sample/ensemble scoring, lower temperature, or reporting a confidence/range.
2) Stubborn alignment miss: even after the pp-ps1u prompt fix (which cut misses 11->1), the scorer repeatedly assigns Breadth=4 without emitting a matching rule_finding, forcing --allow-misaligned. Consider an auto-retry on alignment failure, or prompt guidance for citing the 4-anchor 'one case class missing' slip explicitly.
