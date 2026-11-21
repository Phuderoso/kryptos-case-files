#!/bin/bash
# Cycle 227 heavy runs (PREREG227). Run from WORKDIR: setsid timeout 600 bash run227.sh
export OMP_NUM_THREADS=8; mkdir -p R; K4=$(cat k4.txt); s=$(date +%s); A="qg.bin oracle226.txt -6.0 200000"
t(){ echo "$1 $(( $(date +%s)-s ))s" >> R/time.txt; }
./kb227 $K4 x kb227.bin geo227a.txt 1 0 GVQ 0 24 $A > R/k4_direct_a.txt
./kb227 $K4 x kb227.bin geo227b.txt 1 0 GV 0 24 $A > R/k4_direct_b.txt
./kb227 $K4 bank.bin kb227.bin geo227a.txt 1 0 GVQ 0 24 $A > R/k4_bank_a.txt; t "k4 bank a"
./kb227 $K4 bank.bin kb227.bin geo227b.txt 1 0 GV 0 24 $A > R/k4_bank_b.txt; t "k4 bank b"
./kb227 $K4 all.bin kb227.bin geo227a.txt 1 0 GVQ 0 24 $A > R/k4_all_a.txt; t "k4 all a"
./kb227 $K4 all.bin kb227.bin geo227b.txt 1 0 GV 0 24 $A > R/k4_all_b.txt; t "k4 all b"
while read sd ct; do
  ./kb227 $ct x kb227.bin geo227a.txt 1 0 GVQ 0 24 $A > R/null${sd}_direct_a.txt
  ./kb227 $ct x kb227.bin geo227b.txt 1 0 GV 0 24 $A > R/null${sd}_direct_b.txt
  for g in a b; do for sc in bank all; do ./kb227 $ct $sc.bin kb227.bin geo227$g.txt 1 0 G 0 24 $A > R/null${sd}_${sc}_G_$g.txt; done; done
done < nulls224.tsv; t "nulls direct + G"
head -n 12 nulls224.tsv | while read sd ct; do
  for sc in bank all; do
    ./kb227 $ct $sc.bin kb227.bin geo227a.txt 10 0 VQ 0 24 $A > R/null${sd}_${sc}VQ_a_r10.txt
    ./kb227 $ct $sc.bin kb227.bin geo227b.txt 10 0 V 0 24 $A > R/null${sd}_${sc}V_b_r10.txt
  done; t "null $sd r10"
done
