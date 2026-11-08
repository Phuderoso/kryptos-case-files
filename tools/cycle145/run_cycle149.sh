#!/bin/bash
# Cycle 149: ptfree (tools/cycle139/ptfree.c unchanged) behind the full 165k bank, all.txt words 9001-10057 (end of list).
# K4: all 1057 words. Nulls: FULL bank (no subsampling) on words 9001-9528, the first full-bank null baseline.
set -e
W=${W:-/workspace/k139}; P=/home/box/kryptos_support_backup/perms97.bin; cd "$W"
K=$(cat /tmp/kcf/data/k4.txt)
sed -n '9001,$p' allA.txt > w1057.txt
( for c in $(seq 0 15); do lo=$((c*67)); hi=$((lo+67)); [ $hi -gt 1057 ] && hi=1057; echo "K4 $K $lo $hi"; done
  for z in 1 2; do N=$(grep "^null$z" controls.txt|cut -d' ' -f2); for c in 0 1 2 3 4 5 6 7; do echo "null$z $N $((c*66)) $((c*66+66))"; done; done
) | timeout 500 xargs -P 8 -L 1 sh -c 'exec ./ptfree $1 w1057.txt '$P' $0 $2 $3 > c149_$0_$2.txt'
