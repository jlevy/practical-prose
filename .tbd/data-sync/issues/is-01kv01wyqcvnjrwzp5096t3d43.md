---
type: is
id: is-01kv01wyqcvnjrwzp5096t3d43
title: Remove metrics regex workarounds; swap to flexdoc 0.1.0 typed API
kind: task
status: blocked
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-06-13-metrics-flexdoc-workaround-removal.md
labels: []
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-06-13T08:34:43.563Z
updated_at: 2026-06-13T08:44:55.110Z
---
Behavior-preserving rewrite of measure() in metrics.py around a single FlexDoc. Replace structural regexes (headings ATX+setext, images, inline code, footnote refs/defs, tables, code fences, frontmatter strip) with flexdoc typed APIs; feed editorial lint regexes the flexdoc prose-only filtered(...).reassemble() text; move generic-heading check onto heading_title(). Keep link-form, classify_url, and lint regexes. Re-bless fixtures only for intentional changes (footnote double-count fix -> correct count; setext phantom-HR edge). TestB14 size counts must not drift. Update docstring (Known Limitations, recursive=True gotcha).
