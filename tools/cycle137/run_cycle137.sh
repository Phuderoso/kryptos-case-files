#!/bin/bash
# Cycle 137: CT-autokey, keyed cipher alphabet x arbitrary plaintext alphabet,
# behind the 165,065-entry bank (both directions, both index orders), L 1..16.
# K4 full; two shuffled nulls on every 10th bank entry (rate check). 8-way.
set -e
W=${W:-/workspace/k137}; B=/home/box/kryptos_support_backup/perms97.bin; cd "$W"
K=$(cat /tmp/kcf/data/k4.txt)
N1=$(grep "^null1 " controls.txt|cut -d' ' -f2); N2=$(grep "^null2 " controls.txt|cut -d' ' -f2)
nq=$(wc -l < all.txt)
run_one() { local lab=$1 ct=$2 st=$3
  for ((lo=0; lo<nq; lo+=200)); do echo "$ct" "$lab" "$lo" "$((lo+200))"; done |
   xargs -P 8 -L 1 sh -c './ctfree "$0" all.txt '"$B"' "$1" "$2" "$3" 16 '"$st"' > out_"$1"_"$2".txt'
  date > "done_${lab}.txt"; }
run_one K4 "$K" 1
run_one null1 "$N1" 10
run_one null2 "$N2" 10
for lab in K4 null1 null2; do cat out_${lab}_*.txt | awk -v l=$lab '/^C/{t+=$4;c+=$6;s+=$8} END{print l,"tests",t,"consistent",c,"survivors",s}'; done > results.txt
cat out_*.txt | grep '^S' > survivors.txt || true
date > done.txt
