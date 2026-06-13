---
type: is
id: is-01krw2kq1dqn3gd49waqcfccag
title: Implement binary source-check modes
kind: task
status: open
priority: 2
version: 6
spec_path: null
labels: []
dependencies:
  - type: blocks
    target: is-01krw2m5ams9vjqa024nv638qs
parent_id: is-01krvxewx2bjm707fh941e3dvk
created_at: 2026-05-17T22:58:47.980Z
updated_at: 2026-06-13T18:38:36.131Z
---
Implement source_check.mode none|web|manifest for pprose. Start with closed-world metadata by default: mode=none and external_validation_performed=false. For manifest mode, add local evidence context without network tools. For web mode, add provider web-search tools only through adapters. Do not expose allowed/blocked domain controls.
