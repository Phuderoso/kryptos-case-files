#!/bin/bash
# Cycle 162 (IDEAS I-013): split period-7 key behind the 165,065-entry bank (both directions, key at plaintext or
# carved index), Q-III on 86,731 alphabets, Vig/Beau per segment; K4 + 2 shuffled + 2 profile-matched nulls.
# Direct (identity) strict and leave-one-crib-out for K4 and all 8 nulls.  Resumable: finished slices are skipped.
W=${W:-/workspace/k4c162}; A=/home/box/kryptos_support_backup/alpha.bin; B=/home/box/kryptos_support_backup/perms97.bin
cd "$W"; mkdir -p run; K=$(cat k4.txt); NP=165065; S=8; STEP=$(( (NP+S-1)/S ))
alltexts() { echo "K4 $K"; grep '^null' controls.txt; cut -d' ' -f1,2 mnulls.txt | grep '^mnull'; }
banktexts() { echo "K4 $K"; grep -E '^null[12] ' controls.txt; cut -d' ' -f1,2 mnulls.txt | grep -E '^mnull0[12] '; }
alltexts | while read lab ct; do [ -s run/direct_$lab.txt ] && continue
  { ./tools/split7 $ct $A x $lab 0 1 7 1; for d in $(seq 0 23); do ./tools/split7 $ct $A x $lab 0 1 7 1 $d | sed "s/^/D$d /"; done; } > run/direct_$lab.tmp && mv run/direct_$lab.tmp run/direct_$lab.txt
done
banktexts | while read lab ct; do for ((i=0;i<S;i++)); do lo=$((i*STEP)); hi=$((lo+STEP));
  [ -s run/bank_${lab}_$i.txt ] || echo "$ct $lab $lo $hi $i"; done; done |
 xargs -P 8 -L 1 sh -c './tools/split7 "$0" '"$A $B"' "$1" "$2" "$3" > run/bank_"$1"_"$4".tmp && mv run/bank_"$1"_"$4".tmp run/bank_"$1"_"$4".txt'
date > run/done.txt
