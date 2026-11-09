#!/bin/bash
# Cycle 187 planted controls (I-164 / I-179): each plant on all.bin rows q-100..q+100 with lrk186 method 1, L 1-3, in its direction
# (f: A themed x B vocabulary; r: A vocabulary x B themed; negatives in both); audit build lrk186safe (method 2, every pair, no
# shortcut) on q-2..q+3 against method 1 on the same rows; then checkctl187.py.  Every job under setsid timeout (own process group).
W=${W:-/workspace/k4c187/w}; T=${T:-/tmp/kcf/tools/cycle187}; O=${O:-ctl}; cd $W/run; mkdir -p $O/out
V=../support/alpha172.txt; TH=../support/alpha_themed180.txt; A=../support/all.bin
python3 $T/plant187.py $A $V $TH $O > $O/planted.txt
python3 -c "
import json
for p in json.load(open('$O/plants.json')): print(p['name'], p['ct'], p['q'], p['dir'] if p['kind']=='pos' else 'fr')" > $O/jobs.txt
run(){ OMP_NUM_THREADS=6 setsid timeout 60 "$@"; }
while read nm ct q ds; do lo=$((q>100?q-100:0)); a=$((q>2?q-2:0)); b=$((q+4))
  for dr in $(echo $ds | grep -o .); do
    if [ $dr = f ]; then XA=$TH; XB=$V; else XA=$V; XB=$TH; fi
    run ./lrk186     $ct $A $XA $XB $nm $lo $((q+101)) 1 1 3 q4$dr > $O/out/$nm.$dr.m.txt
    run ./lrk186     $ct $A $XA $XB $nm $a $b 1 1 3 q4$dr > $O/out/$nm.$dr.mn.txt
    run ./lrk186safe $ct $A $XA $XB $nm $a $b 2 1 3 q4$dr > $O/out/$nm.$dr.safe.txt
  done
done < $O/jobs.txt
python3 $T/checkctl187.py $O/plants.json $O/out $A $V $TH
