---
type: is
id: is-01kx52wnrh7tzp3arjjy4jy3fb
title: Make generated tbd bootstrap reject incompatible installed versions
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:59:38.768Z
updated_at: 2026-08-19T17:59:38.057Z
closed_at: 2026-08-19T17:59:38.056Z
close_reason: "Both halves resolved as of tbd 0.6.5 (66c85b2). Half 1 fixed upstream: generated launchers now gate local-first on actual format compatibility via tbd_local_can_read_repository() ('tbd config get tbd_format'), so an older installed tbd no longer wins over the pinned runner; the fallback version is read from .tbd/config.yml tbd_fallback_version and semver-validated before reaching npx. Half 2 ('remove generated @latest install advice') is resolved by policy rather than by removal: the remaining 'npm install -g get-tbd@latest' lines are human-facing interactive bootstrap in SKILL.md, which SUPPLY-CHAIN-SECURITY.md's first-party exemption permits for github.com/jlevy packages; every unattended path (session hook, closing-reminder hook) now uses the exact pinned fallback. Reopen if the preference is to pin the interactive advice too."
---
PR #31 generated tbd session scripts prefer any tbd on PATH; an installed 0.2.x still wins over pinned 0.3.0 and cannot read f06. Fix upstream generator to check compatibility or fall back after prime failure; also remove generated @latest install advice under exact-pin repos.

## Notes

tbd 0.4.0 setup still prefers any local tbd and exits on prime failure instead of invoking the pinned runner. The v0.2.0 release PR preserves the repo-local fallback and updates it to get-tbd@0.4.0 in both session and closing-reminder hooks; rerunning setup overwrites this customization, so the upstream generator issue remains open.
