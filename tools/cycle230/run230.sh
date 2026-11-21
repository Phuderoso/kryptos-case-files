#!/bin/bash
# Cycle 230 heavy runs (PREREG230). From /workspace/k4c230/w: setsid timeout 900 bash ../src/run230.sh
export OMP_NUM_THREADS=8; mkdir -p R P; K4=$(cat k4.txt); s=$(date +%s)
t(){ echo "$1 $(( $(date +%s)-s ))s $(date +%H:%M:%S)" >> R/time.txt; }
t start
while IFS=$'\t' read id fam q d xi yi form typ size ct pt; do
  if [ $fam = direct ]; then ./bsk230 $ct x alpha.bin 1 0 86731 $xi 100000 10 6 > P/$id.txt
  else nr=$([ $fam = bank ] && echo 165065 || echo 165782); a=$(( q>50 ? q-50 : 0 )); b=$(( q+51<nr ? q+51 : nr ))
    dd if=$fam.bin of=P/$id.bin bs=194 skip=$a count=$((b-a)) status=none; echo $a > P/$id.off
    ./bsk230 $ct P/$id.bin themed144.bin 1 0 1 0 100000 10 6 > P/$id.txt; fi
done < plants230.tsv; t plants
python3 - <<'PY'
import random
k=open('k4.txt').read().strip()
with open('nulls230.txt','w') as o:
    for i in range(10):
        r=random.Random(209577+i); l=list(k); r.shuffle(l); o.write(''.join(l)+'\n')
PY
i=0; while read SH; do
  ./bsk230 $SH x alpha.bin 1 0 20 $i 100000 10 6 > R/null${i}_direct.txt
  ./bsk230 $SH bank.bin themed144.bin 20 $((2*i)) 1 0 100000 10 6 > R/null${i}_bank.txt
  ./bsk230 $SH all.bin themed144.bin 20 $((2*i)) 1 0 100000 10 6 > R/null${i}_all.txt
  t null$i; i=$((i+1)); done < nulls230.txt
./bsk230 $K4 bank.bin themed144.bin 1 0 1 0 100000 10 6 > R/k4_bank.txt; t k4bank
./bsk230 $K4 all.bin themed144.bin 1 0 1 0 100000 10 6 > R/k4_all.txt; t k4all
./bsk230 $K4 x alpha.bin 1 0 1 0 100000 10 6 > R/k4_direct.txt; t k4direct
t end
