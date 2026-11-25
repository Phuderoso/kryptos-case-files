#!/bin/bash
# PREREG238 Part B: two fresh nulls at FULL scale (row stride 1) on keys237.bin, all three scopes; closes the case 223 stride-10 deviation.
export OMP_NUM_THREADS=8; mkdir -p B; s=$(date +%s)
while IFS=$'\t' read -r seed t sha; do
  ./gn217 $t x alpha.bin alpha.bin keys237.bin 1 0 100000 > B/null${seed}_direct.txt
  ./gn217 $t bank.bin themed144.bin themed144.bin keys237.bin 1 0 100000 > B/null${seed}_bank.txt
  ./gn217 $t all.bin themed144.bin themed144.bin keys237.bin 1 0 100000 > B/null${seed}_all.txt
  echo "null $seed $(( $(date +%s)-s ))s" >> B/time.txt
done < nulls238.tsv
