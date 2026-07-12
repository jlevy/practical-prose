---
type: is
id: is-01kxbyvvq7vxftat8j8asbm2e8
title: Audit v0.2.0 release readiness and upgrade tbd integration to v0.4.0
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies: []
created_at: 2026-07-12T20:03:58.822Z
updated_at: 2026-07-12T20:29:09.792Z
closed_at: 2026-07-12T20:29:09.792Z
close_reason: Released pprose v0.2.0 from merged commit 2fc2b85 after green PR/main CI; upgraded tbd integration to 0.4.0 and flexdoc to 0.3.0, hardened the release process, and verified the published PyPI/uvx/scratch-install path.
---

## Notes

Completed 2026-07-12. Upgraded global get-tbd and repository integrations to 0.4.0 under the confirmed first-party exemption; tbd doctor reports healthy and repeated setup is diff-idempotent. Release audit evidence: last release v0.1.1; origin/main ca7d955; CI green; local lint-check + 338 tests + version guard + constrained build green. Process/readiness findings recorded in pp-jcou and pp-vyc5.
