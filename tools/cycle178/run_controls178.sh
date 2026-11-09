#!/bin/bash
# Cycle 178 planted controls: each plant on all.bin rows q-1500..q+1500 with its model (lr178), then checkctl178.py.
W=${W:-/workspace/k4c178w}; cd $W/run; mkdir -p ctl/out
python3 - <<'PY' > ctl/jobs.txt
import json
for p in json.load(open("ctl/plants.json")):
    q = p["q"]; lo, hi = max(0, q - 1500), q + 1500
    if p["mode"] == 0: args = f"0 1 {max(8, p['L'])}" if p["L"] < 9 else "0 9 9"
    elif p["mode"] == 1: args = "1 1 5"
    else: args = f"2 6 10 {p['ix']} seeds178.txt"
    if p["name"] == "P1_ix0_L3_az_vig" or p["name"].startswith("N1"): args = "0 1 9"
    print(p["name"], p["ct"], lo, hi, args)
PY
while read nm ct lo hi args; do OMP_NUM_THREADS=6 ./lr178 $ct ../support/all.bin $nm $lo $hi $args > ctl/out/$nm.txt; done < ctl/jobs.txt
python3 ../../k4c178/tools/cycle178/checkctl178.py ctl/plants.json ctl/out ../support/all.bin ../support/quadgrams.json
