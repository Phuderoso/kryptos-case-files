#!/bin/bash
# Cycle 180 main run (resumable: outputs ending in END are skipped). W = scratch with run/{lrk180,k4.txt,nulls180.txt} and
# support/{all.bin,all_s8.bin,alpha172.txt,alpha_themed180.txt}. One 6-thread job at a time (shared box).
W=${W:-/workspace/k4c180/w}; cd $W; mkdir -p run/out; K4=$(cat run/k4.txt)
job(){ f=run/out/$1.txt; shift; [ -s $f ] && tail -1 $f | grep -q '^END' && return; OMP_NUM_THREADS=6 "$@" > $f.tmp && mv $f.tmp $f; }
A=support/all.bin; S8=support/all_s8.bin; V=support/alpha172.txt; TH=support/alpha_themed180.txt
date +%s > run/out/t_start.txt
job k4.m0   run/lrk180 $K4 $A $V k4 0 999999 0 1 7
job k4.m1   run/lrk180 $K4 $A $V k4 0 999999 1 1 3
job k4.m1t  run/lrk180 $K4 $A $TH k4 0 999999 1 4 4
job k4.m0s8 run/lrk180 $K4 $S8 $V k4 0 999999 0 1 7
job k4.m1s8 run/lrk180 $K4 $S8 $V k4 0 999999 1 1 3
while read lab ct; do
  job $lab.m0s8 run/lrk180 $ct $S8 $V $lab 0 999999 0 1 7
  job $lab.m1s8 run/lrk180 $ct $S8 $V $lab 0 999999 1 1 3
  job $lab.m1t  run/lrk180 $ct $A $TH $lab 0 999999 1 4 4
done < run/nulls180.txt
date +%s > run/out/t_end.txt; date > run/out/done.txt
