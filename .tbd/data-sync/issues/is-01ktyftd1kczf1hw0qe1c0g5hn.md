---
type: is
id: is-01ktyftd1kczf1hw0qe1c0g5hn
title: Decide frontmatter adoption for core docs/ reference files
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-06-12T17:59:31.122Z
updated_at: 2026-06-12T17:59:31.122Z
---
practical-prose-metrics.md defines a Required frontmatter schema (title, description, date, status), and the repo self-evals score guidelines/rubric/bibliography as artifacts, but practical-prose-guidelines.md, practical-prose-principles.md, practical-prose-bibliography.md, writing-practical-guides.md, ai-prose-corrections.md, and common-doc-guidelines.md carry only a Version: line and no frontmatter. Either adopt the minimum schema in those docs (affects eval baselines and the frontmatter-presence metric) or scope the metrics recommendation to evaluated artifacts only. Found during 2026-06-12 docs conformance review.
