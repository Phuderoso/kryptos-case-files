#!/bin/bash
# Cycle 163 (IDEAS I-069): split period-7 key under one error (split7e.c), behind the 165,065-entry bank (both
# directions, key at plaintext or carved index) for K4 + null1 + mnull01 (and more texts if TEXTS is set), 8 slices
# each; direct (identity) for K4 and all 8 nulls.  Resumable: finished slices are skipped.
W=${W:-/workspace/k4c163}; A=/home/box/kryptos_support_backup/alpha.bin; B=/home/box/kryptos_support_backup/perms97.bin
cd "$W"; mkdir -p run; K=$(cat k4.txt); NP=165065; S=8; STEP=$(( (NP+S-1)/S )); TEXTS=${TEXTS:-"K4 null1 mnull01"}
ct_of() { [ "$1" = K4 ] && echo "$K" || { grep -h "^$1 " controls.txt mnulls.txt | head -1 | cut -d' ' -f2; }; }
for lab in K4 null1 null2 null3 null4 mnull01 mnull02 mnull03 mnull04; do [ -s run/direct_$lab.txt ] && continue
  ./tools/split7e $(ct_of $lab) $A x $lab 0 1 7 1 > run/direct_$lab.tmp && mv run/direct_$lab.tmp run/direct_$lab.txt; done
for lab in $TEXTS; do ct=$(ct_of $lab); for ((i=0;i<S;i++)); do lo=$((i*STEP)); hi=$((lo+STEP));
  [ -s run/bank_${lab}_$i.txt ] || echo "$ct $lab $lo $hi $i"; done; done |
 xargs -P 8 -L 1 sh -c './tools/split7e "$0" '"$A $B"' "$1" "$2" "$3" > run/bank_"$1"_"$4".tmp && mv run/bank_"$1"_"$4".tmp run/bank_"$1"_"$4".txt'
date > run/done.txt
