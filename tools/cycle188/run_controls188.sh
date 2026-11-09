#!/bin/bash
# Cycle 188 planted controls (I-185): each plant on all.bin rows q-win..q+win with lrk188 method 1, L 1..lmax (lmax 2, win 100; the
# order-3 plants and negatives lmax 3, win 10), in its direction (negatives in both); audit build lrk188safe (method 2, every pair, no
# prefilter / shortcut) on q-2..q+3 against method 1 on the same rows; then checkctl188.py.  Every job under setsid timeout.
W=${W:-/workspace/k4c188/w}; T=${T:-/tmp/kcf/tools/cycle188}; O=${O:-ctl}; cd $W/run; mkdir -p $O/out
V=../support/alpha172.txt; TH=../support/alpha_themed180.txt; A=../support/all.bin
python3 $T/plant188.py $A $V $TH $O > $O/planted.txt
python3 -c "
import json
for p in json.load(open('$O/plants.json')): print(p['name'], p['ct'], p['q'], p['dir'] if p['kind']=='pos' else 'fr', p['lmax'], p['win'])" > $O/jobs.txt
run(){ OMP_NUM_THREADS=6 setsid timeout 60 "$@"; }
while read nm ct q ds lx wn; do lo=$((q>wn?q-wn:0)); a=$((q>2?q-2:0)); b=$((q+4))
  for dr in $(echo $ds | grep -o .); do
    if [ $dr = f ]; then XA=$TH; XB=$V; else XA=$V; XB=$TH; fi
    run ./lrk188     $ct $A $XA $XB $nm $lo $((q+wn+1)) 1 1 $lx q4$dr > $O/out/$nm.$dr.m.txt
    run ./lrk188     $ct $A $XA $XB $nm $a $b 1 1 $lx q4$dr > $O/out/$nm.$dr.mn.txt
    run ./lrk188safe $ct $A $XA $XB $nm $a $b 2 1 $lx q4$dr > $O/out/$nm.$dr.safe.txt
  done
done < $O/jobs.txt
python3 $T/checkctl188.py $O/plants.json $O/out $A $V $TH
