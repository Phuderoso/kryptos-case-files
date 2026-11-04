#!/bin/sh
# Cycle 41: progressive keyword key (key_i = k[i mod L] + s*floor(i/L)) on either side of 165,065 transpositions (incl. identity).
# Needs perms97.bin and qg.bin (as in cycles 39-40).
cd "$(dirname "$0")"
gcc -O3 -march=native -o progkw progkw.c
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
./progkw $K4 perms97.bin qg.bin > r_k4.txt &
for s in $(seq 1 20); do ./progkw $(python3 progkw_controls.py null $s) perms97.bin qg.bin > r_null$s.txt & done
for s in $(seq 51 60); do ./progkw $(python3 progkw_controls.py control $s 2>meta_ctl$s.txt) perms97.bin qg.bin > r_ctl$s.txt & done
wait
python3 progkw_summarize.py > summary.txt
