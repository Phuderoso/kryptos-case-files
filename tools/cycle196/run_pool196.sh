#!/bin/bash
# Cycle 196 pooled reference for the grid rank flag (PREREG196b; I-182/I-203): 40 fresh shuffles (seeds 19631-19670, nulls196b.txt), the SAME cell
# as the flagged one: cmp194, tab2 (4 forms), col1_s8 (460 rows), ALL 625 pairs, print config U <= 0.002; then pool196.py.
W=${W:-/workspace/k4c196/w}; cd $W; mkdir -p run/pool; C=$W/run/cmp194; S=$W/support
while read lab ct; do OMP_NUM_THREADS=8 setsid timeout 30 $C $ct $S/col1_s8.bin $S/tab2.txt $lab 0 999999 run/pairs_all.txt 0.002 0 15 | grep -E '^(B|M|END)' > run/pool/g_${lab}_tab2.txt; done < run/nulls196b.txt
python3 tools/pool196.py run
