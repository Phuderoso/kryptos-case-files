#!/bin/bash
# Cycle 178 main run (resumable: outputs ending in END are skipped). W = scratch with run/{lr178,k4.txt,nulls178.txt,seeds178.txt}
# and support/{all.bin,all_s8.bin}. Each job: OMP 6 threads, one at a time (the box is shared).
W=${W:-/workspace/k4c178w}; cd $W; mkdir -p run/out; K4=$(cat run/k4.txt)
job(){ f=run/out/$1.txt; shift; [ -s $f ] && tail -1 $f | grep -q '^END' && return; OMP_NUM_THREADS=6 "$@" > $f.tmp && mv $f.tmp $f; }
A=support/all.bin; S8=support/all_s8.bin; SD=run/seeds178.txt
one(){ lab=$1 ct=$2
  job $lab.m0   run/lr178 $ct $A  $lab 0 165782 0 1 8
  job $lab.m1   run/lr178 $ct $A  $lab 0 165782 1 1 5
  job $lab.w0   run/lr178 $ct $A  $lab 0 165782 2 6 10 0 $SD
  job $lab.w1   run/lr178 $ct $A  $lab 0 165782 2 6 10 1 $SD
  job $lab.m0s8 run/lr178 $ct $S8 $lab 0 999999 0 9 9; }
one k4 $K4
job k4.m0L9 run/lr178 $K4 $A k4 0 165782 0 9 9
while read lab ct; do one $lab $ct; done < run/nulls178.txt
date > run/out/done.txt
