---
type: is
id: is-01kxxwk91343bhxrb5hrxzxckf
title: Align install.py agents-md block template with root AGENTS.md edit-ladder sentence
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-07-19T19:10:40.162Z
updated_at: 2026-07-19T19:10:40.162Z
---
pprose install --project rewrites the repo AGENTS.md pprose block without the hand-authored sentence 'Reserve the deeper pprose-copy-edit and pprose-full-edit passes (both include de-slop) for when a fuller edit is asked for' (added in #34). Either add the sentence to the generated agents-md block template in install.py (with test updates) or move it outside the managed block, so reconcile runs stop dropping owner-authored policy text. Found during v0.3.0 release prep.
