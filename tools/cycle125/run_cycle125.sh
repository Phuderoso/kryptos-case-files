#!/bin/sh
# Cycle 125 reproduction: Digrafid (+ one null / one missing letter) crib test. ~2 min on 8 cores.
set -e
W=${WORK:-/workspace/k4c125}; mkdir -p $W; T=$(cd "$(dirname "$0")" && pwd); K4=$(cat $T/../../data/k4.txt)
gcc -O2 -o $W/digrafid $T/digrafid.c
python3 $T/mkkeys.py $W; python3 $T/plant.py > $W/controls.txt; cd $W
for lab in K4 ctl1 ctl2 ctl3 ctl4 null1 null2 null3; do if [ $lab = K4 ]; then ct=$K4; else ct=$(grep "^$lab " controls.txt|cut -d' ' -f2); fi
  ./digrafid $ct keys.txt pairs_same.txt 48 0 $lab > same_$lab.out & ./digrafid $ct keys.txt pairs_themed.txt 48 0 $lab > themed_$lab.out & done; wait
split -n l/8 -d pairs_cross.txt pc_
for c in pc_0*; do ./digrafid $K4 keys.txt $c 48 0 K4 > cross_K4_$c.out & done; wait
tail -n1 -q same_*.out themed_*.out cross_*.out
