#!/bin/bash
# Cycle 191 registered run (PREREG191). Every job under setsid timeout; order = priority. Binary: run/cmp191 (tools/cycle191/cmp191.c,
# gcc -O3 -march=native -fopenmp -lm). Support: all.bin (165,782 routes), all_s512.bin, all_s2048.bin, direct.bin, slice191.bin
# (all.bin rows 0, 40000, 80000, 120000, 160000, 12345, 100000), tab2.txt (A-Z>KRYPTOS, KRYPTOS>A-Z), tab4.txt (+ A-Z>A-Z, KRYPTOS>KRYPTOS),
# tp_themed/ (20,592 ordered pairs of distinct themed alphabets, 64 per file), tp_vocab/ (75,292: each of 18,824 keyed alphabets with A-Z
# and KRYPTOS, both orders), tp_c3/ (572: each themed alphabet with A-Z and KRYPTOS, both orders).
W=${W:-/workspace/k4c191/w}; cd $W; mkdir -p run/out/c2t run/out/c2v run/out/c3 run/grid run/rc; K4=$(cat run/k4.txt); C=$W/run/cmp191; S=$W/support
t0=$(date +%s); el(){ echo $(( $(date +%s)-t0 )); }
# C1: K4, A-Z>KRYPTOS and KRYPTOS>A-Z, all 165,782 routes, models P and C, forms VV VB BV BB, 600 ordered pairs; print fits with E_config <= 0.002
OMP_NUM_THREADS=8 setsid timeout 330 $C $K4 $S/all.bin $S/tab2.txt k4 0 999999 26 0.002 > run/out/c1_k4_full.txt; echo "C1 done $(el) s"
# Grid: K4 + 19 nulls (seeds 19111-19129), tab2 on all_s512 (324 routes); print E_config <= 0.002
{ echo "k4 $K4"; cat run/nulls191.txt; } > run/grid/texts.txt
while read lab ct; do OMP_NUM_THREADS=8 setsid timeout 30 $C $ct $S/all_s512.bin $S/tab2.txt $lab 0 999999 26 0.002 > run/grid/g512_$lab.txt; done < run/grid/texts.txt; echo "grid done $(el) s"
# C3: K4, 572 themed x {A-Z, KRYPTOS} pairs (both orders) on all_s512 (324 routes)
for f in $S/tp_c3/*.txt; do OMP_NUM_THREADS=8 setsid timeout 60 $C $K4 $S/all_s512.bin $f k4 0 999999 26 0.002 > run/out/c3/$(basename $f); done; echo "C3 done $(el) s"
# C2t: K4 direct, 20,592 themed x themed ordered pairs (one route, 8 single-thread jobs)
ls $S/tp_themed/*.txt | OMP_NUM_THREADS=1 xargs -P 8 -I{} sh -c 'setsid timeout 60 '$C' '$K4' '$S'/direct.bin {} k4 0 1 26 0.002 > run/out/c2t/$(basename {})'; echo "C2t done $(el) s"
# Recount: recount191.py (independent literal tables + vectorised DFS) vs cmp191 (print all fits) on slice191 (7 rows), tab4, texts K4, P1, P2, P7, n19111
for lab in k4 P1 P2 P7 n19111; do ct=$(awk -v l=$lab '$1==l{print $NF}' run/grid/texts.txt run/plants191.txt | head -1)
  setsid timeout 120 python3 tools/recount191.py $ct $S/slice191.bin 0,1,2,3,4,5,6 $S/tab4.txt 26 | sort > run/rc/r_$lab.txt
  OMP_NUM_THREADS=8 setsid timeout 30 $C $ct $S/slice191.bin $S/tab4.txt $lab 0 99 26 1e30 | awk '$1=="M"{print "F",$3,$6,$4,$5,$7,$8,$10}' | sort > run/rc/c_$lab.txt
  cmp -s run/rc/r_$lab.txt run/rc/c_$lab.txt && echo "recount $lab identical $(wc -l < run/rc/c_$lab.txt)" || echo "recount $lab DIFFER"; done; echo "recount done $(el) s"
# C2v (lowest priority): K4 direct, 75,292 vocabulary-keyed x {A-Z, KRYPTOS} pairs
ls $S/tp_vocab/*.txt | OMP_NUM_THREADS=1 xargs -P 8 -I{} sh -c 'setsid timeout 60 '$C' '$K4' '$S'/direct.bin {} k4 0 1 26 0.002 > run/out/c2v/$(basename {})'; echo "C2v done $(el) s"
