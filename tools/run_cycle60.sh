#!/bin/sh
# Cycle 60: exact autokey (CT- and PT-fed; Vig/Beau/variant; both layer orders) behind K3-law decimations.
set -e
python3 tools/decimation_gen.py                   # dec_perm.bin: 159,712 N=97 decimations (cycle 59)
head -c $((264*26)) data/tw_alpha.bin > a264.bin; head -c $((41*26)) data/tw_alpha.bin > a41.bin
python3 tools/autokey_gen60.py data/k4.txt a264.bin dec_perm.bin   # dec98.bin ('?' + K4), planted controls
gcc -O3 -march=native -fopenmp tools/autokey_exact60.c -o ak60
./ak60 dec_perm.bin 97 a264.bin 264 data/cycle60/actl0.txt 0 96 10
for c in actl1 actl2 actl3; do ./ak60 dec_perm.bin 97 a41.bin 41 data/cycle60/$c.txt 0 96 10; done
for c in k4 null0; do ./ak60 dec_perm.bin 97 a264.bin 264 data/cycle59/$c.txt 0 96 10; done
for c in k4q null0q; do ./ak60 dec98.bin 98 a41.bin 41 data/cycle60/$c.txt 1 97 10; done
