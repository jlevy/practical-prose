---
type: is
id: is-01kx3zk73tce1g8jvxykc74myw
title: Decide and apply a frontmatter policy for the repo's own docs
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-07-09T17:42:48.697Z
updated_at: 2026-07-09T18:39:07.341Z
closed_at: 2026-07-09T18:39:07.341Z
close_reason: "Resolved on review branch: required four fields added to all reference docs, shortcuts, runbooks (dates from first git commit); repo-root operational files exempted via a scope note in practical-prose-metrics.md §Recommended Frontmatter Schema."
---
practical-prose-metrics.md declares title/description/date/status as Required, but the repo's own docs sit in three tiers: none (guidelines, principles, common-doc, bibliography, writing-practical-guides, ai-prose-corrections, README), partial title/description/category/author (all shortcuts, authoring-principles), and full (rubric, metrics, runbooks). Two metadata conventions coexist (YAML frontmatter vs the 'Version: v0.x' line). Either adopt the minimum four fields on all durable docs or scope the schema explicitly to evaluated artifacts; reconcile the version-line convention either way. From review-2026-07-09.
