#!/bin/bash
cd /workspace/k4c214/w; mkdir -p AP; export OMP_NUM_THREADS=8
while IFS=$'\t' read id fam q d xi yi form L ix ct pt; do
  if [ $fam = direct ]; then ./gron214 $ct x alpha.bin 1 0 86731 $xi 100000 > AP/$id.txt
  else nr=$([ $fam = bank ] && echo 165065 || echo 165782); a=$(( q>50 ? q-50 : 0 )); b=$(( q+51<nr ? q+51 : nr ))
    dd if=$fam.bin of=AP/$id.bin bs=194 skip=$a count=$((b-a)) status=none; echo $a > AP/$id.off
    ./gron214 $ct AP/$id.bin themed144.bin 1 0 1 0 100000 > AP/$id.txt; fi
  echo "$id $(grep '^T' AP/$id.txt)"
done < plants214.tsv
