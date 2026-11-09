#!/bin/bash
# Cycle 181 planted controls: each plant on all.bin rows q-500..q+500 with lrk181 (M0 L 1-6; M1 L 1-3), then checkctl181.py.
# BIN=lrk181 (default) or lrk181safe (audit build without the two exact shortcuts).
W=${W:-/workspace/k4c181/w}; T=${T:-/workspace/k4c181/repo/tools/cycle181}; BIN=${BIN:-lrk181}; cd $W/run; mkdir -p ctl/out_$BIN
python3 $T/plant181.py ../support/all.bin ../support/alpha172.txt ctl > ctl/planted.txt
python3 - <<'PY' > ctl/jobs.txt
import json
for p in json.load(open("ctl/plants.json")):
    q = p["q"]; lo, hi = max(0, q - 500), q + 500
    print(p["name"], p["ct"], lo, hi, "0 1 6" if p["ix"] == 0 else "1 1 3")
PY
while read nm ct lo hi args; do OMP_NUM_THREADS=6 ./$BIN $ct ../support/all.bin ../support/alpha172.txt $nm $lo $hi $args > ctl/out_$BIN/$nm.txt; done < ctl/jobs.txt
python3 $T/checkctl181.py ctl/plants.json ctl/out_$BIN ../support/all.bin ../support/quadgrams.json ../support/alpha172.txt
