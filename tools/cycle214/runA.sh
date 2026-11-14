#!/bin/bash
cd /workspace/k4c214/w; mkdir -p A; export OMP_NUM_THREADS=8; K4=$(cat k4.txt)
echo "start $(date +%T)"
./gron214 $K4 x alpha.bin 1 0 1 0 100000 > A/k4_direct.txt; echo "k4 direct $(date +%T) $(grep ^T A/k4_direct.txt)"
./gron214 $K4 bank.bin themed144.bin 1 0 1 0 100000 > A/k4_bank.txt; echo "k4 bank $(date +%T) $(grep ^T A/k4_bank.txt)"
./gron214 $K4 all.bin themed144.bin 1 0 1 0 100000 > A/k4_all.txt; echo "k4 all $(date +%T) $(grep ^T A/k4_all.txt)"
python3 -c "
import random
k=open('k4.txt').read().strip()
for seed,n,fn in ((209223,20,'A/nulls_direct_ct.txt'),(209224,10,'A/nulls_fam_ct.txt')):
    r=random.Random(seed); o=open(fn,'w')
    for i in range(n):
        l=list(k); r.shuffle(l); o.write(''.join(l)+'\n')"
i=0; while read SH; do ./gron214 $SH x alpha.bin 1 0 20 $i 100000 > A/null_direct_$i.txt; echo "null direct $i $(grep ^T A/null_direct_$i.txt)"; i=$((i+1)); done < A/nulls_direct_ct.txt
for F in bank all; do i=0; while read SH; do ./gron214 $SH $F.bin themed144.bin 10 $i 1 0 100000 > A/null_${F}_$i.txt; echo "null $F $i $(grep ^T A/null_${F}_$i.txt)"; i=$((i+1)); done < A/nulls_fam_ct.txt; done
echo "end $(date +%T)"
