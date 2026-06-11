---
type: is
id: is-01ktr5c579rk5z365t9eaax1ea
title: Surface writing-practical-guides through skills + document the skill upgrade path
kind: epic
status: closed
priority: 1
version: 5
labels: []
dependencies: []
child_order_hints:
  - is-01ktr5csj7ca1e81c3q0tf8z3e
  - is-01ktr5ct196qr9az4gs35a1167
  - is-01ktr5ct9yhxvyw18mnhdaqgjj
created_at: 2026-06-10T07:01:31.999Z
updated_at: 2026-06-11T16:24:56.807Z
closed_at: 2026-06-11T16:24:56.806Z
close_reason: "Epic complete: pp-uvct (skill genre routing), pp-6f74 (upgrade-path docs), pp-ew5z (v0.1.1 release) all closed."
---
From the skill/CLI clarity review (2026-06-10): the new genre doc writing-practical-guides.md is bundled and listed by 'pprose guidelines --list', but (1) no skill routes to it — the edit/review/eval skills name their guidelines statically, so an agent editing a guide never consults the genre supplement; (2) the upgrade chain is implied, never stated — installed skills bake a version pin (uvx pprose@<ver>), so new guidelines are invisible in installed repos until pprose is upgraded AND 'pprose install' is re-run (which bumps the pin). Fix both, ship in v0.1.1.
