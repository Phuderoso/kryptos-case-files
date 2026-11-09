#!/bin/bash
# Cycle 183 planted controls: each plant on all.bin rows q-100..q+100, both directions (f method 0, r method 1), L 1-5; the audit build
# lrk183safe (method 2: every pair, no prefilter, 13-value loop on every slot) on rows q-20..q+20, compared with the main build on the
# same 41 rows (w20 runs). Then checkctl183.py.
W=${W:-/workspace/k4c183/w}; T=${T:-/workspace/k4c183/tools}; O=${O:-ctl}; cd $W/run; mkdir -p $O/out
V=../support/alpha172.txt; TH=../support/alpha_themed180.txt; A=../support/all.bin
python3 $T/plant183.py $A $V $TH $O > $O/planted.txt
python3 -c "
import json
for p in json.load(open('$O/plants.json')): print(p['name'], p['ct'], p['q'])" > $O/jobs.txt
while read nm ct q; do
  lo=$((q>100?q-100:0)); lo2=$((q>20?q-20:0))
  OMP_NUM_THREADS=6 ./lrk183     $ct $A $TH $V $nm $lo $((q+101)) 0 1 5 q4f > $O/out/$nm.f.txt
  OMP_NUM_THREADS=6 ./lrk183     $ct $A $V $TH $nm $lo $((q+101)) 1 1 5 q4r > $O/out/$nm.r.txt
  OMP_NUM_THREADS=6 ./lrk183     $ct $A $TH $V $nm $lo2 $((q+21)) 0 1 5 q4f > $O/out/$nm.f.w20.txt
  OMP_NUM_THREADS=6 ./lrk183     $ct $A $V $TH $nm $lo2 $((q+21)) 1 1 5 q4r > $O/out/$nm.r.w20.txt
  OMP_NUM_THREADS=6 ./lrk183safe $ct $A $TH $V $nm $lo2 $((q+21)) 2 1 5 q4f > $O/out/$nm.f.safe.txt
  OMP_NUM_THREADS=6 ./lrk183safe $ct $A $V $TH $nm $lo2 $((q+21)) 2 1 5 q4r > $O/out/$nm.r.safe.txt
done < $O/jobs.txt
python3 $T/checkctl183.py $O/plants.json $O/out $A ../support/quadgrams.json $V,$TH
