---
type: is
id: is-01ktdvks6hym56yct9tn3z1tae
title: Re-score both cleaned fixtures and diff vs current scores
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01ktdvksfe3k8staw0ad1z69wr
parent_id: is-01ktdvk2r21qw63cg34kvas59d
created_at: 2026-06-06T06:58:31.761Z
updated_at: 2026-06-06T07:13:06.549Z
closed_at: 2026-06-06T07:13:06.548Z
close_reason: |-
  Re-scored both cleaned fixtures with the updated prompt.
  iTunes (attributable, validated): Verifiability NA->4 and Factuality NA->4 (pp-4j9m); Formatting 3->4 and Consistency 3->4 (pp-r1zp); NA dims 7->5; passed the alignment guard cleanly with no --allow-misaligned (pp-ps1u).
  Bush: Organization stayed 2 even with the bare-number headings removed -> the low score is FAITHFUL to the original (no descriptive headings, thesis buried in section 6), not a conversion artifact; pp-1la7 improved the justification (dropped the questionable rule-9 'templated heading' citation) without moving the score. Other Bush dim shifts (breadth/coherence/discipline/parsimony/precision/scope each ±1) were run-to-run model variance, not the fixes.
  Alignment: Bush improved 11->2->1 misses but still needed --allow-misaligned on one borderline Breadth=4. See follow-up bead.
---
After fixture cleanup and prompt/rubric changes, re-score example-texts/as-we-may-think.md and apple-media-services-terms.md with Opus. Diff the new per-dimension scores against the current ones to quantify how much the artifact-leakage and NA fixes moved things. Should no longer need --allow-misaligned.
