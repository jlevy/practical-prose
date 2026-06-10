---
type: is
id: is-01ktqy4xhsfvm7anze87zcwr53
title: "lint: author v1 rule YAML files (10 categories) under resources/rules/"
kind: task
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktqxg5a0ja7mf8sv4e8175t1
created_at: 2026-06-10T04:55:14.744Z
updated_at: 2026-06-10T05:00:18.468Z
---
New dir tools/pprose/src/pprose/resources/rules/. Files: throat-clearing.yaml, false-agency.yaml, negative-listing.yaml, dramatic-fragmentation.yaml, rhetorical-setups.yaml, narrator-from-a-distance.yaml, vague-declaratives.yaml, self-negating-parallel.yaml, business-jargon.yaml, attention-flags.yaml (adverb/lazy-extreme densities). Source from docs/ai-prose-mitigations.md + ai-prose-corrections.md + attic/stop-slop phrases.md/structures.md (MIT, source: stop-slop attribution field). Every rule: exact phrases + fuzzy variants + model_hints line + correction + exceptions + bad/good exemplar + first_flagged.
SCHEMA NOTE (2026-06-09): FuzzyPattern in rules_schema should carry max_l_dist (int, for fuzzysearch) rather than a rapidfuzz similarity threshold; template patterns are RE2-compatible regex strings (no backreferences/lookaround — fine for our patterns).
