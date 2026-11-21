#!/bin/bash
# Cycle 227: K4 on the r10 rows (same rows as the null r10 runs), for the same-scale comparison pre-registered in PREREG227.
export OMP_NUM_THREADS=8; K4=$(cat k4.txt); A="qg.bin oracle226.txt -6.0 200000"
for sc in bank all; do
  ./kb227 $K4 $sc.bin kb227.bin geo227a.txt 10 0 VQ 0 24 $A > R/k4_${sc}VQ_a_r10.txt
  ./kb227 $K4 $sc.bin kb227.bin geo227b.txt 10 0 V 0 24 $A > R/k4_${sc}V_b_r10.txt
done
