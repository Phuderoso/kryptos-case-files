#!/bin/bash
# Cycle 177 main run (resumable: outputs ending in END are skipped). W = scratch with run/{gm177,pg177,k4.txt,nulls177.txt,
# primers176.txt,cfg176.txt} and support/{all.bin,all_s8.bin}. Each job: OMP 6 threads, one at a time (the box is shared).
W=${W:-/workspace/k4c177w}; cd $W; mkdir -p run/out; K4=$(cat run/k4.txt)
job(){ f=run/out/$1.txt; shift; [ -s $f ] && tail -1 $f | grep -q '^END' && return; OMP_NUM_THREADS=6 "$@" > $f.tmp && mv $f.tmp $f; }
jobb(){ f=run/out/$1.txt; shift; [ -s $f ] && tail -1 $f | grep -q '^ALLEND' && return; { for b in 5 6 7 8 9; do OMP_NUM_THREADS=6 "$@" $b 0; done; echo ALLEND; } > $f.tmp && mv $f.tmp $f; }
A=support/all.bin; S8=support/all_s8.bin
# K4
job  k4.g0e   run/gm177 $K4 $A k4 0 165782 0 2 6 10 1
job  k4.w0e   run/gm177 $K4 $A k4 0 165782 0 0 0 10 1 run/primers176.txt
job  k4.pg0e  run/pg177 $K4 $A run/cfg176.txt k4 0
job  k4.pg1e  run/pg177 $K4 $A run/cfg176.txt k4 1
jobb k4.b0    run/gm177 $K4 $A k4 0 165782 0 2 7
job  k4s8.g1e run/gm177 $K4 $S8 k4s8 0 999999 1 2 5 10 1
job  k4s8.w1e run/gm177 $K4 $S8 k4s8 0 999999 1 0 0 10 1 run/primers176.txt
jobb k4s8.b1  run/gm177 $K4 $S8 k4s8 0 999999 1 2 4
job  k4.g1e   run/gm177 $K4 $A k4 0 165782 1 2 5 10 1
job  k4.w1e   run/gm177 $K4 $A k4 0 165782 1 0 0 10 1 run/primers176.txt
jobb k4.b1    run/gm177 $K4 $A k4 0 165782 1 2 4
# 19 nulls (seeds 17711-17729): ix 0 and PG on the full set, ix 1 on every 8th perm
while read lab ct; do
  job  $lab.g0e  run/gm177 $ct $A $lab 0 165782 0 2 6 10 1
  job  $lab.w0e  run/gm177 $ct $A $lab 0 165782 0 0 0 10 1 run/primers176.txt
  job  $lab.pg0e run/pg177 $ct $A run/cfg176.txt $lab 0
  job  $lab.pg1e run/pg177 $ct $A run/cfg176.txt $lab 1
  jobb $lab.b0   run/gm177 $ct $A $lab 0 165782 0 2 7
  job  $lab.g1e  run/gm177 $ct $S8 $lab 0 999999 1 2 5 10 1
  job  $lab.w1e  run/gm177 $ct $S8 $lab 0 999999 1 0 0 10 1 run/primers176.txt
  jobb $lab.b1   run/gm177 $ct $S8 $lab 0 999999 1 2 4
done < run/nulls177.txt
date > run/out/done.txt
