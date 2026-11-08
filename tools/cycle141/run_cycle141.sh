#!/bin/bash
# Cycle 141: Hill 5x5 direct and behind the 165k bank (both directions, model Q and carved), every alignment, A-Z/KRYPTOS numbering.
# Needs hill5 (gcc -O2 -march=native hill5.c), controls.txt from plant.py.
W=${W:-/workspace/k141}; P=/home/box/kryptos_support_backup/perms97.bin; cd "$W"
K=$(cat /tmp/kcf/data/k4.txt)
for c in ctl1 ctl2; do ./hill5 $(grep "^$c " controls.txt|cut -d' ' -f2) - $c 0 1 1; done > controls_check.txt
./hill5 $(grep "^ctl3 " controls.txt|cut -d' ' -f2) $P ctl3 4240 4245 1 >> controls_check.txt
ROWCAP=17576 COMBOCAP=2000000 ./hill5 $(grep "^ctl4 " controls.txt|cut -d' ' -f2) $P ctl4 160000 160001 1 >> controls_check.txt
./hill5 $(grep "^ctl5 " controls.txt|cut -d' ' -f2) $P ctl5 99999 100000 1 >> controls_check.txt
for l in K4 null1 null2; do T=$([ $l = K4 ] && echo $K || grep "^$l " controls.txt|cut -d' ' -f2)
  ./hill5 $T - D$l 0 1 1 > direct_$l.txt
  s=$(date +%s); for c in 0 1 2 3 4 5 6 7; do ./hill5 $T $P $l $((c*20634)) $((c*20634+20634)) 1 > bank_${l}_$c.txt & done; wait
  echo "T $l $(( $(date +%s)-s ))" >> time.txt; done
