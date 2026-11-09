#!/bin/bash
# Cycle 188 main run (I-185 + I-183 add-on; resumable: outputs ending in END are skipped). W = scratch with run/{lrk188,lrk188safe,
# lrk186,k4.txt,nulls188.txt,rc_texts.txt,i183_texts188.txt} and support/{all,all_s512,all_s20000,all_r256s512,slice188}.bin + lists.
# Every heavy command: OMP 6 threads, `setsid timeout` (own session / process group, so a timeout kills only that job).
# Order = priority: C1 K4 f L 1-2 full set (8 chunks); grid K4 + 19 nulls f and r L 1-2 on all_s512; audit main vs SAFE L 1-3 on
# all_s20000 (f, r); recount (slice); C3 K4 f and r L 1-3 on all_s512; add-on I-183 if BUDGET0 + elapsed + 40 <= 470;
# C2 K4 r L 1-2 full set, 8 chunks, each only if BUDGET0 + elapsed + 18 <= 475 (a chunk without END = not run).
W=${W:-/workspace/k4c188/w}; T=${T:-/tmp/kcf/tools/cycle188}; BUDGET0=${BUDGET0:-45}; cd $W; mkdir -p run/out run/rc run/i183; K4=$(cat run/k4.txt)
job(){ f=$1; shift; [ -s $f ] && tail -1 $f | grep -q '^END' && return; OMP_NUM_THREADS=6 setsid timeout ${TO:-150} "$@" > $f.tmp && mv $f.tmp $f; }
A=support/all.bin; S512=support/all_s512.bin; S20k=support/all_s20000.bin; V=support/alpha172.txt; TH=support/alpha_themed180.txt
t0=$(date +%s); echo $t0 > run/out/t_start.txt; el(){ echo $(( $(date +%s)-t0 )); }
for c in 0 1 2 3 4 5 6 7; do lo=$((c*20723)); hi=$(( c==7 ? 165782 : (c+1)*20723 )); job run/out/k4.f.full.c$c.txt run/lrk188 $K4 $A $TH $V k4 $lo $hi 1 1 2 q4f; done
echo "C1 done $(el) s"
for d in f r; do if [ $d = f ]; then XA=$TH; XB=$V; else XA=$V; XB=$TH; fi
  job run/out/k4.$d.s512.txt run/lrk188 $K4 $S512 $XA $XB k4 0 999999 1 1 2 q4$d
  while read lab ct; do job run/out/$lab.$d.s512.txt run/lrk188 $ct $S512 $XA $XB $lab 0 999999 1 1 2 q4$d; done < run/nulls188.txt
  job run/out/k4.$d.s20k.txt     run/lrk188     $K4 $S20k $XA $XB k4 0 999999 1 1 3 q4$d
  job run/out/k4.$d.s20ksafe.txt run/lrk188safe $K4 $S20k $XA $XB k4 0 999999 2 1 3 q4$d
done
echo "grid+audit done $(el) s"
R=support/alpha_recount180.txt
while read lab ct; do job run/rc/c_$lab.txt run/lrk188 $ct support/slice188.bin $R $R $lab 0 999999 1 1 1 rc; done < run/rc_texts.txt
[ -s run/rc/recount188.txt ] && grep -q "DONE n18812" run/rc/recount188.txt || setsid timeout 120 python3 $T/recount188.py support/slice188.bin $R run/rc_texts.txt > run/rc/recount188.txt
python3 $T/cmprecount188.py run/rc/recount188.txt run/rc_texts.txt run/rc > run/rc/cmp188.txt
echo "recount done $(el) s"
job run/out/k4.f.s512L3.txt run/lrk188 $K4 $S512 $TH $V k4 0 999999 1 1 3 q4f
job run/out/k4.r.s512L3.txt run/lrk188 $K4 $S512 $V $TH k4 0 999999 1 1 3 q4r
echo "C3 done $(el) s"
if [ $((BUDGET0+$(el)+40)) -le 470 ]; then
  while read lab ct; do TO=30 job run/i183/$lab.txt run/lrk186 $ct support/all_r256s512.bin $V $TH $lab 0 999999 1 1 3 q4r; done < run/i183_texts188.txt
  echo "I-183 done $(el) s"
else echo "I-183 skipped (budget)"; fi
for c in 0 1 2 3 4 5 6 7; do lo=$((c*20723)); hi=$(( c==7 ? 165782 : (c+1)*20723 ))
  if [ $((BUDGET0+$(el)+18)) -le 475 ]; then job run/out/k4.r.full.c$c.txt run/lrk188 $K4 $A $V $TH k4 $lo $hi 1 1 2 q4r; else echo "C2 chunk $c skipped (budget)"; fi; done
echo "C2 done $(el) s"
date +%s > run/out/t_end.txt
