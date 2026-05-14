---
type: is
id: is-01krfgeda76zvvdk9zbftcm2vf
title: Fix 4 pre-existing chopdiff fixture-drift failures in test_metrics.py::TestB14_ReproducibilityRegression
kind: bug
status: closed
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md
labels: []
dependencies: []
parent_id: is-01krfgdgghp4x3rtpyk0kd4r1n
created_at: 2026-05-13T01:50:26.630Z
updated_at: 2026-05-13T02:11:33.014Z
closed_at: 2026-05-13T02:11:33.009Z
close_reason: Regenerated the 4 pinned expected JSON fixtures (all_headings, links_mixed, frontmatter_and_code, banned_register) via 'prose-metrics <fixture>.md --json'. Pre-existing drift came from chopdiff emitting new fields (em_dash_density, generic_heading_*, pedantic_marker_*, replacement_history_*). All 150 tests now pass.
---
4 tests fail with 'Left contains 9 more items: em_dash_density_per_1000_words, em_dashes_total, generic_heading_examples, generic_heading_hits, ...'. The metrics module emits these fields (likely from a chopdiff upgrade) but the pinned expected JSON under tests/test_fixtures/practical_prose_metrics/expected/ doesn't include them. Either: (a) regenerate the expected JSON via the regen command in tests/test_metrics.py:348-351 if the new fields are intentional, or (b) pin chopdiff to a version that doesn't include them. These failures predate Phase 0 — they fail identically against the original scripts/ location.
