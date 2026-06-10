---
type: is
id: is-01krhz27s9axj15pcwy0ccpt2d
title: Prepare first pprose PyPI release
kind: task
status: open
priority: 1
version: 6
spec_path: tools/docs/project/specs/active/plan-2026-05-13-cross-agent-skills.md
labels:
  - cross-agent-skills
  - release
dependencies:
  - type: blocks
    target: is-01krhz2f5wsv5rwkvzz2c6mbaq
parent_id: is-01krhz0ckjzn0s26wggjjfays1
created_at: 2026-05-14T00:44:25.257Z
updated_at: 2026-06-10T00:47:37.394Z
---
Cut the first prose-eval package release after the unified CLI entry point is tested, so uvx prose-eval ... resolves without --from. If the PyPI package name changes, keep the package and console script names aligned so uvx <name> ... remains self-documenting.

## Notes

Package renamed prose-eval → practical-prose → pprose. Local release prep complete.

Pin-correctness guard added in PR #27 (devtools/check_release_version.py + a publish.yml step): the publish fails unless the release tag == DISCOVERY_VERSION, so the committed `uvx pprose@<pin>` discovery skills always resolve to a real published version (this and future releases). Both former blockers (pp-p51y, pp-z00k) are closed, so this gate is unblocked.

Remaining EXTERNAL steps (need explicit user approval — not done by the agent):
1. Merge PR #27 (release hardening) to main.
2. Register the PyPI trusted publisher for `pprose` (pending-publisher; one-time, on PyPI).
3. `gh release create v0.1.0` — tags and triggers publish.yml (OIDC trusted publishing).
DISCOVERY_VERSION is already 0.1.0, so the new guard passes for v0.1.0.

Refs: docs/project/release-readiness-2026-06.md (2026-06-09 status update); e2e-testing.runbook.md Phase E (post-publish smoke).
