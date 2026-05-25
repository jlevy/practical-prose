---
type: is
id: is-01kseg7gwbvvrq6671047kkxxd
title: "Design-system: use atomic file writes in generate.py"
kind: task
status: open
priority: 3
version: 1
labels:
  - design-system
dependencies: []
created_at: 2026-05-25T02:43:08.298Z
updated_at: 2026-05-25T02:43:08.298Z
---
Replace Path.write_text with strif's atomic_output_file (per python-modern-guidelines) so a Ctrl-C mid-write never leaves a partial generated file on disk.  Add strif to the script's PEP 723 inline deps.

Currently low-impact because the generator runs locally and is fast, but adopting the convention is cheap.
