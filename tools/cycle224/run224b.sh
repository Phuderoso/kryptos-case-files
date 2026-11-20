#!/bin/bash
# Cycle 224 follow-on runs (as executed 07:51-08:00 PT), from WORKDIR with kb224 built from kb224.c (scoring enabled by the qg.bin arg).
export OMP_NUM_THREADS=8; K4=$(cat k4.txt); mkdir -p RS RV
# scored K4 runs (decrypt + quadgram of every V / Q hit) and one scored null on every 10th row
./kb224 $K4 x kb224.bin geo224.txt 1 0 GVQ 0 24 qg.bin > RS/k4_direct.txt
./kb224 $K4 bank.bin kb224.bin geo224.txt 1 0 GVQ 0 24 qg.bin > RS/k4_bank.txt
./kb224 $K4 all.bin kb224.bin geo224.txt 1 0 GVQ 0 24 qg.bin > RS/k4_all.txt
NL=$(head -1 nulls224.tsv | cut -f2)
./kb224 $NL bank.bin kb224.bin geo224.txt 10 0 VQ 0 24 qg.bin > RS/null209417_bankVQ_r10.txt
./kb224 $NL all.bin kb224.bin geo224.txt 10 0 VQ 0 24 qg.bin > RS/null209417_allVQ_r10.txt
# two full-scale nulls for V / Q behind both families (nulls 209418, 209419)
sed -n 2,3p nulls224.tsv | while read sd ct; do
  ./kb224 $ct bank.bin kb224.bin geo224.txt 1 0 VQ 0 24 > R/null${sd}_bankVQ_full.txt
  ./kb224 $ct all.bin kb224.bin geo224.txt 1 0 VQ 0 24 > R/null${sd}_allVQ_full.txt; done
# post hoc (not pre-registered): 100 shuffles (seeds 209437-209536, nullsV224.tsv) for V on all.bin
while read sd ct; do ./kb224 $ct all.bin kb224.bin geo224.txt 1 0 V 0 24 > RV/null${sd}_allV.txt; done < nullsV224.tsv
