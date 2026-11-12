#!/bin/bash
# Cycle 204 registered run (PREREG204). Own process group (setsid), hard timeout 480 s; kill only this group.
set -u
cd "$(dirname "$0")"
SUP=${SUP:-/workspace/k4c204/sup}
setsid timeout -k 10 480 python3 run204.py "$SUP" results204.json 1.0 > runlog204.txt 2>&1
echo "exit $?" >> runlog204.txt
