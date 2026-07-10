---
type: is
id: is-01kx52wnamngff125vtzq6crv4
title: Restrict OIDC publishing to validated release tags
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:59:38.323Z
updated_at: 2026-07-10T04:48:05.443Z
closed_at: 2026-07-10T04:48:05.442Z
close_reason: Manual arbitrary-ref publishing was removed; release tags are validated and OIDC job actions are SHA-pinned.
---
PR #31, publish.yml: workflow_dispatch skips the version guard and can publish an arbitrary selected ref; github.ref_name is directly interpolated into shell; OIDC steps use mutable action tags. Remove or strictly gate manual publishing, pass tag via env, and SHA-pin publish actions.
