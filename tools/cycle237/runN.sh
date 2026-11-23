#!/bin/bash
# PREREG237 Part A nulls, EXECUTED AT ROW STRIDE 10 (bank and all.bin; direct full) -- deviation from runA.sh (full scale) because full-scale nulls would take ~17 min (compute budget); disclosed in case 223.
export OMP_NUM_THREADS=8; mkdir -p A; s=$(date +%s)
while IFS=$'\t' read -r seed t sha; do
  ./gn217 $t x alpha.bin alpha.bin keys237.bin 1 0 100000 > A/null${seed}_direct.txt
  ./gn217 $t bank.bin themed144.bin themed144.bin keys237.bin 10 0 100000 > A/null${seed}_bank_r10.txt
  ./gn217 $t all.bin themed144.bin themed144.bin keys237.bin 10 0 100000 > A/null${seed}_all_r10.txt
  echo "null $seed $(( $(date +%s)-s ))s" >> A/time.txt
done < nulls237.tsv
