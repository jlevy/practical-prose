---
type: is
id: is-01kt5ngj8xp71rrd56s9yj5r0k
title: "Repo org: single specs home; gitignore/remove attic + loose root drafts"
kind: task
status: closed
priority: 3
version: 2
spec_path: docs/project/release-readiness-2026-06.md
labels:
  - release
  - org
dependencies: []
parent_id: is-01kt5nebv6vqtrx17dfy0hy04m
created_at: 2026-06-03T02:37:59.453Z
updated_at: 2026-06-11T16:24:57.012Z
closed_at: 2026-06-11T16:24:57.011Z
close_reason: Specs consolidated to the single docs/project/specs/{active,done} home (legacy tools/docs tree removed; 05-12 and 05-13 archived as implemented, 05-25 moved to active with precondition met); bead spec_paths re-pointed (pp-mpo1, pp-flf2, pp-3hg4) and pp-h780's ghost spec_path cleared; attic/ already gitignored and now documented in agents-internal-guide as reference checkouts; loose root drafts all committed. Ghost links fixed in design-system.md; release-readiness item marked resolved.
---
Risk #16. Project specs live in TWO places (docs/project/specs/active and tools/docs/project/specs/active) — pick one home. attic/ vendors full copies (chopdiff/flowmark/simple-modern-uv/leximetry) and research-archive/ is large; loose drafts sit at the repo root (e.g. thinkingclearlyinwriting.md). Decide what should not ship in a first-release snapshot and gitignore or remove it. NOTE: the JS-tooling-into-tools move was deliberately deferred (lefthook hook discovery) — see PR #19 / risk #16 in the spec.
