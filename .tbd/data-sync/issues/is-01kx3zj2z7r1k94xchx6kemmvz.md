---
type: is
id: is-01kx3zj2z7r1k94xchx6kemmvz
title: Cut the pending v0.2.0 release (or re-pin skill fallbacks)
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-07-09T17:42:11.686Z
updated_at: 2026-07-09T17:42:11.686Z
---
pprose 0.2.0 is not on PyPI (latest: 0.1.1) but AGENTS.md and all committed SKILL.md discovery copies fall back to 'uvx pprose@0.2.0', which fails for anyone without a local install. Release pending since 2026-06-13 (PR #28). Either tag/publish v0.2.0 (publish.yml + check_release_version guard exist) or re-pin the committed discovery copies to a published version. From review-2026-07-09-comprehensive-project-review.
