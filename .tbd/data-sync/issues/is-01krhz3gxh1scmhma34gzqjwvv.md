---
type: is
id: is-01krhz3gxh1scmhma34gzqjwvv
title: Finalize file-level skill design against research
kind: task
status: open
priority: 2
version: 10
spec_path: tools/docs/project/specs/active/plan-2026-05-13-cross-agent-skills.md
labels:
  - cross-agent-skills
  - planning
  - research-alignment
dependencies:
  - type: blocks
    target: is-01krhz12n33ecbdyrwb0c07ght
  - type: blocks
    target: is-01krhz172mtbpkr2ptyac3f0fp
  - type: blocks
    target: is-01krhz1b0bwex8nhw2mgkazmyd
  - type: blocks
    target: is-01krhz1fnfqa80jxzqsefnmgvc
  - type: blocks
    target: is-01krhz1m2ae7n8ghbjnjjeqcsz
  - type: blocks
    target: is-01krhz1wf1bsx960qc78frs7sx
  - type: blocks
    target: is-01krhz20668axryc1y423xcs5h
  - type: blocks
    target: is-01krhz27s9axj15pcwy0ccpt2d
  - type: blocks
    target: is-01krhz2f5wsv5rwkvzz2c6mbaq
parent_id: is-01krhz0ckjzn0s26wggjjfays1
created_at: 2026-05-14T00:45:07.376Z
updated_at: 2026-05-14T00:45:28.214Z
---
Before implementation, review the cross-agent skills spec against tools/docs/general/research/research-2026-05-13-repo-as-cross-agent-skill.md and expand the plan to file/function-level detail. Confirm concrete paths for AGENTS.md, CLAUDE.md, skills/*/SKILL.md, .claude/skills symlinks, tools/prose-eval/src/prose_eval/cli.py, pyproject.toml scripts, and CLI tests. Confirm the design follows the research: portable name/description frontmatter only, short router SKILL.md bodies, repo-as-distribution, uvx prose-eval entry point, no setup wizard/hooks/doc bundling, supported install paths, and no contradiction with AGENTS.md/CLAUDE.md guidance.
