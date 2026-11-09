#!/bin/bash
# Cycle 182 planted controls: each plant on all.bin rows q-500..q+500, both directions (f: A themed x B vocab, method 0; r: A vocab x
# B themed, method 1), M0 L 1-6, plus the audit build lrk182safe with method 2 (every pair looked up, no shortcut), then checkctl182.py.
W=${W:-/workspace/k4c182/w}; T=${T:-/workspace/k4c182/tools}; cd $W/run; mkdir -p ctl/out
V=../support/alpha172.txt; TH=../support/alpha_themed180.txt
python3 $T/plant182.py ../support/all.bin $V $TH ctl > ctl/planted.txt
python3 -c "
import json
for p in json.load(open('ctl/plants.json')): print(p['name'], p['ct'], max(0, p['q'] - 500), p['q'] + 500)" > ctl/jobs.txt
while read nm ct lo hi; do
  OMP_NUM_THREADS=6 ./lrk182     $ct ../support/all.bin $TH $V $nm $lo $hi 0 1 6 q4f > ctl/out/$nm.f.txt
  OMP_NUM_THREADS=6 ./lrk182     $ct ../support/all.bin $V $TH $nm $lo $hi 1 1 6 q4r > ctl/out/$nm.r.txt
  OMP_NUM_THREADS=6 ./lrk182safe $ct ../support/all.bin $TH $V $nm $lo $hi 2 1 6 q4f > ctl/out/$nm.f.safe.txt
  OMP_NUM_THREADS=6 ./lrk182safe $ct ../support/all.bin $V $TH $nm $lo $hi 2 1 6 q4r > ctl/out/$nm.r.safe.txt
done < ctl/jobs.txt
python3 $T/checkctl182.py ctl/plants.json ctl/out ../support/all.bin ../support/quadgrams.json $V,$TH
