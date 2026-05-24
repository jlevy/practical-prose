---
type: is
id: is-01ksbzzpf4vq12anme7phg3j6p
title: "Schema: bump rubric_schema.yaml version and replace 0 with ERR in valid score values"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01ksbzxycfj95nzb0mexrshpp6
created_at: 2026-05-24T03:20:45.795Z
updated_at: 2026-05-24T03:55:30.020Z
closed_at: 2026-05-24T03:55:30.017Z
close_reason: implemented on rubric-zero-to-err branch (PR pending)
---
tools/pprose/src/pprose/rubric_schema.yaml: bump version 20-dim-v1 -> 20-dim-v2; in score_values.valid remove 0 and add ERR; update the notes string to describe NA + ERR + 1-5 (no 0).
