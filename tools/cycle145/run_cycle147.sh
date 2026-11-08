#!/bin/bash
# Cycle 147: ptfree (tools/cycle139/ptfree.c unchanged) behind the 165k bank, all.txt words 6801-9000 (lines 6801-9000 of allA.txt).
# Nulls: every 10th bank entry. Remaining after this: words 9001-10056.
set -e
W=${W:-/workspace/k139}; P=/home/box/kryptos_support_backup/perms97.bin; cd "$W"
K=$(cat /tmp/kcf/data/k4.txt)
sed -n 6801,9000p allA.txt > w2200.txt
for c in 0 1 2 3 4 5 6 7; do ./ptfree $K w2200.txt $P K4 $((c*275)) $((c*275+275)) > c147_K4_$c.txt & done; wait
for z in 1 2; do N=$(grep "^null$z" controls.txt|cut -d' ' -f2)
  for c in 0 1 2 3; do ./ptfree $N w2200.txt $P null$z $((c*550)) $((c*550+550)) 10 > c147_null${z}_$c.txt & done; done; wait
