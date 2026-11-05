#!/bin/sh
# Cycle 62: exact autokey (CT/PT-fed, Vig/Beau/variant, both layer orders, lags 1-96) behind cycle 61's 6,070
# spiral and diagonal routes. Needs route_perm.bin (tools/route_gen61.py) and data/tw_alpha.bin.
set -e
head -c $((264*26)) data/tw_alpha.bin > a264.bin; head -c $((41*26)) data/tw_alpha.bin > a41.bin
gcc -O3 -march=native -fopenmp tools/autokey_exact60.c -o ak60
python3 tools/autokey_gen62.py a41.bin route_perm.bin data/cycle62     # planted controls (seed 62)
for c in actl0 actl1 actl2 actl3; do ./ak60 route_perm.bin 97 a41.bin 41 data/cycle62/$c.txt 0 96 10; done
./ak60 route_perm.bin 97 a41.bin 41 data/cycle62/actl3.txt 0 96 6      # B/PT control only reaches n = 6
for c in data/k4.txt data/cycle61/null0.txt data/cycle61/null1.txt data/cycle61/null2.txt; do
  ./ak60 route_perm.bin 97 a264.bin 264 $c 0 96 10
done
