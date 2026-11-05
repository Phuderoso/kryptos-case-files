#!/bin/sh
# Cycle 61: spiral and diagonal route transpositions behind periodic Quagmire III keys (exact on the 24 crib letters).
set -e
python3 tools/route_gen61.py   # writes route_perm.bin, data/cycle61 nulls + planted controls
gcc -O3 -march=native -fopenmp tools/periodic_exact59.c -o periodic_exact59
head -c $((264*26)) data/tw_alpha.bin > a264.bin; head -c 52 data/tw_alpha.bin > a2.bin
for c in data/k4.txt data/cycle61/null0.txt data/cycle61/null1.txt data/cycle61/null2.txt data/cycle61/ctl1.txt data/cycle61/ctl2.txt data/cycle61/ctl3.txt; do
  ./periodic_exact59 route_perm.bin a264.bin 264 $c 20 12
  ./periodic_exact59 route_perm.bin a2.bin 2 $c 26 26 > /dev/null
done
for c in data/k4.txt data/cycle61/null0.txt data/cycle61/null1.txt data/cycle61/null2.txt data/cycle61/ctl1.txt; do
  ./periodic_exact59 route_perm.bin data/tw_alpha.bin 20946 $c 14 10
done
