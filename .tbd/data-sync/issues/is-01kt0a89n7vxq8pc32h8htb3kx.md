---
type: is
id: is-01kt0a89n7vxq8pc32h8htb3kx
title: "Spec: Static HTML eval report (Visual 9B)"
kind: epic
status: open
priority: 2
version: 12
spec_path: docs/project/specs/done/plan-2026-05-29-static-html-eval-report.md
labels: []
dependencies: []
child_order_hints:
  - is-01kt0a8me8bzsyc6ahsredycc6
  - is-01kt0a8rz8b6tmkf8m5hwtj1m5
  - is-01kt0a8xtz8w43sm00sjkqzank
  - is-01kt0a92st5e3r1p2k9188sx6p
  - is-01kt0a988swdskqf2dxkgb5pza
  - is-01kt0a9bqdn8nnp9qakxr61fh8
  - is-01kt0a9gsq6batsb6vb0mcf3k0
  - is-01kt0a9nd0xknbge25v7hz56aw
  - is-01kt0a9shf12zsdj7racajn2n7
  - is-01kt0a9x5m907a3gz0sxtbhft1
created_at: 2026-06-01T00:45:01.985Z
updated_at: 2026-06-13T18:38:35.589Z
---
Ship a clean, shareable, print-friendly static HTML rendering of a Practical Prose eval, extracted from Visual 9B. Two workflows: end-to-end via 'pprose score --render-html' and standalone via 'pprose render <eval.md>'. Renderer is a single primitive in tools/pprose/src/pprose/render_html/, input-aware via a dispatch table so future kinds (plain docs, advanced eval w/ embedded source) plug in without CLI churn. See spec for the full design.
