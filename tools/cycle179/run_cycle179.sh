#!/bin/bash
# Cycle 179 main run (resumable: outputs ending in END are skipped). W = scratch with run/{lr179,k4.txt,nulls179.txt}
# and support/{all.bin,all_s8.bin}. Each job: OMP 6 threads, one at a time (the box is shared).
W=${W:-/workspace/k4c179/w}; cd $W; mkdir -p run/out; K4=$(cat run/k4.txt)
job(){ f=run/out/$1.txt; shift; [ -s $f ] && tail -1 $f | grep -q '^END' && return; OMP_NUM_THREADS=6 "$@" > $f.tmp && mv $f.tmp $f; }
A=support/all.bin; S8=support/all_s8.bin
one(){ lab=$1 ct=$2
  job $lab.m0   run/lr179 $ct $A  $lab 0 165782 0 1 8
  job $lab.m1   run/lr179 $ct $A  $lab 0 165782 1 1 4
  job $lab.m1s8 run/lr179 $ct $S8 $lab 0 999999 1 5 5; }
one k4 $K4
job k4.m1L5 run/lr179 $K4 $A k4 0 165782 1 5 5
while read lab ct; do one $lab $ct; done < run/nulls179.txt
date > run/out/done.txt
