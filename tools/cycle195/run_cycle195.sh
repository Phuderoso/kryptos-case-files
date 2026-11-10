#!/bin/bash
# Cycle 195 registered run (PREREG195). Every job under setsid timeout; order = priority. Solver: run/cmp193 (tools/cycle193/cmp193.c UNCHANGED,
# gcc -O3 -march=native -fopenmp -lm); only the permutation bank changes. Support: col1.bin (3,674 single keyed columnars = case 50's 1,837
# orders, perm + inverse), col2.bin (16,928 double keyed columnars over the 92 themed orders, perm + inverse, not in col1), col1_th.bin (184
# themed rows of col1), ctl195.bin (7 control rows), tab4.txt, tp_c3/ (572 themed x {A-Z, KRYPTOS} pairs, both orders). gen195.py, sub195.py.
W=${W:-/workspace/k4c195/w}; cd $W; mkdir -p run/out/c3 run/grid run/rc; K4=$(cat run/k4.txt); C=$W/run/cmp193; S=$W/support
t0=$(date +%s); el(){ echo $(( $(date +%s)-t0 )); }
# C1: K4, tab4, all 3,674 single keyed columnars, S1 + S2, forms VV VB BV BB, 625 ordered pairs (m = n included); print fits with E_config <= 0.002
OMP_NUM_THREADS=8 setsid timeout 120 $C $K4 $S/col1.bin $S/tab4.txt k4 0 999999 26 0.002 > run/out/c1_k4.txt; echo "C1 done $(el) s"
# C2: K4, tab4, all 16,928 themed double keyed columnars
OMP_NUM_THREADS=8 setsid timeout 240 $C $K4 $S/col2.bin $S/tab4.txt k4 0 999999 26 0.002 > run/out/c2_k4.txt; echo "C2 done $(el) s"
# Grid: K4 + 19 shuffles (seeds 19511-19529, nulls195.txt), tab4 on ALL of col1.bin; print E_config <= 0.002
{ echo "k4 $K4"; cat run/nulls195.txt; } > run/grid/texts.txt
while read lab ct; do OMP_NUM_THREADS=8 setsid timeout 60 $C $ct $S/col1.bin $S/tab4.txt $lab 0 999999 26 0.002 | grep -E '^(M|H|B|END)' > run/grid/g_$lab.txt; done < run/grid/texts.txt; echo "grid done $(el) s"
# C3: K4, 572 themed x {A-Z, KRYPTOS} tableau pairs on the 184 themed-keyword rows of col1 (col1_th.bin), H summed over tableau pairs (condensed on the fly)
for f in $S/tp_c3/*.txt; do OMP_NUM_THREADS=8 setsid timeout 90 $C $K4 $S/col1_th.bin $f k4 0 999999 26 0.002 1 > run/out/c3/$(basename $f); done; echo "C3 done $(el) s"
ls run/out/c3/*.txt | run/agg193 > run/agg_c3.txt
# Recount: recount195.py (= recount193.py, independent literal tables + vectorised DFS) vs cmp193 (all fits) on ctl195.bin (7 rows), tab4, texts K4, P1, P5, P6, n19511
for lab in k4 P1 P5 P6 n19511; do ct=$(awk -v l=$lab '$1==l{print $NF}' run/grid/texts.txt run/plants195.txt | head -1)
  ( setsid timeout 240 python3 tools/recount195.py $ct $S/ctl195.bin 0,1,2,3,4,5,6 $S/tab4.txt 26 | sort > run/rc/r_$lab.txt ) &
done; wait
for lab in k4 P1 P5 P6 n19511; do ct=$(awk -v l=$lab '$1==l{print $NF}' run/grid/texts.txt run/plants195.txt | head -1)
  OMP_NUM_THREADS=8 setsid timeout 30 $C $ct $S/ctl195.bin $S/tab4.txt $lab 0 99 26 1e30 | awk '$1=="M"{print "F",$3,$6,$4,$5,$7,$8,$10}' | sort > run/rc/c_$lab.txt
  cmp -s run/rc/r_$lab.txt run/rc/c_$lab.txt && echo "recount $lab identical $(wc -l < run/rc/c_$lab.txt)" || echo "recount $lab DIFFER"; done; echo "recount done $(el) s"
