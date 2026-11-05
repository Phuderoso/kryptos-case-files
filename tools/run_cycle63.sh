#!/bin/sh
# Cycle 63: exact Swagman (7x7 Latin key square) + periodic Vig/Beau (variant equivalent) before/after, 9 block configs.
set -e
head -c $((41*26)) data/tw_alpha.bin > a41.bin; head -c $((5*26)) data/tw_alpha.bin > a5.bin; head -c $((3*26)) data/tw_alpha.bin > a3.bin
gcc -O3 -march=native -fopenmp tools/swagman63.c -o sw63
python3 tools/swagman_gen63.py a41.bin data/cycle63            # planted controls (seed 63)
for c in 0 1 2 3 4; do ./sw63 a5.bin 5 data/cycle63/sctl$c.txt 7 3; done
for c in data/k4.txt data/cycle63/null0.txt data/cycle63/null1.txt data/cycle63/null2.txt; do
  ./sw63 a41.bin 41 $c 6 5      # 41 themed alphabets, p 1-6
  ./sw63 a3.bin 3 $c 8 5        # AZ, KA, ZA tableaux, p 1-8
done
