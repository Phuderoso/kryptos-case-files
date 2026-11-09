#!/bin/bash
# Cycle 193 registered run (PREREG193). Every job under setsid timeout; order = priority. Binary: run/cmp193 (tools/cycle193/cmp193.c,
# gcc -O3 -march=native -fopenmp -lm). Support (unchanged from cycles 191-192): all.bin (165,782 routes), all_s512.bin, slice191.bin
# (all.bin rows 0, 40000, 80000, 120000, 160000, 12345, 100000), tab4.txt (A-Z>KRYPTOS, KRYPTOS>A-Z, A-Z>A-Z, KRYPTOS>KRYPTOS),
# tp_c3/ (572: each themed alphabet with A-Z and KRYPTOS, both orders).
W=${W:-/workspace/k4c193/w}; cd $W; mkdir -p run/out/c3 run/grid run/rc; K4=$(cat run/k4.txt); C=$W/run/cmp193; S=$W/support
t0=$(date +%s); el(){ echo $(( $(date +%s)-t0 )); }
# C1: K4, tab4, all 165,782 routes, models S1 and S2, forms VV VB BV BB, 625 ordered pairs (m = n included); print fits with E_config <= 0.002
OMP_NUM_THREADS=8 setsid timeout 420 $C $K4 $S/all.bin $S/tab4.txt k4 0 999999 26 0.002 > run/out/c1_k4_full.txt; echo "C1 done $(el) s"
# Grid: K4 + 19 shuffles (seeds 19311-19329, nulls193.txt), tab4 on all_s512 (324 routes); print E_config <= 0.002
{ echo "k4 $K4"; cat run/nulls193.txt; } > run/grid/texts.txt
while read lab ct; do OMP_NUM_THREADS=8 setsid timeout 30 $C $ct $S/all_s512.bin $S/tab4.txt $lab 0 999999 26 0.002 > run/grid/g512_$lab.txt; done < run/grid/texts.txt; echo "grid done $(el) s"
# C3: K4, 572 themed x {A-Z, KRYPTOS} pairs (both orders) on all_s512, H lines summed over the tableau pairs of each file (condensed on the fly)
for f in $S/tp_c3/*.txt; do OMP_NUM_THREADS=8 setsid timeout 90 $C $K4 $S/all_s512.bin $f k4 0 999999 26 0.002 1 > run/out/c3/$(basename $f); done; echo "C3 done $(el) s"
ls run/out/c3/*.txt | run/agg193 > run/agg_c3.txt
# Recount: recount193.py (independent literal tables + vectorised DFS) vs cmp193 (print all fits) on slice191 (7 rows), tab4, texts K4, P1, P2, P6, n19311
for lab in k4 P1 P2 P6 n19311; do ct=$(awk -v l=$lab '$1==l{print $NF}' run/grid/texts.txt run/plants193.txt | head -1)
  ( setsid timeout 200 python3 tools/recount193.py $ct $S/slice191.bin 0,1,2,3,4,5,6 $S/tab4.txt 26 | sort > run/rc/r_$lab.txt ) &
done; wait
for lab in k4 P1 P2 P6 n19311; do ct=$(awk -v l=$lab '$1==l{print $NF}' run/grid/texts.txt run/plants193.txt | head -1)
  OMP_NUM_THREADS=8 setsid timeout 30 $C $ct $S/slice191.bin $S/tab4.txt $lab 0 99 26 1e30 | awk '$1=="M"{print "F",$3,$6,$4,$5,$7,$8,$10}' | sort > run/rc/c_$lab.txt
  cmp -s run/rc/r_$lab.txt run/rc/c_$lab.txt && echo "recount $lab identical $(wc -l < run/rc/c_$lab.txt)" || echo "recount $lab DIFFER"; done; echo "recount done $(el) s"
