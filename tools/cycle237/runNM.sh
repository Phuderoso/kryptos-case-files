#!/bin/bash
# PREREG237 I-376: near-miss profile on the CASE 222 window list (keys236.bin, 8,792 windows), tool gn237nm (gn217 + agreement histogram).
# K4 and 20 fresh nulls (nulls237nm.tsv, seeds 209686-209705): direct (full) and all.bin at row stride 20 offset 0 (rows / 20). Output NM/*.txt ('M maxagree= hist=' line).
export OMP_NUM_THREADS=8; mkdir -p NM; K4=$(cat k4.txt); s=$(date +%s); : > NM/time.txt
./gn237nm $K4 x alpha.bin alpha.bin keys236.bin 1 0 0 > NM/k4_direct.txt
./gn237nm $K4 all.bin themed144.bin themed144.bin keys236.bin 20 0 0 > NM/k4_all_r20.txt
echo "k4 $(( $(date +%s)-s ))s" >> NM/time.txt
while IFS=$'\t' read -r seed t sha; do
  ./gn237nm $t x alpha.bin alpha.bin keys236.bin 1 0 0 > NM/null${seed}_direct.txt
  ./gn237nm $t all.bin themed144.bin themed144.bin keys236.bin 20 0 0 > NM/null${seed}_all_r20.txt
  echo "null $seed $(( $(date +%s)-s ))s" >> NM/time.txt
done < nulls237nm.tsv
