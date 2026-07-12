---
type: is
id: is-01kx3zj2z7r1k94xchx6kemmvz
title: Cut the pending v0.2.0 release (or re-pin skill fallbacks)
kind: task
status: closed
priority: 1
version: 4
labels: []
dependencies: []
created_at: 2026-07-09T17:42:11.686Z
updated_at: 2026-07-12T20:29:09.768Z
closed_at: 2026-07-12T20:29:09.767Z
close_reason: Released pprose v0.2.0 from merged commit 2fc2b85 after green PR/main CI; upgraded tbd integration to 0.4.0 and flexdoc to 0.3.0, hardened the release process, and verified the published PyPI/uvx/scratch-install path.
---
pprose 0.2.0 is not on PyPI (latest: 0.1.1) but AGENTS.md and all committed SKILL.md discovery copies fall back to 'uvx pprose@0.2.0', which fails for anyone without a local install. Release pending since 2026-06-13 (PR #28). Either tag/publish v0.2.0 (publish.yml + check_release_version guard exist) or re-pin the committed discovery copies to a published version. From review-2026-07-09-comprehensive-project-review.

## Notes

2026-07-12 release audit: origin/main ca7d955 is technically buildable. Latest main CI passed (Python 3.11-3.14, root lint, wheel smoke); isolated local run passed make lint-check, 338 tests, check_release_version.py v0.2.0, and constrained sdist/wheel build. PyPI still serves 0.1.1 and DISCOVERY_VERSION/committed skills pin 0.2.0, so publishing resolves the current broken fallback. Before cutting: use the actual origin/main release commit, update the CHANGELOG 0.2.0 date to the publish date, and decide/sign off the documented manual browser/provider/install checks plus stale self-eval baselines. Release-guide hazards are tracked in pp-vyc5.
