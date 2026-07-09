---
type: is
id: is-01kx3zkbdw8sh1f1zrahz2erv0
title: Self-lint CI baseline for the repo's own docs
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-07-09T17:42:53.116Z
updated_at: 2026-07-09T17:42:53.116Z
---
Institutionalize self-application: run pprose metrics over docs/, shortcuts/, runbooks/, README.md in CI and compare against committed expected-hit baselines (mention-vs-use hits are expected; new regressions fail). Would have caught the rubric's generic 'Notes' heading and the British-spelling drift found in review-2026-07-09. Cheap, deterministic, very on-brand.
