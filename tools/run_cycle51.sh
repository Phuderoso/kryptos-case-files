#!/bin/bash
# Cycle 51: finish the Nihilist transposition checkpoint (sigma[0] = 8, 9), print the single L=19 config, matched nulls.
cd "$(dirname "$0")"; gcc -O3 -march=native -o /tmp/nihilist nihilist.c
QG=${QG:-qg.bin}
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
for s in 8 9; do /tmp/nihilist $K4 $QG $s > k4_s$s.out & done
PRINTL=19 LMAX=19 /tmp/nihilist $K4 $QG 7 > k4_L19.out &
wait
MAXSIG=60000 /tmp/nihilist $K4 $QG 8 > k4_s8_matched.out
PRINTL=20 LMAX=20 MAXSIG=60000 /tmp/nihilist $K4 $QG 8 > k4_s8_L20.out
while read n c; do MAXSIG=60000 /tmp/nihilist $c $QG 8 > ${n}_s8.out; done < <(grep NULL ../data/cycle50/ctl50.txt)
