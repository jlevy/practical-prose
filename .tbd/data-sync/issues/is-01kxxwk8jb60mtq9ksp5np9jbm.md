---
type: is
id: is-01kxxwk8jb60mtq9ksp5np9jbm
title: "Release pprose v0.3.0: prep, publish, post-verify"
kind: chore
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-07-19T19:10:39.690Z
updated_at: 2026-07-19T19:14:37.704Z
closed_at: 2026-07-19T19:14:37.704Z
close_reason: "v0.3.0 released: PR #35 merged (28ddd1f), tag v0.3.0, publish.yml run 29700171302 green, PyPI verified (uvx pprose@0.3.0 --version + fresh scratch install, pins=0.3.0, 7 skills incl. de-slop)"
---
Cut v0.3.0 (feats #33/#34: cross-agent skill profiles, de-slop skill). Prep on claude/tbd-upgrade-v0.4.1-o70gm6: CHANGELOG 0.3.0, DISCOVERY_VERSION bump + regenerated skills/mirrors, upgrade-path docs (verified live 0.2.0->0.3.0 scratch upgrade), e2e note refresh. Then: PR, CI green, squash-merge, gh release v0.3.0 (triggers publish.yml -> PyPI), verify uvx pprose@0.3.0.
