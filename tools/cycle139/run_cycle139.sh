#!/bin/bash
# Cycle 139: PT-fed autokey with a free plaintext alphabet, tested on crib-to-crib links only.
# Needs ptfree (gcc -O2 -march=native ptfree.c), allA.txt (cycle 131's all.txt + "A"),
# words601.txt (first 600 words + "A"), controls.txt from plant.py.
set -e
W=${W:-/workspace/k139}; P=/home/box/kryptos_support_backup/perms97.bin; cd "$W"
K=$(cat /tmp/kcf/data/k4.txt)
for l in K4 null1 null2; do T=$([ $l = K4 ] && echo $K || grep "^$l" controls.txt|cut -d' ' -f2)
  MINCHK=4 MINBITS=18.8 ./ptfree $T allA.txt - D$l 0 10057 > direct_$l.txt; done
for c in 0 1 2 3 4 5 6 7; do ./ptfree $K words601.txt $P K4 $((c*76)) $((c*76+76)) > bank_K4_$c.txt & done; wait
for z in 1 2; do N=$(grep "^null$z" controls.txt|cut -d' ' -f2)
  for c in 0 1 2 3; do ./ptfree $N words601.txt $P null$z $((c*151)) $((c*151+151)) 10 > bank_null${z}_$c.txt & done; done; wait
