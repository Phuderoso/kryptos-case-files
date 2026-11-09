#!/bin/bash
# Cycle 184 planted controls: each plant on all.bin rows q-200..q+200 with method 1 (syndrome join) and method 0 (CSR union map),
# vocabulary x vocabulary, M0 L 1-4 (H lines must be identical); audit build lrk184safe method 2 (every pair, no shortcut) on q-2..q+3
# against method 1 on the same rows; then checkctl184.py.
W=${W:-/workspace/k4c184/w}; T=${T:-/workspace/k4c184/tools}; D=${D:-ctl}; cd $W/run; mkdir -p $D/out
V=../support/alpha172.txt; TH=../support/alpha_themed180.txt; A=../support/all.bin
python3 $T/plant184.py $A $V $TH $D > $D/planted.txt
python3 -c "
import json
for p in json.load(open('$D/plants.json')): print(p['name'], p['ct'], p['q'])" > $D/jobs.txt
while read nm ct q; do lo=$((q>200?q-200:0)); hi=$((q+200)); a=$((q>2?q-2:0)); b=$((q+3))
  OMP_NUM_THREADS=6 ./lrk184     $ct $A $V $V $nm $lo $hi 1 1 4 q4vv > $D/out/$nm.m1.txt
  OMP_NUM_THREADS=6 ./lrk184     $ct $A $V $V $nm $lo $hi 0 1 4 q4vv > $D/out/$nm.m0.txt
  OMP_NUM_THREADS=6 ./lrk184     $ct $A $V $V $nm $a $b 1 1 4 q4vv > $D/out/$nm.m1n.txt
  OMP_NUM_THREADS=6 ./lrk184safe $ct $A $V $V $nm $a $b 2 1 4 q4vv > $D/out/$nm.safe.txt
done < $D/jobs.txt
python3 $T/checkctl184.py $D/plants.json $D/out $A ../support/quadgrams.json $V
