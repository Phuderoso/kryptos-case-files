#!/bin/bash
# Cycle 201 registered run. Own process group, hard timeout 480 s (kill only this group).
set -u
cd "$(dirname "$0")"
OUT=${OUT:-.}
SUP=${SUP:-/workspace/k4c201/sup}
setsid timeout -k 10 480 bash -c "python3 recount201.py $SUP && python3 robust201.py run --sup $SUP --seedbase 21000 --nref 1000 --nheld 200 --nown 300 --ndil 300 --procs 7 --out $OUT/results201.json" > $OUT/runlog201.txt 2>&1
echo "exit $?" >> $OUT/runlog201.txt
