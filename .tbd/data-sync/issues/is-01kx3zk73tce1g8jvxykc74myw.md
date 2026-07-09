---
type: is
id: is-01kx3zk73tce1g8jvxykc74myw
title: Decide and apply a frontmatter policy for the repo's own docs
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-07-09T17:42:48.697Z
updated_at: 2026-07-09T17:42:48.697Z
---
practical-prose-metrics.md declares title/description/date/status as Required, but the repo's own docs sit in three tiers: none (guidelines, principles, common-doc, bibliography, writing-practical-guides, ai-prose-corrections, README), partial title/description/category/author (all shortcuts, authoring-principles), and full (rubric, metrics, runbooks). Two metadata conventions coexist (YAML frontmatter vs the 'Version: v0.x' line). Either adopt the minimum four fields on all durable docs or scope the schema explicitly to evaluated artifacts; reconcile the version-line convention either way. From review-2026-07-09.
