#!/bin/bash
# Cycle 209 registered run 2 (PREREG209b). Own process group (setsid), hard timeout 420 s; kill only this group.
set -u
cd "$(dirname "$0")"
SUP=${SUP:-/workspace/k4c209/sup}
SKIP_SOUND=1 setsid timeout -k 10 420 python3 run209.py "$SUP" results209b.json > runlog209b.txt 2>&1
echo "exit $?" >> runlog209b.txt
