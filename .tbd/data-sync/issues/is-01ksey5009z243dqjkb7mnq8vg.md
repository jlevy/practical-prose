---
type: is
id: is-01ksey5009z243dqjkb7mnq8vg
title: Update hand-ordered design-system schema/enums
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01ksey4hc3txw0a3f13445ahrm
created_at: 2026-05-25T06:46:25.544Z
updated_at: 2026-05-25T06:56:12.902Z
closed_at: 2026-05-25T06:56:12.898Z
close_reason: Updated GroupId Literal/enum and dimension id regex character class to PEFRGJ order in tools/design-system/schema.py and tools/design-system/lib/design-system.js (regex semantics unchanged).
---
The design-system schema files contain hand-ordered GroupId enums and id regexes that should match the new canonical order for readability (the regex character class semantics are unchanged):
- tools/design-system/schema.py:35 — GroupId = Literal["P", "E", "F", "G", "R", "J"] → Literal["P", "E", "F", "R", "G", "J"]
- tools/design-system/schema.py:143-144 — regex /^[PEFGRJ]\\d+$/ → /^[PEFRGJ]\\d+$/
- tools/design-system/lib/design-system.js:46 — z.enum(["P", "E", "F", "G", "R", "J"])
- tools/design-system/lib/design-system.js:67 — same regex
