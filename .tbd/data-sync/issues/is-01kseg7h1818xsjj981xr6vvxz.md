---
type: is
id: is-01kseg7h1818xsjj981xr6vvxz
title: "Design-system: pin Zod locally instead of esm.sh CDN"
kind: task
status: open
priority: 2
version: 1
labels:
  - design-system
  - supply-chain
dependencies: []
created_at: 2026-05-25T02:43:08.455Z
updated_at: 2026-05-25T02:43:08.455Z
---
tools/design-system/lib/design-system.js imports Zod from 'https://esm.sh/zod@3.23.8'.  This is a runtime CDN dependency: supply-chain risk + offline-fragile.  Options:
1. Vendor a copy of Zod under tools/design-system/lib/vendor/ (bundle via esbuild at generate time, then commit).
2. Drop Zod validation at runtime; rely solely on the Python-side Pydantic validation at generate time.  The hand-written design-system.js becomes a typed re-export.  Faster + smaller; loses the defensive re-validation on hand-edited generated files.

Per the supply-chain hardening guideline (14-day rule + audit), favor option 1 if we keep Zod, otherwise option 2.
