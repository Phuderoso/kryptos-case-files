#!/bin/bash
# Cycle 181 main run (resumable: outputs ending in END are skipped). W = scratch with run/{lrk181,k4.txt,nulls181.txt} and
# support/{all.bin,all_s8.bin,all_s64.bin,alpha172.txt}. One 6-thread job at a time (shared box).
W=${W:-/workspace/k4c181/w}; cd $W; mkdir -p run/out; K4=$(cat run/k4.txt)
job(){ f=run/out/$1.txt; shift; [ -s $f ] && tail -1 $f | grep -q '^END' && return; OMP_NUM_THREADS=6 "$@" > $f.tmp && mv $f.tmp $f; }
A=support/all.bin; S8=support/all_s8.bin; S64=support/all_s64.bin; V=support/alpha172.txt
date +%s > run/out/t_start.txt
job k4.m0     run/lrk181 $K4 $A   $V k4 0 999999 0 1 6
job k4.m1     run/lrk181 $K4 $A   $V k4 0 999999 1 1 2
job k4.m1L3s8 run/lrk181 $K4 $S8  $V k4 0 999999 1 3 3
job k4.m0s64  run/lrk181 $K4 $S64 $V k4 0 999999 0 1 6
job k4.m1s64  run/lrk181 $K4 $S64 $V k4 0 999999 1 1 3
while read lab ct; do
  job $lab.m0s64 run/lrk181 $ct $S64 $V $lab 0 999999 0 1 6
  job $lab.m1s64 run/lrk181 $ct $S64 $V $lab 0 999999 1 1 3
done < run/nulls181.txt
date +%s > run/out/t_end.txt; date > run/out/done.txt
