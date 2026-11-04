#!/bin/bash
# Cycle 50: Nihilist transposition (10x10 square, rows and columns reordered by the same sigma) x periodic/progressive
# keyword key, exact crib test. Checkpoint: sigma[0] = 0..7 done in cycle 50; 8 and 9 still to run.
cd "$(dirname "$0")"; gcc -O3 -march=native -o /tmp/nihilist nihilist.c
QG=${QG:-qg.bin}   # 26^4 float32 log-probabilities, built from data/quadgrams.json
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
for s in 0 1 2 3 4 5 6 7; do /tmp/nihilist $K4 $QG $s > k4_s$s.out & done; wait
# controls: python3 ctl50.py > ctl50.txt; while read n c; do MAXSIG=2000 /tmp/nihilist $c $QG 0 | grep HIT; done < <(grep CTL ctl50.txt)
# nulls:    while read n c; do MAXSIG=60000 /tmp/nihilist $c $QG 0 > $n.out; done < <(grep NULL ctl50.txt)
# next cycle: PRINTL=19 LMAX=19 /tmp/nihilist $K4 $QG 7   (print the single L=19 consistent config)
