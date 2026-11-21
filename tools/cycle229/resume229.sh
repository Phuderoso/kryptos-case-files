#!/bin/bash
# Cycle 229 resume: the run229.sh process group ended at 03:54:51 PT mid null 209565 (no error output); same commands for 209565-209574.
export OMP_NUM_THREADS=8; s=$(date +%s); A="qg.bin oracle226.txt -6.0 200000"
t(){ echo "$1 $(( $(date +%s)-s ))s $(date +%H:%M:%S) (resume)" >> R/time.txt; }
run_text(){
  ./kb229 $2 x kb227.bin geo227a.txt 1 0 GVQ 0 24 $A > R/$1_direct_a.txt
  ./kb229 $2 x kb227.bin geo227b.txt 1 0 GV 0 24 $A > R/$1_direct_b.txt
  for sc in bank all; do
    ./kb229 $2 $sc.bin kb227.bin geo227a.txt 10 0 Q 0 24 $A > R/$1_${sc}_Q_r10.txt
    ./kb229 $2 $sc.bin kb227.bin geo227a.txt 1 0 V 0 24 $A > R/$1_${sc}_V_a.txt
    ./kb229 $2 $sc.bin kb227.bin geo227b.txt 1 0 V 0 24 $A > R/$1_${sc}_V_b.txt
  done; t "$1"; }
t start
tail -n +2 nulls229.tsv | awk '$1>=209565' | while read sd ct; do run_text null$sd $ct; done
t end
