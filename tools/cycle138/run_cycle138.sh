#!/bin/bash
# Cycle 138: CT-fed autokey with the key letter read through the free plaintext alphabet x.
# Needs: ctself2 (gcc -O2 -march=native ctself2.c), quad.bin (26^4 float32 log10 quadgrams,
# built from quadgrams.json), words601.txt (first 600 words of cycle 131's all.txt + "A"),
# controls.txt from plant.py. Direct pass used the older ctself (no language score).
set -e
W=${W:-/workspace/k138}; P=/home/box/kryptos_support_backup/perms97.bin; cd "$W"
K=$(cat /tmp/kcf/data/k4.txt)
for i in 1 2 3; do C=$(sed -n ${i}p controls.txt|cut -d' ' -f2); ./ctself2 $C words601.txt $P ctl$i 0 7 16 > b_ctl$i.txt & done; wait
for c in 0 1 2 3 4 5 6 7; do ./ctself2 $K words601.txt $P K4 $((c*30)) $((c*30+30)) 16 > k4_$c.txt & done; wait
for z in 1 2; do N=$(grep "^null$z" controls.txt|cut -d' ' -f2)
  for c in 0 1 2 3; do ./ctself2 $N words601.txt $P null$z $((c*60)) $((c*60+60)) 16 10 > n${z}_$c.txt & done; done; wait
