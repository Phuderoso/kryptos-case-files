#!/bin/bash
# Cycle 224 heavy runs (PREREG224). Run from WORKDIR containing kb224, kb224.bin, geo224.txt, bank.bin, all.bin, k4.txt, nulls224.tsv
export OMP_NUM_THREADS=8; mkdir -p R; K4=$(cat k4.txt); s=$(date +%s)
./kb224 $K4 x kb224.bin geo224.txt 1 0 GVQ 300000 24 > R/k4_direct.txt
./kb224 $K4 bank.bin kb224.bin geo224.txt 1 0 GVQ 300000 24 > R/k4_bank.txt; echo "k4 bank $(( $(date +%s)-s ))s" >> R/time.txt
./kb224 $K4 all.bin kb224.bin geo224.txt 1 0 GVQ 300000 24 > R/k4_all.txt; echo "k4 all $(( $(date +%s)-s ))s" >> R/time.txt
while read sd ct; do
  ./kb224 $ct x kb224.bin geo224.txt 1 0 GVQ 0 24 > R/null${sd}_direct.txt
  ./kb224 $ct bank.bin kb224.bin geo224.txt 1 0 G 0 24 > R/null${sd}_bankG.txt
  ./kb224 $ct all.bin kb224.bin geo224.txt 1 0 G 0 24 > R/null${sd}_allG.txt
done < nulls224.tsv; echo "nulls G/direct $(( $(date +%s)-s ))s" >> R/time.txt
head -3 nulls224.tsv | while read sd ct; do
  ./kb224 $ct bank.bin kb224.bin geo224.txt 10 0 VQ 0 24 > R/null${sd}_bankVQ_r10.txt
  ./kb224 $ct all.bin kb224.bin geo224.txt 10 0 VQ 0 24 > R/null${sd}_allVQ_r10.txt
done; echo "nulls VQ r10 $(( $(date +%s)-s ))s" >> R/time.txt
