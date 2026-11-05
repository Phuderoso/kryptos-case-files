#!/bin/sh
# Cycle 59: K3's rotation as a decimation; decimation family behind periodic keys (exact on the 24 crib letters).
set -e
python3 tools/k3_as_decimation.py                 # shows K3 = step +192 mod 337
python3 tools/decimation_gen.py                   # writes dec_perm.bin/.txt (new perms vs cycle-12 set)
gcc -O3 -march=native -fopenmp tools/periodic_exact59.c -o periodic_exact59
head -c $((264*26)) data/tw_alpha.bin > a264.bin; head -c 52 data/tw_alpha.bin > a2.bin
for c in k4 null0 null1 null2 ctl1 ctl2; do ./periodic_exact59 dec_perm.bin a264.bin 264 data/cycle59/$c.txt 16 12; done
for c in k4 null0 null1 null2 ctl1; do ./periodic_exact59 dec_perm.bin a2.bin 2 data/cycle59/$c.txt 26 26 > /dev/null; done
./periodic_exact59 dec_perm.bin data/tw_alpha.bin 20946 data/cycle59/k4.txt 12 8
