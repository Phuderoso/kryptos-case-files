#!/bin/bash
# Cycle 231 heavy runs (PREREG231). From /workspace/k4c231/w: setsid timeout 700 bash ../src/run231.sh
export OMP_NUM_THREADS=8; mkdir -p R P; s=$(date +%s)
t(){ echo "$1 $(( $(date +%s)-s ))s $(date +%H:%M:%S)" >> R/time.txt; }
t start
python3 ../src/plant230.py 209608 > plants231.tsv
while IFS=$'\t' read id fam q d xi yi form typ size ct pt; do
  if [ $fam = direct ]; then ./bsk230 $ct x alpha.bin 1 0 86731 $xi 100000 10 6 > P/$id.txt
  else nr=$([ $fam = bank ] && echo 165065 || echo 165782); a=$(( q>50 ? q-50 : 0 )); b=$(( q+51<nr ? q+51 : nr ))
    dd if=$fam.bin of=P/$id.bin bs=194 skip=$a count=$((b-a)) status=none; echo $a > P/$id.off
    ./bsk230 $ct P/$id.bin themed144.bin 1 0 1 0 100000 10 6 > P/$id.txt; fi
done < plants231.tsv; t plants
python3 - <<'PY'
import random
k=open('k4.txt').read().strip()
with open('nulls231.txt','w') as o:
    for i in range(20):
        r=random.Random(209588+i); l=list(k); r.shuffle(l); o.write(''.join(l)+'\n')
PY
i=0; while read SH; do
  # bank / all.bin: 1/20 scale, row stride 20, offset 2i mod 20 (all 20 offsets are used over 20 nulls: rowoff = i)
  ./bsk230 $SH bank.bin themed144.bin 20 $i 1 0 100000 10 6 > R/null${i}_bank.txt
  ./bsk230 $SH all.bin themed144.bin 20 $i 1 0 100000 10 6 > R/null${i}_all.txt
  t nullBA$i; i=$((i+1)); done < nulls231.txt
i=0; while read SH; do
  if [ $i -lt 8 ]; then ./bsk230 $SH x alpha.bin 1 0 5 $i 100000 10 6 > R/null${i}_direct.txt; t nullD$i; fi
  i=$((i+1)); done < nulls231.txt
t end
