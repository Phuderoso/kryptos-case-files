#!/bin/bash
# Cycle 182 add-on (I-160, PREREG182 section B): case 169's D2 (lrk181 mode 1, one-error mod-2 passes, L 1-3, all_s64, 18,776
# alphabets x q1/q2/q3) on 40 fresh plain shuffles (seeds 18241-18280) and 20 parity-matched shuffles (seeds 18281-18300: K4's letters
# permuted within the A-Z parity classes, so every position keeps its A-Z parity), plus K4 recomputed (expected 18,432).
W=${W:-/workspace/k4c182/w}; cd $W; mkdir -p run/i160
python3 -c "
import random
K=open('run/k4.txt').read().strip()
for s in range(18241,18281):
    l=list(K); random.Random(s).shuffle(l); print(f'f{s}', ''.join(l))
for s in range(18281,18301):
    R=random.Random(s); out=list(K)
    for par in (0,1):
        pos=[i for i,c in enumerate(K) if (ord(c)-65)%2==par]; let=[K[i] for i in pos]; R.shuffle(let)
        for i,c in zip(pos,let): out[i]=c
    print(f'm{s}', ''.join(out))
print('k4', K)" > run/i160/texts182.txt
while read lab ct; do f=run/i160/$lab.txt; [ -s $f ] && tail -1 $f | grep -q '^END' && continue
  OMP_NUM_THREADS=6 run/lrk181 $ct support/all_s64.bin support/alpha172.txt $lab 0 999999 1 1 3 > $f.tmp && mv $f.tmp $f; done < run/i160/texts182.txt
