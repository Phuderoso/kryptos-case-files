#!/bin/bash
# Cycle 226 heavy runs (PREREG226). Run from WORKDIR with kb226 (gcc -O2 -fopenmp kb226.c), kb224.bin, geo224.txt, bank.bin, all.bin,
# k4.txt, nulls224.tsv, qg.bin, oracle226.txt. Wrapped by: setsid timeout 600 bash run226.sh
export OMP_NUM_THREADS=8; mkdir -p R; K4=$(cat k4.txt); s=$(date +%s); A="qg.bin oracle226.txt -6.0 200000"
./kb226 $K4 x kb224.bin geo224.txt 1 0 GVQ 0 24 $A > R/k4_direct.txt
./kb226 $K4 bank.bin kb224.bin geo224.txt 1 0 GVQ 0 24 $A > R/k4_bank.txt; echo "k4 bank $(( $(date +%s)-s ))s" >> R/time.txt
./kb226 $K4 all.bin kb224.bin geo224.txt 1 0 GVQ 0 24 $A > R/k4_all.txt; echo "k4 all $(( $(date +%s)-s ))s" >> R/time.txt
while read sd ct; do
  ./kb226 $ct bank.bin kb224.bin geo224.txt 10 0 VQ 0 24 $A > R/null${sd}_bankVQ_r10.txt
  ./kb226 $ct all.bin kb224.bin geo224.txt 10 0 VQ 0 24 $A > R/null${sd}_allVQ_r10.txt
  echo "null $sd $(( $(date +%s)-s ))s" >> R/time.txt
done < nulls224.tsv
