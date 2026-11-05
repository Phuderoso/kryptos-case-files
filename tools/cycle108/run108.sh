#!/bin/sh
# Cycle 108: feedback-key cipher behind 165,065 transpositions (perms97.bin from tools/export_perms.py).
gcc -O2 -o fbkey fbkey.c && gcc -O2 -DLMAX=8 -o fbkey8 fbkey.c
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
./fbkey $K4 perms97.bin 165065 | tail -1
./fbkey8 $K4 perms97.bin 165065 | tail -1
python3 ctl108.py
