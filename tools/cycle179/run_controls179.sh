#!/bin/bash
# Cycle 179 planted controls: each plant on all.bin rows q-1500..q+1500 with lr179 (M0 L 1-8 or M1 L 1-5), then checkctl179.py.
W=${W:-/workspace/k4c179/w}; T=$(cd "$(dirname "$0")" && pwd); cd $W/run; mkdir -p ctl/out
python3 $T/plant179.py ../support/all.bin ctl > ctl/plants.log
python3 - <<'PY' > ctl/jobs.txt
import json
for p in json.load(open("ctl/plants.json")):
    q = p["q"]; print(p["name"], p["ct"], max(0, q - 1500), q + 1500, "0 1 8" if p["ix"] == 0 else "1 1 5")
PY
while read nm ct lo hi args; do OMP_NUM_THREADS=6 ./lr179 $ct ../support/all.bin $nm $lo $hi $args > ctl/out/$nm.txt; done < ctl/jobs.txt
python3 $T/checkctl179.py ctl/plants.json ctl/out ../support/all.bin ../support/quadgrams.json
