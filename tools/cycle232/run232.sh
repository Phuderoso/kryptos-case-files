#!/bin/bash
# Cycle 232 heavy runs (PREREG232). From WORKDIR: setsid timeout 480 bash run232.sh   (resumable: finished files are skipped)
# Same commands as run229.sh (case 213 family, kb229 unchanged), fresh nulls only; K4 is NOT re-run (published data/cycle229/R used).
export OMP_NUM_THREADS=8; mkdir -p R; s=$(date +%s); A="qg.bin oracle226.txt -6.0 200000"; AP="qg.bin oracle226.txt -99 200000"
t(){ echo "$1 $(( $(date +%s)-s ))s $(date +%H:%M:%S)" >> R/time.txt; }
t start
[ -s plants232.tsv ] || python3 plant232.py . 209641 > plants232.tsv
[ -s nulls232.tsv ] || python3 plant232.py --nulls k4.txt 209609 32 > nulls232.tsv
tail -n +2 plants232.tsv | while IFS=$'\t' read pid sc row d p x y f bad tr kn nq ncp ct pt dec; do
  [ -s R/plant_$pid.txt ] || { ./kb229 $ct $sc.bin kb227.bin geo227a.txt 100000000 $row Q 100000 24 $AP > R/.tmp_p && mv R/.tmp_p R/plant_$pid.txt; }
done; t plants
one(){ [ -s R/$1.txt ] && return; shift_=$1; shift; "$@" > R/.tmp_$shift_ && mv R/.tmp_$shift_ R/$shift_.txt; }
run_text(){ # $1 label  $2 ciphertext
  one $1_direct_a ./kb229 $2 x kb227.bin geo227a.txt 1 0 GVQ 0 24 $A
  one $1_direct_b ./kb229 $2 x kb227.bin geo227b.txt 1 0 GV 0 24 $A
  for sc in bank all; do
    one $1_${sc}_Q_r10 ./kb229 $2 $sc.bin kb227.bin geo227a.txt 10 0 Q 0 24 $A
    one $1_${sc}_V_a ./kb229 $2 $sc.bin kb227.bin geo227a.txt 1 0 V 0 24 $A
    one $1_${sc}_V_b ./kb229 $2 $sc.bin kb227.bin geo227b.txt 1 0 V 0 24 $A
  done; t "$1"; }
tail -n +2 nulls232.tsv | while read sd ct; do run_text null$sd $ct; done
t end
