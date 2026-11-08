#!/bin/bash
# Cycle 130 runner: jobs "text L mode lo hi" in parallel (8 cores).
W=${W:-/workspace/k4c130}; D=$(cd $(dirname "$0"); pwd); cd $W
gcc -O2 -o pgfree $D/pgfree.c; python3 $D/plant.py > controls.txt
ct(){ if [ $1 = K4 ]; then cat $D/../../data/k4.txt; else grep "^$1 " controls.txt | cut -d' ' -f2; fi; }
{ for T in K4 null1 null2 null3 null4 null5 null6; do
    for L in 2 3 4 5 6 7 8; do echo "$T $L all 0 100000000"; done
    for L in 8 9 10 11; do echo "$T $L perm 0 100000000"; done
    case $T in K4|null1|null2)
      for s in 0 1 2 3 4 5 6 7 8 9; do echo "$T 9 all ${s}00000000 $((s+1))00000000"; done
      for s in $(seq 0 15); do echo "$T 12 perm $((s*30000000)) $(((s+1)*30000000))"; done;;
    esac
  done; } > jobs.txt
for T in K4 null1 null2 null3 null4 null5 null6; do ct $T > ct_$T.txt; done
xargs -P 8 -L 1 sh -c './pgfree $(cat '"$W"'/ct_$0.txt) $1 $2 $3 $4 $0' < jobs.txt > results_raw.txt
