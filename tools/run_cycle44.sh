#!/bin/sh
# Cycle 44: rail fence / Redefence / AMSCO transpositions x periodic or progressive keyword substitution.
# railamsco.c = progkw.c (cycle 41) with an optional SMAX env cap on the step s; perms from railamsco_gen.py.
# Needs qg.bin (as in cycles 39-41) and progkw_controls.py (cycle 41) in the same directory.
cd "$(dirname "$0")"
gcc -O3 -march=native -o railamsco railamsco.c
python3 railamsco_gen.py A; python3 railamsco_gen.py B      # A: rail+Redefence+AMSCO w2-8 (422,433); B: AMSCO w9 (1,451,521)
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
ln -sf perms_A.bin perms97.bin
./railamsco $K4 perms_A.bin qg.bin > rA_k4.txt
./railamsco $K4 perms_B.bin qg.bin > rB_k4.txt
for s in $(seq 1 10); do ./railamsco $(python3 progkw_controls.py null $s) perms_A.bin qg.bin > rA_null$s.txt; done
for s in $(seq 1 5); do ./railamsco $(python3 progkw_controls.py null $s) perms_B.bin qg.bin > rB_null$s.txt; done
for s in $(seq 61 66); do python3 progkw_controls.py control $s > ctlA$s.txt 2>metaA$s.txt; ./railamsco $(head -1 ctlA$s.txt) perms_A.bin qg.bin > rA_ctl$s.txt; done
# family-B controls: generate with perms_B.bin linked as perms97.bin in ./cb, run on a +-2000 window around the planted perm
python3 railamsco_ctl0.py 50 7 > ctl0_rail.txt; python3 railamsco_ctl0.py 3000 8 > ctl0_redef.txt   # s=0 periodic controls (ABSCISSA, KA)
python3 railamsco_summarize.py > summary.txt
