#!/bin/bash
# Cycle 229 heavy runs (PREREG229). Run from WORKDIR: setsid timeout 420 bash run229.sh
export OMP_NUM_THREADS=8; mkdir -p R; K4=$(cat k4.txt); s=$(date +%s); A="qg.bin oracle226.txt -6.0 200000"
t(){ echo "$1 $(( $(date +%s)-s ))s $(date +%H:%M:%S)" >> R/time.txt; }
t start
python3 plant229.py . 209558 > plants229.tsv
python3 plant229.py --nulls k4.txt 209559 16 > nulls229.tsv
tail -n +2 plants229.tsv | while IFS=$'\t' read pid sc row d p x y f bad tr kn nq ncp ct pt dec; do
  ./kb229 $ct $sc.bin kb227.bin geo227a.txt 100000000 $row Q 100000 24 $A > R/plant_$pid.txt
done; t plants
run_text(){ # $1 label  $2 ciphertext
  ./kb229 $2 x kb227.bin geo227a.txt 1 0 GVQ 0 24 $A > R/$1_direct_a.txt
  ./kb229 $2 x kb227.bin geo227b.txt 1 0 GV 0 24 $A > R/$1_direct_b.txt
  for sc in bank all; do
    ./kb229 $2 $sc.bin kb227.bin geo227a.txt 10 0 Q 0 24 $A > R/$1_${sc}_Q_r10.txt
    ./kb229 $2 $sc.bin kb227.bin geo227a.txt 1 0 V 0 24 $A > R/$1_${sc}_V_a.txt
    ./kb229 $2 $sc.bin kb227.bin geo227b.txt 1 0 V 0 24 $A > R/$1_${sc}_V_b.txt
  done; t "$1"; }
run_text k4 $K4
tail -n +2 nulls229.tsv | while read sd ct; do run_text null$sd $ct; done
t end
