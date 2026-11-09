#!/bin/bash
# Cycle 187 main run (I-164 via I-179; resumable: outputs ending in END are skipped). W = scratch with run/{lrk186,lrk186safe,lrk185,
# k4.txt,nulls187.txt,i176_texts187.txt,rc_texts.txt} and support/{all.bin,all_s8,all_s512,all_s20000,all_r1024s2048,slice187}.bin + lists.
# Every heavy command: OMP 6 threads, `setsid timeout` (own session / process group, so a timeout kills only that job).
# Order = priority: C1 K4 f L 1-3 full set (8 chunks); grid K4 + 19 nulls f and r on all_s512; audit main vs SAFE on all_s20000 (f, r);
# C2 K4 r L 1-3 on all_s8; recount (slice); add-on I-176 only if the heavy total so far + 110 s <= 480 s (BUDGET0 = seconds spent before).
W=${W:-/workspace/k4c187/w}; T=${T:-/tmp/kcf/tools/cycle187}; BUDGET0=${BUDGET0:-17}; cd $W; mkdir -p run/out run/rc run/i176; K4=$(cat run/k4.txt)
job(){ f=$1; shift; [ -s $f ] && tail -1 $f | grep -q '^END' && return; OMP_NUM_THREADS=6 setsid timeout ${TO:-150} "$@" > $f.tmp && mv $f.tmp $f; }
A=support/all.bin; S8=support/all_s8.bin; S512=support/all_s512.bin; S20k=support/all_s20000.bin; V=support/alpha172.txt; TH=support/alpha_themed180.txt
t0=$(date +%s); echo $t0 > run/out/t_start.txt
for c in 0 1 2 3 4 5 6 7; do lo=$((c*20723)); hi=$(( c==7 ? 165782 : (c+1)*20723 )); job run/out/k4.f.full.c$c.txt run/lrk186 $K4 $A $TH $V k4 $lo $hi 1 1 3 q4f; done
echo "C1 done $(( $(date +%s)-t0 )) s"
for d in f r; do if [ $d = f ]; then XA=$TH; XB=$V; else XA=$V; XB=$TH; fi
  job run/out/k4.$d.s512.txt run/lrk186 $K4 $S512 $XA $XB k4 0 999999 1 1 3 q4$d
  while read lab ct; do job run/out/$lab.$d.s512.txt run/lrk186 $ct $S512 $XA $XB $lab 0 999999 1 1 3 q4$d; done < run/nulls187.txt
  job run/out/k4.$d.s20k.txt     run/lrk186     $K4 $S20k $XA $XB k4 0 999999 1 1 3 q4$d
  job run/out/k4.$d.s20ksafe.txt run/lrk186safe $K4 $S20k $XA $XB k4 0 999999 2 1 3 q4$d
done
echo "grid+audit done $(( $(date +%s)-t0 )) s"
job run/out/k4.r.s8.txt run/lrk186 $K4 $S8 $V $TH k4 0 999999 1 1 3 q4r
echo "C2 done $(( $(date +%s)-t0 )) s"
R=support/alpha_recount180.txt
while read lab ct; do job run/rc/c_$lab.txt run/lrk186 $ct support/slice187.bin $R $R $lab 0 999999 1 1 1 rc; done < run/rc_texts.txt
[ -s run/rc/recount187.txt ] && grep -q "DONE n18712" run/rc/recount187.txt || setsid timeout 120 python3 $T/recount187.py support/slice187.bin $R run/rc_texts.txt > run/rc/recount187.txt
python3 $T/cmprecount187.py run/rc/recount187.txt run/rc_texts.txt run/rc > run/rc/cmp187.txt
el=$(( $(date +%s)-t0 )); echo "recount done $el s"
if [ $((BUDGET0+el+110)) -le 480 ]; then
  while read lab ct; do TO=30 job run/i176/$lab.txt run/lrk185 $ct support/all_r1024s2048.bin $V $V $lab 0 999999 1 1 3 q4r; done < run/i176_texts187.txt
  echo "I-176 done $(( $(date +%s)-t0 )) s"
else echo "I-176 skipped (budget: $BUDGET0 + $el + 110 > 480)"; fi
date +%s > run/out/t_end.txt
