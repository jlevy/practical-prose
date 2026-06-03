---
type: is
id: is-01kt7ehpz8mfmpb8byqdf68wdw
title: "Phase 2: new command surface (eval / report / show / validate) + cli.py rewrite"
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-06-03-reporting-cli-redesign.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt7ehqb20vghneke0y28xj58
parent_id: is-01kt7eh75j40zhgrbbkrrv6kc9
created_at: 2026-06-03T19:14:45.863Z
updated_at: 2026-06-03T19:15:11.337Z
---
New eval command (metrics+score+rollups → .eval.md; carries over score/from-metrics options; --no-score, --output/-, --report, --open composition). New report command (--format md,html,yaml,json + all; --detail standard; output-location rule: stdout / single file / multi-format dir). New show command (open artifact; render .eval.md to HTML via report first). New top-level validate (schema+alignment+--complete; --recompute rewrites derived+body). Rewrite cli.py COMMANDS/groups; remove report subcommands, score, render, score --render-html; realign metrics/compare flags to long-only --output + shared --format.
