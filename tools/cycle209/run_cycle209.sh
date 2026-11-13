#!/bin/bash
# Cycle 209 registered run (PREREG209). Own process group (setsid), hard timeout 600 s; kill only this group.
set -u
cd "$(dirname "$0")"
SUP=${SUP:-/workspace/k4c209/sup}
setsid timeout -k 10 600 python3 run209.py "$SUP" results209.json > runlog209.txt 2>&1
echo "exit $?" >> runlog209.txt
