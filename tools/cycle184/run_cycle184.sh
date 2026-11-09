#!/bin/bash
# Cycle 184 main run (resumable: outputs ending in END are skipped). W = scratch with run/{lrk184,lrk184safe,k4.txt,nulls184.txt} and
# support/{all.bin,all_s64.bin,all_s512.bin,all_s2048.bin,alpha172.txt}. One 6-thread job at a time (shared box).
# vv = A vocabulary (plaintext side) x B vocabulary (ciphertext side), 352,538,176 ordered pairs, Vig/Beau, M0 L 1-4.
W=${W:-/workspace/k4c184/w}; cd $W; mkdir -p run/out; K4=$(cat run/k4.txt)
job(){ f=run/out/$1.txt; shift; [ -s $f ] && tail -1 $f | grep -q '^END' && return; s=$(date +%s); OMP_NUM_THREADS=6 "$@" > $f.tmp && mv $f.tmp $f; echo "$(basename $f .txt) $(( $(date +%s)-s )) s" >> run/out/timing.txt; }
A=support/all.bin; S64=support/all_s64.bin; S512=support/all_s512.bin; S2K=support/all_s2048.bin; V=support/alpha172.txt
date +%s > run/out/t_start.txt
job k4.full     run/lrk184     $K4 $A    $V $V k4 0 999999 1 1 4 q4vv
job k4.s64m1    run/lrk184     $K4 $S64  $V $V k4 0 999999 1 1 4 q4vv
job k4.s64m0    run/lrk184     $K4 $S64  $V $V k4 0 999999 0 1 4 q4vv
job k4.s2km1    run/lrk184     $K4 $S2K  $V $V k4 0 999999 1 1 4 q4vv
job k4.s2ksafe  run/lrk184safe $K4 $S2K  $V $V k4 0 999999 2 1 4 q4vv
job k4.s512     run/lrk184     $K4 $S512 $V $V k4 0 999999 1 1 4 q4vv
while read lab ct; do job $lab.s512 run/lrk184 $ct $S512 $V $V $lab 0 999999 1 1 4 q4vv; done < run/nulls184.txt
date +%s > run/out/t_end.txt; date > run/out/done.txt
