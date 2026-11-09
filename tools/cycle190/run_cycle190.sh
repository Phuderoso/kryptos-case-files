#!/bin/bash
# Cycle 190 registered run (PREREG190). Every job under setsid timeout; order = priority. Binary: run/cmp190 (tools/cycle190/cmp190.c,
# gcc -O3 -march=native -fopenmp). Support: all.bin, all_s512.bin, direct.bin, slice190.bin (all.bin rows 0, 80000, 12345, 100000, 51712),
# azka.txt (A-Z, KRYPTOS), alpha_themed180.txt (144), alpha_direct189.txt (18,824).
W=${W:-/workspace/k4c190/w}; cd $W; mkdir -p run/out run/rc run/grid; K4=$(cat run/k4.txt); C=run/cmp190; S=support
t0=$(date +%s); el(){ echo $(( $(date +%s)-t0 )); }
export OMP_NUM_THREADS=8
# C1: K4, A-Z/KRYPTOS, all 165,782 routes, models P and C, Vig/Beau, 260 pairs, one-error scope; print fits with ex_after >= 5
setsid timeout 300 $C $K4 $S/all.bin $S/azka.txt k4 0 999999 25 26 5 > run/out/c1_k4_full.txt; echo "C1 done $(el) s"
# C2: K4 direct, 18,824 keyed alphabets
setsid timeout 60 $C $K4 $S/direct.bin $S/alpha_direct189.txt k4 0 1 25 26 5 > run/out/c2_k4_direct.txt; echo "C2 done $(el) s"
# C3: K4, 144 themed alphabets on all_s512 (324 routes)
setsid timeout 90 $C $K4 $S/all_s512.bin $S/alpha_themed180.txt k4 0 999999 25 26 5 > run/out/c3_k4_s512_themed.txt; echo "C3 done $(el) s"
# Grid: K4 + 19 nulls (seeds 19011-19029): A-Z/KRYPTOS on all_s512 (8 threads each), then direct (8 single-thread jobs at a time); print ex_after >= 3
{ echo "k4 $K4"; cat run/nulls190.txt; } > run/grid/texts.txt
while read lab ct; do setsid timeout 30 $C $ct $S/all_s512.bin $S/azka.txt $lab 0 999999 25 26 3 > run/grid/g512_$lab.txt; done < run/grid/texts.txt
cat run/grid/texts.txt | OMP_NUM_THREADS=1 xargs -P 8 -L 1 sh -c 'setsid timeout 90 '$C' $1 '$S'/direct.bin '$S'/alpha_direct189.txt $0 0 1 25 26 3 > run/grid/gdir_$0.txt'
echo "grid done $(el) s"
# Recount: recount190.py (independent null-space algebra) vs cmp190 PE 0 on slice190 (5 rows), A-Z/KRYPTOS, texts K4, E1, E2, E6, n19011
setsid timeout 200 python3 tools/recount190.py $S/slice190.bin $S/azka.txt run/rc_texts.txt 25 26 > run/rc/recount.txt
while read lab ct; do setsid timeout 30 $C $ct $S/slice190.bin $S/azka.txt $lab 0 99 25 26 0 > run/rc/cmp_$lab.txt; done < run/rc_texts.txt; echo "recount done $(el) s"
