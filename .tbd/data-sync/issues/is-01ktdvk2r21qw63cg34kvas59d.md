---
type: is
id: is-01ktdvk2r21qw63cg34kvas59d
title: "Calibration pass: fix artifact leakage, NA over-application, and scoring-prompt compliance"
kind: epic
status: open
priority: 1
version: 9
labels: []
dependencies: []
child_order_hints:
  - is-01ktdvkr8fvq08g2bgskm2n0bv
  - is-01ktdvkrg2safyp2p9xv376xqz
  - is-01ktdvkrqm1m1tg056wa26a2qa
  - is-01ktdvkrz57p98g5aghdazv4r6
  - is-01ktdvks6hym56yct9tn3z1tae
  - is-01ktdvksfe3k8staw0ad1z69wr
  - is-01ktdvkspth49ng7xxfrw3zeg8
  - is-01ktdweftjsa1p9bgvc3qg1typ
created_at: 2026-06-06T06:58:08.770Z
updated_at: 2026-06-06T07:13:06.897Z
---
Calibration pass from evaluating two example docs (Vannevar Bush 'As We May Think' and the Apple Media Services Terms) with pprose score.

Findings:
- Grounding is strong: every cited specific verified against source; no hallucinations.
- Conversion artifacts leak into scores: Bush Organization penalized by bare '## 1'..'## 8' headings (our conversion); iTunes Formatting/Consistency penalized by 29 escaped '\-' hyphens and a '\$' (pandoc artifacts). The eval is scoring our fixture conversion, not the documents.
- NA over-applied on iTunes Verifiability/Factuality despite institutional attributions and '48 C.F.R.' statutory citations (G1 NA anchor says attributions to institutions DO engage Verifiability).
- overall_mean inverts (iTunes 3.92 > Bush 3.5) because 7 NA dims are excluded; means are reductive across genres.
- Process: scorer under-emits structured rule_findings for sub-5 scores, tripping the alignment guard (we needed --allow-misaligned; 11 issues on Bush).

Goal: clean the fixtures, tighten the scoring prompt + NA guidance, re-score, regenerate README screenshots, and document the mean caveat.
