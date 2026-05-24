---
type: is
id: is-01ksbzzr4f9kxys44jrw3esyz3
title: "Resource sync: regenerate bundled copies of the rubric and prompt under tools/pprose/src/pprose/resources/"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01ksbzxycfj95nzb0mexrshpp6
created_at: 2026-05-24T03:20:47.502Z
updated_at: 2026-05-24T03:20:47.502Z
---
tools/pprose/src/pprose/resources/guidelines/practical-prose-rubric.md (and any other resource files mirrored from docs/, shortcuts/, runbooks/) must be re-synced after the rubric edits. Use devtools/sync_resources.py if present (per the codespell skip note in pyproject.toml). Verify the wheel will ship the updated text.
