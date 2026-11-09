#!/bin/bash
# Cycle 192 registered run (PREREG192). Every job under setsid timeout; order = priority. Binary: run/cmp192 (tools/cycle192/cmp192.c,
# gcc -O3 -march=native -fopenmp -lm). Support as cycle 191 (all.bin 165,782 routes, all_s512, direct, slice191, tab2, tab4, tp_c3, tp_themed,
# tp_vocab). Pair lists (fixed before any K4 run from the structure-only pass on the reserved shuffle, mode 2): pairs_c1 (all_s512 U x 512 <= 1:
# P 138 / C 118), pairs_c3 (572 x U_s512 <= 1: 254), pairs_c2t (20,592 x U_direct <= 1: P 166), pairs_c2v (75,292 x U_direct <= 1: P 138).
W=${W:-/workspace/k4c192/w}; cd $W; mkdir -p run/out/c2t run/out/c2v run/out/c3 run/grid run/rc; K4=$(cat run/k4.txt); C=$W/run/cmp192; S=$W/support
t0=$(date +%s); el(){ echo $(( $(date +%s)-t0 )); }
# C1: K4, tab2, all 165,782 routes, candidate pairs, mode 0, print fits with U <= 0.002
OMP_NUM_THREADS=8 setsid timeout 420 $C $K4 $S/all.bin $S/tab2.txt k4 0 999999 run/pairs_c1.txt 0.002 0 > run/out/c1_k4_full.txt; echo "C1 done $(el) s"
# Grid: K4 + 19 shuffles (seeds 19211-19229), tab2 on all_s512, ALL 600 pairs, mode 0
{ echo "k4 $K4"; cat run/nulls192.txt; } > run/grid/texts.txt
while read lab ct; do OMP_NUM_THREADS=8 setsid timeout 30 $C $ct $S/all_s512.bin $S/tab2.txt $lab 0 999999 run/pairs_all.txt 0.002 0 | grep -v '^H' > run/grid/g512_$lab.txt; done < run/grid/texts.txt; echo "grid done $(el) s"
# C3: 572 themed x {A-Z, KRYPTOS} pairs on all_s512, pairs_c3
for f in $S/tp_c3/*.txt; do OMP_NUM_THREADS=8 setsid timeout 90 $C $K4 $S/all_s512.bin $f k4 0 999999 run/pairs_c3.txt 0.002 0 | awk -f tools/agg192.awk > run/out/c3/$(basename $f); done; echo "C3 done $(el) s"
# Recount: recount192.py (independent) vs cmp192 (all fits) on slice191 (7 rows), tab4, all 600 pairs, texts K4, P1, P2, P7, n19211 (5 parallel)
python3 -c "
with open('run/pairs_rcall.txt','w') as o:
  [o.write(f'{md} {m} {n}\n') for md in 'PC' for m in range(2,27) for n in range(2,27) if m!=n]"
for lab in k4 P1 P2 P7 n19211; do ct=$(awk -v l=$lab '$1==l{print $NF}' run/grid/texts.txt run/plants192.txt | head -1); echo "$lab $ct"; done > run/rc/texts.txt
cat run/rc/texts.txt | xargs -P 5 -L 1 sh -c 'setsid timeout 240 python3 tools/recount192.py $1 '$S'/slice191.bin 0,1,2,3,4,5,6 '$S'/tab4.txt run/pairs_rcall.txt | sort > run/rc/r_$0.txt'
while read lab ct; do OMP_NUM_THREADS=8 setsid timeout 60 $C $ct $S/slice191.bin $S/tab4.txt $lab 0 99 run/pairs_rcall.txt 1e30 0 | awk '$1=="M"{print "F",$3,$6,$4,$5,$7,$8}' | sort > run/rc/c_$lab.txt
  cmp -s run/rc/r_$lab.txt run/rc/c_$lab.txt && echo "recount $lab identical $(wc -l < run/rc/c_$lab.txt)" || echo "recount $lab DIFFER"; done < run/rc/texts.txt; echo "recount done $(el) s"
# C2t: direct, 20,592 themed x themed ordered pairs, pairs_c2t
ls $S/tp_themed/*.txt | OMP_NUM_THREADS=1 xargs -P 8 -I{} sh -c 'setsid timeout 60 '$C' '$K4' '$S'/direct.bin {} k4 0 1 run/pairs_c2t.txt 0.002 0 | awk -f tools/agg192.awk > run/out/c2t/$(basename {})'; echo "C2t done $(el) s"
# C2v (lowest priority): direct, 75,292 vocabulary-keyed x {A-Z, KRYPTOS} pairs, pairs_c2v
ls $S/tp_vocab/*.txt | OMP_NUM_THREADS=1 xargs -P 8 -I{} sh -c 'setsid timeout 60 '$C' '$K4' '$S'/direct.bin {} k4 0 1 run/pairs_c2v.txt 0.002 0 | awk -f tools/agg192.awk > run/out/c2v/$(basename {})'; echo "C2v done $(el) s"
