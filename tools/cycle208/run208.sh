#!/bin/bash
# Cycle 208 registered run (PREREG208). Usage: run208.sh BIN ALLBIN OUTDIR K4FILE
BIN=$1; BANK=$2; OUT=$3; K4=$(cat "$4"); export OMP_NUM_THREADS=6
echo "start $(date)"
$BIN $K4 x 1 26 0 > $OUT/k4_direct_G0.txt
$BIN $K4 $BANK 1 22 5000 > $OUT/k4_fam_L1-22.txt
$BIN $K4 $BANK 23 26 0 > $OUT/k4_fam_L23-26.txt
echo "k4 done $(date)"
python3 - > $OUT/nulls_ct.txt <<PY
import random
k="$K4"; r=random.Random(208208)
for i in range(20):
    l=list(k); r.shuffle(l); print("".join(l))
PY
i=0; while read SH; do i=$((i+1)); $BIN $SH $BANK 1 22 0 > $OUT/null_$i.txt; echo "null $i $(date +%T)"; done < $OUT/nulls_ct.txt
echo "end $(date)"
