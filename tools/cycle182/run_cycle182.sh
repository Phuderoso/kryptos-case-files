#!/bin/bash
# Cycle 182 main run (resumable: outputs ending in END are skipped). W = scratch with run/{lrk182,lrk182safe,k4.txt,nulls182.txt} and
# support/{all.bin,all_s64.bin,alpha172.txt,alpha_themed180.txt}. One 6-thread job at a time (shared box).
# f = A themed (plaintext side) x B vocabulary (ciphertext side), method 0;  r = A vocabulary x B themed, method 1.  M0 L 1-6.
W=${W:-/workspace/k4c182/w}; cd $W; mkdir -p run/out; K4=$(cat run/k4.txt)
job(){ f=run/out/$1.txt; shift; [ -s $f ] && tail -1 $f | grep -q '^END' && return; OMP_NUM_THREADS=6 "$@" > $f.tmp && mv $f.tmp $f; }
A=support/all.bin; S64=support/all_s64.bin; V=support/alpha172.txt; TH=support/alpha_themed180.txt
date +%s > run/out/t_start.txt
job k4.f      run/lrk182 $K4 $A   $TH $V k4 0 999999 0 1 6 q4f
job k4.r      run/lrk182 $K4 $A   $V $TH k4 0 999999 1 1 6 q4r
job k4.fs64   run/lrk182 $K4 $S64 $TH $V k4 0 999999 0 1 6 q4f
job k4.rs64   run/lrk182 $K4 $S64 $V $TH k4 0 999999 1 1 6 q4r
job k4.fs64safe run/lrk182safe $K4 $S64 $TH $V k4 0 999999 2 1 6 q4f
job k4.rs64safe run/lrk182safe $K4 $S64 $V $TH k4 0 999999 2 1 6 q4r
while read lab ct; do
  job $lab.fs64 run/lrk182 $ct $S64 $TH $V $lab 0 999999 0 1 6 q4f
  job $lab.rs64 run/lrk182 $ct $S64 $V $TH $lab 0 999999 1 1 6 q4r
done < run/nulls182.txt
date +%s > run/out/t_end.txt; date > run/out/done.txt
