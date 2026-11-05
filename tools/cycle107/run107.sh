#!/bin/sh
# Cycle 107: W-triggered Alberti disk. Needs perms97.bin from tools/export_perms.py (165,065 transpositions).
gcc -O2 -o wturn wturn.c
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
./wturn $K4 perms97.bin 165065 | grep -E 'TOP|HIST|MONO|RESULT'
python3 ctl107.py
python3 fixed_ring.py 121558
