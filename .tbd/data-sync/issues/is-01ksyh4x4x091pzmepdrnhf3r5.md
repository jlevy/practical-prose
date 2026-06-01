---
type: is
id: is-01ksyh4x4x091pzmepdrnhf3r5
title: Bundling additions and removal in sync_resources.py
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-05-30-pprose-install-scopes-and-surfaces.md
labels: []
dependencies:
  - type: blocks
    target: is-01ksyh4xcc5rpsrs84cwfqg0p0
  - type: blocks
    target: is-01ksyh4y5d5zpdp8rv6tk5g5k4
parent_id: is-01ksyh41ve1a731ww85kxnh54k
created_at: 2026-05-31T08:07:02.044Z
updated_at: 2026-05-31T08:10:04.161Z
closed_at: 2026-05-31T08:10:04.154Z
close_reason: sync_resources adds design-system.md + README.md (about category); /docs/development.md naturally unbundled (moved to /docs/project/). pprose guidelines lists 9 docs including new bundled ones.
---
Add design-system.md from tools/design-system/ into the bundled guidelines plan. Add README.md as a new bundled category 'about' (one doc; loader special case). Verify /docs/development.md is no longer bundled (file is now under /docs/project/, excluded by non-recursive glob). Run devtools/sync_resources.py; the drift test should pass.
