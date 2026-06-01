---
type: is
id: is-01kt0wbjcdtg8pyezcwrkhk69j
title: "Spec: Shared render components — single source of truth"
kind: epic
status: open
priority: 2
version: 15
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies: []
child_order_hints:
  - is-01kt0wbtdd2fnj2qfb70jv59je
  - is-01kt0wbzv8hc39vy2t8ztxd5cx
  - is-01kt0wc4fnqsdbg2xz75xa7fs8
  - is-01kt0wc871tfh3b6qgqqrrpdej
  - is-01kt0wcd4svat9pjsedtzm3nff
  - is-01kt0wcj8vnf5gk2c92fqzadvr
  - is-01kt0wcr3c1tsrzp9e34fzv2eg
  - is-01kt0wcy0gvgwmr7pxyx9qh0f9
  - is-01kt0wd442cmyknxtpkvpapfr3
  - is-01kt0wd6xe32z4gjbtjbapgs58
  - is-01kt0wdbv1016t7ta4nxxaqwyz
  - is-01kt0wdfzjjqe6sdawfc77e4v1
  - is-01kt0wdn9eh9m81ct8n1gr8k7y
  - is-01kt0wdsdxen1z505jfgq70k2e
created_at: 2026-06-01T06:01:23.596Z
updated_at: 2026-06-01T06:02:36.348Z
---
Extract the CSS + JS + Jinja partials that draw the Practical Prose visual surfaces into shared components at tools/render-components/, ingested by both the explorations workbench and the pprose render output via an auto-generated mirror. Renderer becomes thin outer page + data shaping; the card and tip panels are JS-built client-side. Phase 1 ships one variant — 'interactive' — and the architecture leaves room for future static-cards / annotated-doc variants. See spec for the full design.
