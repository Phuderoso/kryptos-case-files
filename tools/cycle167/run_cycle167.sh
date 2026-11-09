#!/bin/bash
# Cycle 167 (IDEAS I-082): segment-shifted period-7 key (k | k+d2 | k+d3), Quagmire III.  Resumable: finished files skipped.
# BS: every 4000th bank entry (q = 0, 4000, ..., 164000: 42 perms x 2 dir x 2 ix = 168 configs), all 86,731 alphabets,
#     K4 + null1-2 + mnull01-02 (6 slices each).
# D:  direct strict + leave-one-crib-out (24 drops), all 86,731 alphabets, K4 + 4 shuffled + 20 profile-matched nulls.
# BA: full 165,065-entry bank (both directions, ix 0/1), A-Z/KRYPTOS only, all 25 texts (4 slices each).
# BE: bank A-Z/KRYPTOS leave-one-crib-out, K4 + null1 + mnull01 (24 drops).
H=$(cd "$(dirname "$0")" && pwd); W=${W:-/workspace/k4c167/run167}; A=/home/box/kryptos_support_backup/alpha.bin; B=/home/box/kryptos_support_backup/perms97.bin
mkdir -p $W; cd $W; X=$H/shift3; NP=165065
job(){ local n=$1; shift; [ -s $n.txt ] && return; "$@" > $n.tmp && mv $n.tmp $n.txt; }
export -f job; export X A B NP
{
grep -E '^(K4|null1|null2|mnull01|mnull02) ' $H/texts167.txt | while read lab ct; do for i in 0 1 2 3 4 5; do lo=$((i*28000)); echo "job BS_${lab}_$i $X $ct $A $B $lab $lo $((lo+28000)) 86731 -1 4000"; done; done
while read lab ct; do echo "job D_${lab} $H/djob.sh $lab $ct"; done < $H/texts167.txt
grep -E '^(K4|null1|mnull01) ' $H/texts167.txt | while read lab ct; do for d in $(seq 0 23); do echo "job BE_${lab}_$d $X $ct $A $B $lab 0 $NP 2 $d"; done; done
while read lab ct; do for i in 0 1 2 3; do lo=$((i*41267)); echo "job BA_${lab}_$i $X $ct $A $B $lab $lo $((lo+41267)) 2"; done; done < $H/texts167.txt
} > jobs.txt
date > start.txt
xargs -P 8 -L 1 bash -c '"$@"' _ < jobs.txt
date > done.txt
