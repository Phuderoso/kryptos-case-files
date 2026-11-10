#!/bin/bash
# Cycle 194 registered run (PREREG194). Every job under setsid timeout; order = priority; budget gate on the one-tableau chunks.
# Binary: run/cmp194 (tools/cycle194/cmp194.c, gcc -O3 -march=native -fopenmp -lm). Support unchanged from cycles 191-193 (all.bin 165,782 routes,
# all_s2048 (81 routes), slice191 (7 rows), tab2 = A-Z>KRYPTOS, KRYPTOS>A-Z; tab1s = A-Z>A-Z, KRYPTOS>KRYPTOS).
# Pair list pairs_fp.txt (fixed before any K4 run, text-free: structure-only pass, mode 2, on the reserved shuffle 9191, all_s512, cell U
# estimate = U_s512 x 165,782/324 <= 0.05): 116 pairs per model. One-tableau files run forms VV, VB only (BB = VV, BV = VB exactly).
W=${W:-/workspace/k4c194/w}; cd $W; mkdir -p run/out run/grid run/rc; K4=$(cat run/k4.txt); C=$W/run/cmp194; S=$W/support
t0=$(date +%s); el(){ echo $(( $(date +%s)-t0 )); }; echo "registered run start $(date +%T) PT"
# C1a: K4, two-tableau (tab2, 4 forms), all routes, pairs_fp, mode 0, print every fit with U <= 0.05 (so every fit in a full-power cell is printed)
OMP_NUM_THREADS=8 setsid timeout 330 $C $K4 $S/all.bin $S/tab2.txt k4 0 999999 run/pairs_fp.txt 0.05 0 15 > run/out/c1a_k4.txt; echo "C1a done $(el) s"
# C1b: K4, one-tableau stacks (tab1s, VV/VB), all routes in 8 chunks of 20,723 rows; a chunk starts only if elapsed <= 390 s (budget gate)
for c in 0 1 2 3 4 5 6 7; do lo=$((c*20723)); hi=$(( c==7 ? 165782 : (c+1)*20723 ))
  if [ $(el) -gt 390 ]; then echo "C1b chunk $c ($lo-$hi) NOT RUN (budget gate)"; continue; fi
  OMP_NUM_THREADS=8 setsid timeout 60 $C $K4 $S/all.bin $S/tab1s.txt k4 $lo $hi run/pairs_fp.txt 0.05 0 3 > run/out/c1b_k4_$c.txt; echo "C1b chunk $c ($lo-$hi) done $(el) s"; done
# Grid: K4 + 19 shuffles (seeds 19411-19429, nulls194.txt), tab2 (4 forms) + tab1s (VV/VB) on all_s2048 (81 routes), ALL 625 pairs, B lines only
{ echo "k4 $K4"; cat run/nulls194.txt; } > run/grid/texts.txt
while read lab ct; do for tf in "tab2 15" "tab1s 3"; do set -- $tf
  OMP_NUM_THREADS=8 setsid timeout 30 $C $ct $S/all_s2048.bin $S/$1.txt $lab 0 999999 run/pairs_all.txt 0.002 0 $2 | grep -E '^(B|M|END)' > run/grid/g_${lab}_$1.txt; done; done < run/grid/texts.txt; echo "grid done $(el) s"
# Recount: recount194.py (independent, all 25 deletions, no reduction) vs cmp194 (all fits) on slice191 (7 rows), pairs_fp, tab2 x 4 forms + tab1s x VV/VB
for lab in k4 P1 P4 P7 n19411; do ct=$(awk -v l=$lab '$1==l{print $NF}' run/grid/texts.txt run/plants194.txt | head -1); echo "$lab $ct"; done > run/rc/texts.txt
cat run/rc/texts.txt | xargs -P 5 -L 1 sh -c '{ setsid timeout 120 python3 tools/recount194.py $1 '$S'/slice191.bin 0,1,2,3,4,5,6 '$S'/tab2.txt run/pairs_fp.txt; setsid timeout 120 python3 tools/recount194.py $1 '$S'/slice191.bin 0,1,2,3,4,5,6 '$S'/tab1s.txt run/pairs_fp.txt VV,VB; } | sort > run/rc/r_$0.txt'
while read lab ct; do { OMP_NUM_THREADS=8 setsid timeout 30 $C $ct $S/slice191.bin $S/tab2.txt $lab 0 99 run/pairs_fp.txt 1e30 0 15; OMP_NUM_THREADS=8 setsid timeout 30 $C $ct $S/slice191.bin $S/tab1s.txt $lab 0 99 run/pairs_fp.txt 1e30 0 3; } | awk '$1=="M"{print "F",$3,$6,$4,$5,$7,$8}' | sort > run/rc/c_$lab.txt
  cmp -s run/rc/r_$lab.txt run/rc/c_$lab.txt && echo "recount $lab identical $(wc -l < run/rc/c_$lab.txt)" || echo "recount $lab DIFFER"; done < run/rc/texts.txt; echo "recount done $(el) s"
echo "registered run end $(date +%T) PT ($(el) s)"
