#!/bin/bash
# PREREG239 Part A: K4 full scale in direct / bank / all.bin; 6 fresh nulls (209711-209716): direct full, bank / all.bin at row stride 10 (declared in advance, as cases 220 / 222 / 223).
export OMP_NUM_THREADS=8; mkdir -p A; K4=$(cat k4.txt); s=$(date +%s); : > A/time.txt
./gn217 $K4 x alpha.bin alpha.bin keys239.bin 1 0 100000 > A/k4_direct.txt; echo "direct $(( $(date +%s)-s ))s" >> A/time.txt
./gn217 $K4 bank.bin themed144.bin themed144.bin keys239.bin 1 0 100000 > A/k4_bank.txt; echo "bank $(( $(date +%s)-s ))s" >> A/time.txt
./gn217 $K4 all.bin themed144.bin themed144.bin keys239.bin 1 0 100000 > A/k4_all.txt; echo "all $(( $(date +%s)-s ))s" >> A/time.txt
while IFS=$'\t' read -r seed t sha; do
  ./gn217 $t x alpha.bin alpha.bin keys239.bin 1 0 100000 > A/null${seed}_direct.txt
  ./gn217 $t bank.bin themed144.bin themed144.bin keys239.bin 10 0 100000 > A/null${seed}_bank_r10.txt
  ./gn217 $t all.bin themed144.bin themed144.bin keys239.bin 10 0 100000 > A/null${seed}_all_r10.txt
  echo "null $seed $(( $(date +%s)-s ))s" >> A/time.txt
done < nulls239.tsv
