#!/bin/bash
# Cycle 200 registered run. Own process group, hard timeout 480 s (kill only this group).
set -u
cd "$(dirname "$0")"
OUT=${OUT:-.}
setsid timeout -k 10 480 bash -c "python3 recount200.py && python3 rhythm200.py run --seedbase 20000 --nplant 150 --nown 300 --ntarget 300 --out $OUT/results200.json" > $OUT/runlog200.txt 2>&1
echo "exit $?" >> $OUT/runlog200.txt
