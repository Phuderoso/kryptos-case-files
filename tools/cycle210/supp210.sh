#!/bin/bash
# Cycle 210 descriptive supplement (NOT registered; decided after the registered run): 40 more shuffled-K4 tenth-nulls at L 15-17,
# random.Random(209215); null j on rows q % 10 == j % 10 of bank (j < 20) or all.bin (j >= 20) -> 2 more full-family null-equivalents each.
set -u; OUT=$1; export OMP_NUM_THREADS=8
python3 -c "
import random
k=open('k4.txt').read().strip(); r=random.Random(209215)
for i in range(40):
    l=list(k); r.shuffle(l); print(''.join(l))" > $OUT/supp_ct.txt
j=0; while read SH; do if [ $j -lt 20 ]; then F=bank.bin; else F=all.bin; fi
  ./wrq $SH $F 15 17 alph8.txt p62.txt 10 $((j % 10)) 50 > $OUT/supp_$j.txt; j=$((j+1)); done < $OUT/supp_ct.txt
echo done
