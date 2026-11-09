#!/bin/bash
# Cycle 183 main run (resumable: outputs ending in END are skipped). W = scratch with run/{lrk183,lrk183safe,k4.txt,nulls183.txt,all_s2048.bin}
# and support/{all.bin,all_s64.bin,alpha172.txt,alpha_themed180.txt}. One 6-thread job at a time (shared box).
# f = A themed (plaintext side) x B vocabulary (ciphertext side), method 0;  r = A vocabulary x B themed, method 1.  Key on the plaintext index.
# K4: L 1-4 on the full set; L 1-5 on all_s64 (L 5 = 1/64 of the routes); audit build (method 2) L 1-5 on all_s2048.  Nulls: L 1-4 on all_s64.
W=${W:-/workspace/k4c183/w}; cd $W; mkdir -p run/out; K4=$(cat run/k4.txt)
job(){ f=run/out/$1.txt; shift; [ -s $f ] && tail -1 $f | grep -q '^END' && return; OMP_NUM_THREADS=6 "$@" > $f.tmp && mv $f.tmp $f; }
A=support/all.bin; S64=support/all_s64.bin; S2k=run/all_s2048.bin; V=support/alpha172.txt; TH=support/alpha_themed180.txt
date +%s > run/out/t_start.txt
job k4.f      run/lrk183 $K4 $A   $TH $V k4 0 999999 0 1 4 q4f
job k4.r      run/lrk183 $K4 $A   $V $TH k4 0 999999 1 1 4 q4r
job k4.fs64L5 run/lrk183 $K4 $S64 $TH $V k4 0 999999 0 1 5 q4f
job k4.rs64L5 run/lrk183 $K4 $S64 $V $TH k4 0 999999 1 1 5 q4r
job k4.fs2k   run/lrk183 $K4 $S2k $TH $V k4 0 999999 0 1 5 q4f
job k4.rs2k   run/lrk183 $K4 $S2k $V $TH k4 0 999999 1 1 5 q4r
job k4.fs2ksafe run/lrk183safe $K4 $S2k $TH $V k4 0 999999 2 1 5 q4f
job k4.rs2ksafe run/lrk183safe $K4 $S2k $V $TH k4 0 999999 2 1 5 q4r
job k4.fs64   run/lrk183 $K4 $S64 $TH $V k4 0 999999 0 1 4 q4f
job k4.rs64   run/lrk183 $K4 $S64 $V $TH k4 0 999999 1 1 4 q4r
while read lab ct; do
  job $lab.fs64 run/lrk183 $ct $S64 $TH $V $lab 0 999999 0 1 4 q4f
  job $lab.rs64 run/lrk183 $ct $S64 $V $TH $lab 0 999999 1 1 4 q4r
done < run/nulls183.txt
date +%s > run/out/t_end.txt; date > run/out/done.txt
