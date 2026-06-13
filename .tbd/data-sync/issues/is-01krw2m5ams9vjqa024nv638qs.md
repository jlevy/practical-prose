---
type: is
id: is-01krw2m5ams9vjqa024nv638qs
title: Tighten eval validation for source-check claims
kind: task
status: open
priority: 2
version: 6
spec_path: null
labels: []
dependencies:
  - type: blocks
    target: is-01krw2m9zbx7t5eatwh9k4je11
parent_id: is-01krvxewx2bjm707fh941e3dvk
created_at: 2026-05-17T22:59:02.611Z
updated_at: 2026-06-13T18:38:36.681Z
---
Extend pprose prompt capability text and report validation so closed-world runs cannot claim external corroboration. Warn or fail on phrases such as spot-checked, URLs resolve, followed links, externally corroborated, or confirmed by source lookup when no source-check tool or evidence manifest ran. Require provider tool-use or manifest evidence for corroboration claims.
