#!/bin/bash
# Cycle 145: extends cycles 139-140's ptfree (tools/cycle139/ptfree.c, unchanged) behind the
# 165k bank to the next 3,200 vocabulary alphabets (all.txt words 3601-6800).
# Needs the cycle 139 work dir (ptfree, allA.txt, controls.txt from tools/cycle139/plant.py).
set -e
W=${W:-/workspace/k139}; P=/home/box/kryptos_support_backup/perms97.bin; cd "$W"
K=$(cat /tmp/kcf/data/k4.txt)
sed -n 3601,6800p allA.txt > w3200.txt
for c in 0 1 2 3 4 5 6 7; do ./ptfree $K w3200.txt $P K4 $((c*400)) $((c*400+400)) > c145_K4_$c.txt & done; wait
for z in 1 2; do N=$(grep "^null$z" controls.txt|cut -d' ' -f2)
  for c in 0 1 2 3; do ./ptfree $N w3200.txt $P null$z $((c*800)) $((c*800+800)) 10 > c145_null${z}_$c.txt & done; done; wait
