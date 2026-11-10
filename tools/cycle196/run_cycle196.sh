#!/bin/bash
# Cycle 196 registered run (PREREG196): ONE-ERROR audit of case 182 (sandwich compound key around a keyed columnar). Every job under setsid timeout;
# order = priority. Binary: run/cmp194 (tools/cycle194/cmp194.c UNCHANGED, gcc -O3 -march=native -fopenmp -lm); only the bank and pair lists change.
# Banks (cycle 195, hashes in tools/cycle195/sha195.txt): col1.bin 3,674 single keyed columnars; col2.bin 16,928 themed double keyed columnars.
# Pair lists fixed text-free by a structure pass (mode 2) over the WHOLE bank (exact cell U, no estimate): pairs_fp_col1.txt (139 per model),
# pairs_fp_col2.txt (136 per model), cell U <= 0.05. One-tableau stacks run VV/VB only (BB = VV, BV = VB exactly).
W=${W:-/workspace/k4c196/w}; cd $W; mkdir -p run/out run/grid run/rc; K4=$(cat run/k4.txt); C=$W/run/cmp194; S=$W/support
t0=$(date +%s); el(){ echo $(( $(date +%s)-t0 )); }; echo "registered run start $(date +%T) PT"
# C1: K4, col1, two-tableau (tab2, 4 forms) then one-tableau (tab1s, VV/VB); print every fit with config U <= 0.05 (all fits of full-power cells)
OMP_NUM_THREADS=8 setsid timeout 120 $C $K4 $S/col1.bin $S/tab2.txt k4 0 999999 run/pairs_fp_col1.txt 0.05 0 15 > run/out/c1a_k4.txt; echo "C1a done $(el) s"
OMP_NUM_THREADS=8 setsid timeout 120 $C $K4 $S/col1.bin $S/tab1s.txt k4 0 999999 run/pairs_fp_col1.txt 0.05 0 3 > run/out/c1b_k4.txt; echo "C1b done $(el) s"
# C2: K4, col2, same
OMP_NUM_THREADS=8 setsid timeout 200 $C $K4 $S/col2.bin $S/tab2.txt k4 0 999999 run/pairs_fp_col2.txt 0.05 0 15 > run/out/c2a_k4.txt; echo "C2a done $(el) s"
OMP_NUM_THREADS=8 setsid timeout 200 $C $K4 $S/col2.bin $S/tab1s.txt k4 0 999999 run/pairs_fp_col2.txt 0.05 0 3 > run/out/c2b_k4.txt; echo "C2b done $(el) s"
# Grid: K4 + 19 shuffles (seeds 19611-19629, nulls196.txt), tab2 (4 forms) + tab1s (VV/VB) on col1_s8 (= col1.bin[::8], 460 rows), ALL 625 pairs;
# gate: the grid starts only if elapsed <= 150 s (else reported as not run)
{ echo "k4 $K4"; cat run/nulls196.txt; } > run/grid/texts.txt
if [ $(el) -le 150 ]; then while read lab ct; do for tf in "tab2 15" "tab1s 3"; do set -- $tf
  OMP_NUM_THREADS=8 setsid timeout 30 $C $ct $S/col1_s8.bin $S/$1.txt $lab 0 999999 run/pairs_all.txt 0.002 0 $2 | grep -E '^(B|M|END)' > run/grid/g_${lab}_$1.txt; done; done < run/grid/texts.txt; echo "grid done $(el) s"
else echo "grid NOT RUN (budget gate)"; fi
# Recount: recount196.py (independent, all 25 deletions, no reduction) vs cmp194 (all fits, U <= 1e30) on ctl195.bin (7 rows), ALL 1,250 model-pairs,
# tab2 x 4 forms + tab1s x VV/VB, texts K4, P1, P5, P6, n19611
for lab in k4 P1 P5 P6 n19611; do ct=$(awk -v l=$lab '$1==l{print $NF}' run/grid/texts.txt run/plants196.txt | head -1); echo "$lab $ct"; done > run/rc/texts.txt
while read lab ct; do ( setsid timeout 150 python3 tools/recount196.py $ct $S/ctl195.bin 0,1,2,3,4,5,6 $S/tab2.txt run/pairs_all_x.txt > run/rc/r2_$lab.txt ) &
  ( setsid timeout 150 python3 tools/recount196.py $ct $S/ctl195.bin 0,1,2,3,4,5,6 $S/tab1s.txt run/pairs_all_x.txt VV,VB > run/rc/r1_$lab.txt ) & done < run/rc/texts.txt; wait
while read lab ct; do cat run/rc/r2_$lab.txt run/rc/r1_$lab.txt | sort > run/rc/r_$lab.txt
  { OMP_NUM_THREADS=8 setsid timeout 30 $C $ct $S/ctl195.bin $S/tab2.txt $lab 0 99 run/pairs_all.txt 1e30 0 15; OMP_NUM_THREADS=8 setsid timeout 30 $C $ct $S/ctl195.bin $S/tab1s.txt $lab 0 99 run/pairs_all.txt 1e30 0 3; } | awk '$1=="M"{print "F",$3,$6,$4,$5,$7,$8}' | sort > run/rc/c_$lab.txt
  cmp -s run/rc/r_$lab.txt run/rc/c_$lab.txt && echo "recount $lab identical $(wc -l < run/rc/c_$lab.txt)" || echo "recount $lab DIFFER"; done < run/rc/texts.txt; echo "recount done $(el) s"
echo "registered run end $(date +%T) PT ($(el) s)"
