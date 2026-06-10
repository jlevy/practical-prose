---
type: is
id: is-01ktqhdsh5z3rc6xbznfmza3p7
title: "CLI: multi-document eval render (responsive side-by-side cards)"
kind: feature
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-06-10T01:12:54.052Z
updated_at: 2026-06-10T01:12:54.052Z
---
Deferred from the README screenshot work. Add a mode to 'pprose render' (or a new subcommand) that takes multiple .eval.md reports and emits one HTML page laying the cards out in a responsive grid that wraps/sits side-by-side by viewport. Touches render_html cli.py, renderer.py, templates, CSS. Would replace the current 'magick +append' composite for true side-by-side output.
