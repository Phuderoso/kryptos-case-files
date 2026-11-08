#!/bin/bash
# Cycle 143: affine Hill (Hill + period-n additive key) n = 2..5, direct and behind the 165k bank
# (both directions, model Q and carved), every alignment, A-Z/KRYPTOS numbering. K4 and 2 nulls, full bank.
# Needs hillaff (gcc -O2 -march=native hillaff.c) and controls.txt from plant.py.
W=${W:-/workspace/k143}; P=/home/box/kryptos_support_backup/perms97.bin; cd "$W"; K=$(cat /tmp/kcf/data/k4.txt)
{ for c in "ctl1 - 0" "ctl5 - 0"; do set -- $c; read nm n t < <(grep "^$1 " controls.txt); ./hillaff $t $2 $1 $3 1 1 $n; done
  for c in "ctl2 4240 4245" "ctl3 160000 160001" "ctl4 99999 100000" "ctl6 50000 50001" "ctl7 120000 120001" "ctl8 77777 77778"; do set -- $c
    read nm n t < <(grep "^$1 " controls.txt); ./hillaff $t $P $1 $2 $3 1 $n; done; } > controls_check.txt
s=$(date +%s)
for l in K4 null1 null2; do T=$([ $l = K4 ] && echo $K || grep "^$l " controls.txt|cut -d' ' -f3)
  for n in 2 3 4 5; do ./hillaff $T - D$l 0 1 1 $n > direct_${l}_n$n.txt
    for c in 0 1 2 3 4 5 6 7; do ./hillaff $T $P $l $((c*20634)) $((c*20634+20634)) 1 $n > bank_${l}_n${n}_$c.txt & done; wait; done; done
echo "T $(( $(date +%s)-s ))" > time.txt
