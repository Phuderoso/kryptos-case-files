#!/bin/bash
# Cycle 99: self-key + periodic keyword. Needs the cycle 98 permutation files (perms97.bin, dec_perm.bin, route_perm.bin, affine.bin) and k4.txt.
set -e
gcc -O3 -march=native -o selfkey2 selfkey2.c
F="perms97.bin dec_perm.bin route_perm.bin affine.bin"
./selfkey2 $(cat k4.txt) 12 1 $F > k4_L1.out 2> k4_L1.err      # model C L 1-12, model P L 1
./selfkey2 $(cat k4.txt) 0 2 $F > k4_L2.out 2> k4_L2.err       # model P L 1-2 (split across cores in practice)
python3 ctl99.py > controls.txt
