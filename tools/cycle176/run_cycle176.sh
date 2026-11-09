#!/bin/bash
# Cycle 176 main run (resumable: outputs ending in END are skipped). W = scratch with run/{gm176,pg176,k4.txt,nulls176.txt,
# primers176.txt,cfg176.txt} and support/{all.bin,all_s8.bin}. Each job: OMP 6 threads, one at a time (the box is shared).
W=${W:-/workspace/k4c176}; cd $W; mkdir -p run/out; K4=$(cat run/k4.txt)
job(){ f=run/out/$1.txt; shift; [ -s $f ] && tail -1 $f | grep -q '^END' && return; OMP_NUM_THREADS=6 "$@" > $f.tmp && mv $f.tmp $f; }
# K4, full perm set
job k4.g0      run/gm176 $K4 support/all.bin k4 0 165782 0 2 8
job k4.g1      run/gm176 $K4 support/all.bin k4 0 165782 1 2 5
job k4.w0      run/gm176 $K4 support/all.bin k4 0 165782 0 0 0 run/primers176.txt
job k4.w1      run/gm176 $K4 support/all.bin k4 0 165782 1 0 0 run/primers176.txt
job k4.pg0     run/pg176 $K4 support/all.bin run/cfg176.txt k4 0
job k4.pg1     run/pg176 $K4 support/all.bin run/cfg176.txt k4 1
job k4s8.g1    run/gm176 $K4 support/all_s8.bin k4s8 0 999999 1 2 5
job k4s8.w1    run/gm176 $K4 support/all_s8.bin k4s8 0 999999 1 0 0 run/primers176.txt
# 19 nulls: ix 0 on the full perm set (cost is set by the primers), ix 1 on every 8th perm
i=0; while read lab ct; do i=$((i+1))
  job $lab.g0  run/gm176 $ct support/all.bin $lab 0 165782 0 2 7
  [ $i -le 9 ] && job $lab.g0L8 run/gm176 $ct support/all.bin $lab 0 165782 0 8 8
  job $lab.w0  run/gm176 $ct support/all.bin $lab 0 165782 0 0 0 run/primers176.txt
  job $lab.pg0 run/pg176 $ct support/all.bin run/cfg176.txt $lab 0
  job $lab.pg1 run/pg176 $ct support/all.bin run/cfg176.txt $lab 1
  job $lab.g1  run/gm176 $ct support/all_s8.bin $lab 0 999999 1 2 5
  job $lab.w1  run/gm176 $ct support/all_s8.bin $lab 0 999999 1 0 0 run/primers176.txt
done < run/nulls176.txt
date > run/out/done.txt
