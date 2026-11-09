#!/bin/bash
# Cycle 180 planted controls: each plant on all.bin rows q-1500..q+1500 with lrk180 (M0 L 1-7 vocab; M1 L 1-3 vocab; P9 M1 L 4 themed), then checkctl180.py.
W=${W:-/workspace/k4c180/w}; T=${T:-/workspace/k4c180/repo/tools/cycle180}; cd $W/run; mkdir -p ctl/out
python3 $T/plant180.py ../support/all.bin ../support/alpha172.txt ctl > ctl/planted.txt
python3 - <<'PY' > ctl/jobs.txt
import json
for p in json.load(open("ctl/plants.json")):
    q = p["q"]; lo, hi = max(0, q - 1500), q + 1500
    if p["ix"] == 0: args = "../support/alpha172.txt 0 1 7"
    elif p["run"] == "themed": args = "../support/alpha_themed180.txt 1 4 4"
    else: args = "../support/alpha172.txt 1 1 3"
    print(p["name"], p["ct"], lo, hi, args)
PY
while read nm ct lo hi af args; do OMP_NUM_THREADS=6 ./lrk180 $ct ../support/all.bin $af $nm $lo $hi $args > ctl/out/$nm.txt; done < ctl/jobs.txt
python3 $T/checkctl180.py ctl/plants.json ctl/out ../support/all.bin ../support/quadgrams.json ../support/alpha172.txt
