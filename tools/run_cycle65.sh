#!/bin/bash
# Cycle 65: Gromark (base 10) with both alphabets arbitrary. Census of feasible primers, then hard-constrained annealing.
cd "${WORKDIR:-$(dirname "$0")}"
gcc -O3 -march=native -o c65 c65.c -lm
python3 gen65.py > /dev/null
txt(){ if [ $1 = K4 ]; then cat k4.txt; else grep "^$1 " ctl65.txt|cut -d' ' -f2; fi; }
for L in 4 5 6 7; do for n in K4 CTL1 CTL2 CTL3 CTL4 NULL0 NULL1 NULL2 NULL3 NULL4 NULL5; do echo "$n $(./c65 census $(txt $n) $L|tail -1)" & done; wait; done > census.out
for n in K4 CTL1 CTL2 CTL3 CTL4 NULL0 NULL2 NULL5; do ./c65 sa $(txt $n) 5 qg.bin 6 400000 7 > sa5_$n.out & done; wait
for s in 11 12 13 14; do ./c65 sa $(txt K4) 5 qg.bin 12 600000 $s > sa5b_K4_s$s.out & ./c65 sa $(txt CTL4) 5 qg.bin 12 600000 $s > sa5b_CTL4_s$s.out & done; wait
for p in 0 1 2 3 4 5; do ./c65 sa $(txt K4) 6 qg.bin 8 400000 21 $p 6 > sa6_K4_p$p.out & done
for s in 31 32; do ./c65 sa $(txt NULL5) 5 qg.bin 12 600000 $s > sa5b_NULL5_s$s.out & done; wait
echo DONE
