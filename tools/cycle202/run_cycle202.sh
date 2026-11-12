#!/bin/bash
# Cycle 202 registered run (PREREG202). Own process group (setsid), hard timeout 480 s; kill only this group.
set -u
cd "$(dirname "$0")"
SUP=${SUP:-/workspace/k4c202/sup}
setsid timeout -k 10 480 bash -c "python3 recount202.py $SUP && python3 col202.py run --sup $SUP --seedbase 202202 --nref 4000 --nheld 1000 --nb 2000 --ng3 500 --nown 300 --procs 7 --out results202.json && python3 verify_errata202.py $SUP 1000 errata202.json" > runlog202.txt 2>&1
echo "exit $?" >> runlog202.txt
