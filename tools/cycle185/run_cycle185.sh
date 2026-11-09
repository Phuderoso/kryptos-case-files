#!/bin/bash
# Cycle 185 main run (I-172; resumable: outputs ending in END are skipped). W = scratch with run/{lrk185,lrk185safe,k4.txt,nulls185.txt}
# and support/{all.bin,all_s8.bin,all_s64.bin,all_s2048.bin,all_s20000.bin,alpha172.txt}. One 6-thread job at a time (shared box).
# Single path: method 1 (25-probe syndrome join), A = B list = the 18,776 vocabulary, key on the plaintext index. Order = priority:
# 1 K4 L 1-3 on all_s64; 2 grid: K4 + 19 nulls L 1-3 on all_s2048; 3 audit: K4 L 1-3 main vs SAFE build on all_s20000 (9 rows);
# 4 K4 L 1-2 on all_s8; 5 K4 L 1 on the full set in 8 contiguous chunks (a chunk not ending in END is not counted).
W=${W:-/workspace/k4c185/w}; cd $W; mkdir -p run/out; K4=$(cat run/k4.txt)
job(){ f=run/out/$1.txt; shift; [ -s $f ] && tail -1 $f | grep -q '^END' && return; OMP_NUM_THREADS=6 "$@" > $f.tmp && mv $f.tmp $f; }
A=support/all.bin; S8=support/all_s8.bin; S64=support/all_s64.bin; S2k=support/all_s2048.bin; S20k=support/all_s20000.bin; V=support/alpha172.txt
date +%s > run/out/t_start.txt
job k4.s64L3   run/lrk185 $K4 $S64 $V $V k4 0 999999 1 1 3 q4r
job k4.s2k     run/lrk185 $K4 $S2k $V $V k4 0 999999 1 1 3 q4r
while read lab ct; do job $lab.s2k run/lrk185 $ct $S2k $V $V $lab 0 999999 1 1 3 q4r; done < run/nulls185.txt
job k4.s20k     run/lrk185     $K4 $S20k $V $V k4 0 999999 1 1 3 q4r
job k4.s20ksafe run/lrk185safe $K4 $S20k $V $V k4 0 999999 2 1 3 q4r
date +%s > run/out/t_mid.txt
job k4.s8L2    run/lrk185 $K4 $S8 $V $V k4 0 999999 1 1 2 q4r
for c in 0 1 2 3 4 5 6 7; do lo=$((c*20723)); hi=$(( c==7 ? 165782 : (c+1)*20723 )); job k4.fullL1.c$c run/lrk185 $K4 $A $V $V k4 $lo $hi 1 1 1 q4r; done
date +%s > run/out/t_end.txt; date > run/out/done.txt
