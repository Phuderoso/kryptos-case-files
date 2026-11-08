#!/bin/bash
# Cycle 142: Hill 6x6 direct, every alignment o=0..5, A-Z/KRYPTOS numbering; K4 and 20 shuffled nulls, 500 restarts each.
# Needs hilln (gcc -O2 -march=native hilln.c), controls.txt from plant.py, texts.txt (K4 + nulls).
W=${W:-/workspace/k142}; cd "$W"
while read nm o nu t; do RESTARTS=300 ./hilln $t 6 $o $nu $nm; done < <(grep "^ctl" controls.txt) > controls_check.txt
s=$(date +%s)
while read nm t; do for o in 0 1 2 3 4 5; do for nu in 0 1; do echo "$t $o $nu $nm"; done; done; done < texts.txt |
  xargs -P 8 -L 1 sh -c 'RESTARTS=500 SEED=$(( $2*2+$3+1 )) ./hilln $1 6 $2 $3 $4' sh > results.txt
echo "T $(( $(date +%s)-s ))" > time.txt
