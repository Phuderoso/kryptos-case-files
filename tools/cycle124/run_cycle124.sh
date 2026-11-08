#!/bin/sh
# Cycle 124 reproduction: all 9! and 10! column orders (rotation 0), COL/ROW read, both directions, x periodic key.
# Needs qg.bin (float32 log10 quadgrams, 26^4) from the support backup for scoring only.
set -e
S=${SUPPORT:-/home/box/kryptos_support_backup}; W=${WORK:-/workspace/k4c124}; mkdir -p $W/p22
T=$(cd "$(dirname "$0")" && pwd); K4=$(cat $T/../../data/k4.txt)
gcc -O2 -o $W/allcol $T/allcol.c
python3 $T/plant.py > $W/controls.txt
for n in ctl1 ctl3; do ct=$(grep "^$n " $W/controls.txt|cut -d' ' -f2); for f in 0 1 2 3 4 5 6 7 8 9; do $W/allcol $ct 10 $f 18 $n > $W/$n.w10.$f & done; wait; done
cat $W/ctl?.w10.* > $W/ctl_w10.out
for n in ctl2 ctl4; do ct=$(grep "^$n " $W/controls.txt|cut -d' ' -f2); $W/allcol $ct 9 -1 18 $n; done > $W/ctl_w9.out
# K4 and 3 shuffled nulls, p 1-22 (p <= 18 is the exact claim; 19-22 underdetermined, scored)
for n in K4 null1 null2 null3; do if [ $n = K4 ]; then ct=$K4; else ct=$(grep "^$n " $W/controls.txt|cut -d' ' -f2); fi
  $W/allcol $ct 9 -1 22 $n > $W/p22/$n.w9; for f in 0 1 2 3 4 5 6 7 8 9; do $W/allcol $ct 10 $f 22 $n > $W/p22/$n.w10.$f & done; wait; done
cat $W/p22/* > $W/p22.out
python3 $T/score_surv.py $W/p22.out $W/controls.txt $T/../../data/k4.txt $S/qg.bin
python3 $T/score_surv.py $W/ctl_w10.out $W/controls.txt $T/../../data/k4.txt $S/qg.bin
python3 $T/score_surv.py $W/ctl_w9.out $W/controls.txt $T/../../data/k4.txt $S/qg.bin
