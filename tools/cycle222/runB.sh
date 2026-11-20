#!/bin/bash
export OMP_NUM_THREADS=8; mkdir -p B; K4=$(cat k4.txt); NL=$(cat null1.txt)
s=$(date +%s)
./gn217 $K4 x alpha.bin alpha.bin keys222b.bin 1 0 100000 > B/k4_direct.txt; echo "direct $(( $(date +%s)-s ))s" >> B/time.txt
./gn217 $K4 bank.bin themed144.bin themed144.bin keys222b.bin 1 0 100000 > B/k4_bank.txt; echo "bank $(( $(date +%s)-s ))s" >> B/time.txt
./gn217 $K4 all.bin themed144.bin themed144.bin keys222b.bin 1 0 100000 > B/k4_all.txt; echo "all $(( $(date +%s)-s ))s" >> B/time.txt
./gn217 $NL x alpha.bin alpha.bin keys222b.bin 1 0 100000 > B/null1_direct.txt
./gn217 $NL bank.bin themed144.bin themed144.bin keys222b.bin 10 0 100000 > B/null1_bank_r10.txt
./gn217 $NL all.bin themed144.bin themed144.bin keys222b.bin 10 0 100000 > B/null1_all_r10.txt; echo "nulls $(( $(date +%s)-s ))s" >> B/time.txt
