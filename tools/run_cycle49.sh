#!/bin/bash
# Cycle 49: Bazeries digit-group reversal x mono / periodic key, exact crib test.
cd "$(dirname "$0")"; gcc -O3 -march=native -o /tmp/bazeries bazeries.c
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
/tmp/bazeries $K4 7 1 > k4_d1_7.out
for s in 0 1 2 3 4 5; do /tmp/bazeries $K4 8 8 $s 6 > k4_d8_$s.out & done; wait
# controls/nulls: python3 ctl49.py > ctl49.txt; while read n c; do /tmp/bazeries $c 7 | grep -cE '^(MONO|PER)'; done < ctl49.txt
