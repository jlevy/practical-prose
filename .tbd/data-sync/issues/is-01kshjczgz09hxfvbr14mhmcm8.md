---
type: is
id: is-01kshjczgz09hxfvbr14mhmcm8
title: Render rule_findings as markdown bullets; drop qual_reasons summary for numeric scores
kind: feature
status: closed
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-05-26T07:18:47.570Z
updated_at: 2026-05-26T07:20:52.898Z
closed_at: 2026-05-26T07:20:52.897Z
close_reason: "Implemented option A: assessment block now renders rule_findings as a bulleted list (sans, with bold 'Rule N · verdict' prefix). qual_reasons string is dropped for numeric scores (redundant with findings); kept as the assessment text for NA/ERR scores where it's the only place that explains why. Dropped unused .tip-reason / .tip-finding card CSS."
---
