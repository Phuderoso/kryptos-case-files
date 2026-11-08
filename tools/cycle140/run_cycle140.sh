#!/bin/bash
# Cycle 140: extends cycle 139's ptfree (tools/cycle139/ptfree.c, unchanged) behind the
# 165k bank to the next 3,000 vocabulary alphabets (all.txt words 601-3600).
# Needs the cycle 139 work dir (ptfree, allA.txt, controls.txt from tools/cycle139/plant.py).
set -e
W=${W:-/workspace/k139}; P=/home/box/kryptos_support_backup/perms97.bin; cd "$W"
K=$(cat /tmp/kcf/data/k4.txt)
sed -n 601,3600p allA.txt > w3000.txt
for c in 0 1 2 3 4 5 6 7; do ./ptfree $K w3000.txt $P K4 $((c*375)) $((c*375+375)) > c140_K4_$c.txt & done; wait
for z in 1 2; do N=$(grep "^null$z" controls.txt|cut -d' ' -f2)
  for c in 0 1 2 3; do ./ptfree $N w3000.txt $P null$z $((c*750)) $((c*750+750)) 10 > c140_null${z}_$c.txt & done; done; wait
