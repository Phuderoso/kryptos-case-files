#!/bin/sh
# Cycle 106: Alberti cipher-disk family. Needs perms97.bin, alpha.bin (support backup) and tw264.bin in the cwd.
gcc -O3 -march=native -o alberti alberti.c
python3 ctl106.py
cat texts.txt | xargs -P 8 -L 1 sh -c './alberti $1 perms97.bin 165065 tw264.bin 264 10 > behind_$0.txt'
cat texts.txt | xargs -P 8 -L 1 sh -c './alberti $1 perms97.bin 1 alpha.bin 86731 12 > direct86k_$0.txt'
cat texts_sat.txt | xargs -P 8 -L 1 sh -c 'echo "$0 $(timeout 200 python3 alberti_maxsat.py $1)"' > maxsat_direct.txt
python3 audit104.py > audit104.txt
