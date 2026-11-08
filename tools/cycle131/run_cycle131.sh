#!/bin/bash
# Cycle 131 runner (8 cores). Word lists: themed (tools/dcol_gen.py) and themed + cycle-56 vocabulary.
W=${W:-/workspace/k4c131}; D=$(cd $(dirname "$0"); pwd); BANK=${BANK:-/home/box/kryptos_support_backup/perms97.bin}; cd $W
gcc -O2 -o dbl $D/dbl.c; python3 $D/mklists.py; python3 $D/plant.py > controls.txt
ct(){ if [ $1 = K4 ]; then cat $D/../../data/k4.txt; else grep "^$1 " controls.txt | cut -d' ' -f2; fi; }
for T in K4 null1 null2; do n=$(wc -l < all.txt)
  for k in 0 1 2 3 4 5 6 7; do ./dbl $(ct $T) all.txt all.txt D x $T $((k*n/8)) $(((k+1)*n/8)) > resD_${T}_$k.txt & done; wait; done
for T in K4 null1; do
  for k in 0 1 2 3 4 5 6 7; do ./dbl $(ct $T) themed.txt themed.txt T $BANK $T $((k*97/8)) $(((k+1)*97/8)) > resT_${T}_$k.txt & done; wait; done
