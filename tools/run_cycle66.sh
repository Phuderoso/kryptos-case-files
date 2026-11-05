#!/bin/bash
# Cycle 66: four-square with arbitrary cipher squares; themed plain squares; 26- and 36-cell shapes; direct + 96,630 transpositions, both orders.
cd "${WORKDIR:-$(dirname "$0")}"
gcc -O3 -march=native -o c66 c66.c
python3 gen66.py > ctl66.txt; python3 mknulls66.py
mkdir -p out
while read name ct rest; do for s in 0 1 2 3; do ./c66 $ct a264.bin c12_perm.bin $s > out/${name}_s$s.out & done; wait; done < ctl66.txt
echo DONE
# pass 2: 20 more shuffled nulls (seeds 6605-6624) for a wider null range
while read name ct; do for s in 0 1 2 3; do ./c66 $ct a264.bin c12_perm.bin $s > out/${name}_s$s.out & done; [ $((++i % 2)) = 0 ] && wait; done < nulls_extra.txt; wait
python3 summarize66.py > results66.txt
