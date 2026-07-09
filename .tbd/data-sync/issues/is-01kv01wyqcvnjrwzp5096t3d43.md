---
type: is
id: is-01kv01wyqcvnjrwzp5096t3d43
title: Remove metrics regex workarounds; swap to flexdoc 0.1.0 typed API
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/done/plan-2026-06-13-metrics-flexdoc-workaround-removal.md
labels: []
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-06-13T08:34:43.563Z
updated_at: 2026-06-14T02:16:04.770Z
closed_at: 2026-06-14T02:13:59.384Z
close_reason: "Done: metrics.py swapped structural-count + link-form regexes for flexdoc 0.2.0 typed APIs (heading_level, link_form, images(), typed footnotes/tables/code) and editorial lint onto prose_text(); size path preserved byte-identical. Fixtures re-blessed (footnote double-count 6->3; links_mixed bare_urls 2->0). 326 tests + basedpyright + lint green; 0 crashes over 150 docs."
---
Behavior-preserving rewrite of measure() in metrics.py around a single FlexDoc. Replace structural regexes (headings ATX+setext, images, inline code, footnote refs/defs, tables, code fences, frontmatter strip) with flexdoc typed APIs; feed editorial lint regexes the flexdoc prose-only filtered(...).reassemble() text; move generic-heading check onto heading_title(). Keep link-form, classify_url, and lint regexes. Re-bless fixtures only for intentional changes (footnote double-count fix -> correct count; setext phantom-HR edge). TestB14 size counts must not drift. Update docstring (Known Limitations, recursive=True gotcha).
