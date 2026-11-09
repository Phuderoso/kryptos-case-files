#!/bin/bash
# Cycle 185 planted controls (I-172): each plant on all.bin rows q-100..q+100 with lrk185 method 1 (A = B list = vocabulary), L 1-3; the audit
# build lrk185safe (method 2: every pair, no prefilter, 13-value loop on every slot) on rows q-2..q+3, compared with the main build on the
# same 6 rows (w20 runs, name kept from cycle 183). Then checkctl185.py.
W=${W:-/workspace/k4c185/w}; T=${T:-/workspace/k4c185/tools}; O=${O:-ctl}; cd $W/run; mkdir -p $O/out
V=../support/alpha172.txt; TH=../support/alpha_themed180.txt; A=../support/all.bin
python3 $T/plant185.py $A $V $TH $O > $O/planted.txt
python3 -c "
import json
for p in json.load(open('$O/plants.json')): print(p['name'], p['ct'], p['q'])" > $O/jobs.txt
while read nm ct q; do
  lo=$((q>100?q-100:0)); lo2=$((q>2?q-2:0))
  OMP_NUM_THREADS=6 ./lrk185     $ct $A $V $V $nm $lo $((q+101)) 1 1 3 q4r > $O/out/$nm.r.txt
  OMP_NUM_THREADS=6 ./lrk185     $ct $A $V $V $nm $lo2 $((q+4)) 1 1 3 q4r > $O/out/$nm.r.w20.txt
  OMP_NUM_THREADS=6 ./lrk185safe $ct $A $V $V $nm $lo2 $((q+4)) 2 1 3 q4r > $O/out/$nm.r.safe.txt
done < $O/jobs.txt
python3 $T/checkctl185.py $O/plants.json $O/out $A ../support/quadgrams.json $V
