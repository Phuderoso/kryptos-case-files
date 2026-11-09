#!/bin/bash
# Cycle 166 (IDEAS I-070): three segments / returning key, period-7 phase, Quagmire III.  Resumable: finished files skipped.
# D: direct strict + leave-one-crib-out (24 drops), all 86,731 alphabets, K4 + 4 shuffled + 20 profile-matched nulls.
# BA: behind the full 165,065-entry bank (both directions, ix 0/1), A-Z/KRYPTOS only, all 25 texts (8 slices each).
# BS: behind every 200th bank entry, all 86,731 alphabets, K4 + null1-2 + mnull01-02.
# BE: bank A-Z/KRYPTOS leave-one-crib-out, K4 + null1-2 + mnull01-02 (24 drops).
H=$(cd "$(dirname "$0")" && pwd); W=${W:-/workspace/k4c166/run166}; A=/home/box/kryptos_support_backup/alpha.bin; B=/home/box/kryptos_support_backup/perms97.bin
mkdir -p $W; cd $W; X=$H/split3; NP=165065
job(){ # name cmd...
  local n=$1; shift; [ -s $n.txt ] && return; "$@" > $n.tmp && mv $n.tmp $n.txt; }
export -f job; export X A B NP
{
while read lab ct; do echo "job D_${lab} $H/djob.sh $lab $ct"; done < $H/texts166.txt
while read lab ct; do for i in 0 1 2 3 4 5 6 7; do lo=$((i*20634)); echo "job BA_${lab}_$i $X $ct $A $B $lab $lo $((lo+20634)) 2"; done; done < $H/texts166.txt
grep -E '^(K4|null1|null2|mnull01|mnull02) ' $H/texts166.txt | while read lab ct; do for i in 0 1 2 3 4 5 6 7; do lo=$((i*20800)); echo "job BS_${lab}_$i $X $ct $A $B $lab $lo $((lo+20800)) 86731 -1 200"; done; done
grep -E '^(K4|null1|null2|mnull01|mnull02) ' $H/texts166.txt | while read lab ct; do for d in $(seq 0 23); do echo "job BE_${lab}_$d $X $ct $A $B $lab 0 $NP 2 $d"; done; done
} > jobs.txt
date > start.txt
xargs -P 8 -L 1 bash -c '"$@"' _ < jobs.txt
date > done.txt
