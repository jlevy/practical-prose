---
type: is
id: is-01krw2kwyemv5gswppedwfpqn4
title: Add repeat, multi-target, and concurrent run executor
kind: task
status: open
priority: 2
version: 6
spec_path: null
labels: []
dependencies:
  - type: blocks
    target: is-01krw2m12xa8r5qp2zcmmfqv2b
parent_id: is-01krvxewx2bjm707fh941e3dvk
created_at: 2026-05-17T22:58:54.030Z
updated_at: 2026-06-13T18:38:36.314Z
---
Add repeated --target and --repeat expansion for scoring one eval report across targets x repeat. Reuse the existing gather_limited() helper and --max-concurrent naming for bounded in-flight provider calls. Preserve current --batch multi-file behavior and define clear errors for unsupported combinations.
