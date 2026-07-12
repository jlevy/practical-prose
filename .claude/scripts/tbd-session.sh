#!/bin/bash
# Ensure the tbd CLI is available and run `tbd prime`.
# Installed by: tbd setup --auto. Runs on SessionStart and PreCompact.
#
# Local-first, then a VERSION-PINNED zero-install fallback. Pinning is both a
# supply-chain control (an unpinned runner re-resolves to latest on every run
# and bypasses any cool-off) and a consistency control (every teammate and agent
# runs the same tbd version).

# Prefer common local bin locations.
export PATH="$HOME/.local/bin:$HOME/bin:/usr/local/bin:$PATH"

# Local-first: use tbd if it is already on PATH. If it fails (for example, an
# older install that cannot read this repo's .tbd config format), fall through
# to the pinned runner instead of exiting with the failure.
local_tbd_failed=0
if command -v tbd &> /dev/null; then
    if tbd prime "$@"; then
        exit 0
    fi
    local_tbd_failed=1
    echo "[tbd] local tbd failed (older than this repo's config format?); trying the pinned fallback." >&2
fi

# Pinned zero-install fallback. Never use an unpinned runner here.
if command -v npx &> /dev/null; then
    npx --yes get-tbd@0.4.0 prime "$@"
    exit $?
fi

if [ "$local_tbd_failed" -eq 1 ]; then
    echo "[tbd] local tbd failed and npx is unavailable."
    echo "[tbd] Fix or upgrade local tbd, or install Node.js/npm to enable the pinned fallback."
else
    echo "[tbd] tbd CLI not found and npx is unavailable."
    echo "[tbd] Install it with: npm install -g get-tbd@0.4.0"
fi
exit 1
