#!/bin/bash
# Cycle 188 add-on C (I-184, PREREG188b): case 174 direction r (A vocabulary x B themed), strict, L 1-3, lrk186 (cycle-187 binary,
# md5 4f41a243...) on the residue classes all.bin[r::8], r = 1..7 in order; class r runs only if HEAVY0 + elapsed + 32 <= 460
# (HEAVY0 = heavy seconds spent before this script). Each job under setsid timeout 60; a class without END = not run.
W=${W:-/workspace/k4c188/w}; HEAVY0=${HEAVY0:-290}; cd $W; mkdir -p run/i184; K4=$(cat run/k4.txt); V=support/alpha172.txt; TH=support/alpha_themed180.txt
t0=$(date +%s); el(){ echo $(( $(date +%s)-t0 )); }
for r in 1 2 3 4 5 6 7; do f=run/i184/k4.r.r${r}s8.txt
  if [ $((HEAVY0+$(el)+32)) -le 460 ]; then OMP_NUM_THREADS=6 setsid timeout 60 run/lrk186 $K4 support/all_r${r}s8.bin $V $TH k4 0 999999 1 1 3 q4r > $f.tmp && mv $f.tmp $f; echo "class $r done $(el) s"
  else echo "class $r skipped (budget: $HEAVY0 + $(el) + 32 > 460)"; fi; done
