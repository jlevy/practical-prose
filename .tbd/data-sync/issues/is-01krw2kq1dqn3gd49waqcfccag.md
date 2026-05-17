---
type: is
id: is-01krw2kq1dqn3gd49waqcfccag
title: Implement binary source-check modes
kind: task
status: open
priority: 2
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-17-eval-tool-and-model-configuration.md
labels: []
dependencies:
  - type: blocks
    target: is-01krw2m5ams9vjqa024nv638qs
parent_id: is-01krvxewx2bjm707fh941e3dvk
created_at: 2026-05-17T22:58:47.980Z
updated_at: 2026-05-17T22:59:27.434Z
---
Implement source_check.mode none|web|manifest. Keep default no-web behavior. For web mode, add provider web-search tools only through adapters: OpenAI Responses web_search and Anthropic server web search. Do not expose allowed/blocked domain controls. For manifest mode, add local evidence context without network tools. Record external_validation_performed and tool usage metadata.
