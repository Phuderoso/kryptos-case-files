#!/bin/sh
# Cycle 72 audit: Sanborn-convention end-to-end controls for the cycle 41 and cycle 59 solvers; K4 rerun of cycle 41.
# Needs perms97.bin and qg.bin (cycles 39-41) in tools/. Run from tools/.
set -e
cd "$(dirname "$0")"
gcc -O3 -march=native -o progkw progkw.c
gcc -O3 -march=native -fopenmp periodic_exact59.c -o periodic_exact59
for i in 0 1 2 3 4 5; do python3 sanborn_controls.py $i > c$i.txt 2> m$i.json
  p=$(python3 -c "import json;print(json.load(open('m$i.json'))['perm'])"); a=$((p>500?p-500:0))
  ./progkw $(cat c$i.txt) perms97.bin qg.bin $a $((p+500)) > r$i.txt; done
(cd .. && python3 tools/decimation_gen.py) && mv ../dec_perm.bin ../dec_perm.txt . 2>/dev/null || true
head -c 52 ../data/tw_alpha.bin > a2.bin
python3 sanborn_dec_controls.py
for n in 0 1 2 3; do ./periodic_exact59 dec_perm.bin a2.bin 2 d$n.txt 12 12 > dh$n.txt 2> ds$n.txt; done
./progkw OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR perms97.bin qg.bin > rk4_full.txt
