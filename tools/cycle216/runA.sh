#!/bin/bash
# Cycle 216 Part A runner (PREREG216). Own process group via setsid + timeout by the caller.
cd /workspace/k4c216/w; mkdir -p A AP; export OMP_NUM_THREADS=8; K4=$(cat k4.txt)
echo "start $(date +%T)"
# 1. plants first (gate P)
python3 plant216.py
while IFS=$'\t' read pid scope q d X Y form model L ix j dig p C; do
  if [ $scope = direct ]; then ./gron216 $C x alpha.bin 1 0 1000 $((X%1000)) 100000 > AP/p$pid.txt
  else ./gron216 $C $scope.bin themed144.bin 2000 $((q%2000)) 1 0 100000 > AP/p$pid.txt; fi
  # stage 2 on the planted cell's line only (deviation 1 in case 202: structured plant texts print thousands of neighbour lines;
  # the pass rule only reads the planted cell, so this cannot change a pass/fail)
  if [ $scope = direct ]; then grep "^S perm=-1 dir=0 X=$X Y=$Y form=$form " AP/p$pid.txt > AP/p$pid.cell.txt; python3 check216.py $C x alpha.bin AP/p$pid.cell.txt > AP/p$pid.json
  else grep "^S perm=$q dir=$d X=$X Y=$Y form=$form " AP/p$pid.txt > AP/p$pid.cell.txt; python3 check216.py $C $scope.bin themed144.bin AP/p$pid.cell.txt > AP/p$pid.json; fi
done < plants216.tsv
echo "plants done $(date +%T)"
# 2. K4, three scopes, full
./gron216 $K4 x alpha.bin 1 0 1 0 100000 > A/k4_direct.txt; echo "k4 direct $(date +%T) $(grep ^T A/k4_direct.txt)"
./gron216 $K4 bank.bin themed144.bin 1 0 1 0 100000 > A/k4_bank.txt; echo "k4 bank $(date +%T) $(grep ^T A/k4_bank.txt)"
./gron216 $K4 all.bin themed144.bin 1 0 1 0 100000 > A/k4_all.txt; echo "k4 all $(date +%T) $(grep ^T A/k4_all.txt)"
# 3. shuffled-K4 nulls (seeds 209227 direct, 209228 families), case 200 design: 20 direct nulls on X-twentieths, 10+10 family nulls on row-tenths
python3 -c "
import random
k=open('k4.txt').read().strip()
for seed,n,fn in ((209227,20,'A/nulls_direct_ct.txt'),(209228,10,'A/nulls_fam_ct.txt')):
    r=random.Random(seed); o=open(fn,'w')
    for i in range(n):
        l=list(k); r.shuffle(l); o.write(''.join(l)+'\n')"
i=0; while read SH; do ./gron216 $SH x alpha.bin 1 0 20 $i 100000 > A/null_direct_$i.txt; echo "null direct $i $(grep ^T A/null_direct_$i.txt)"; i=$((i+1)); done < A/nulls_direct_ct.txt
for F in bank all; do i=0; while read SH; do ./gron216 $SH $F.bin themed144.bin 10 $i 1 0 100000 > A/null_${F}_$i.txt; echo "null $F $i $(grep ^T A/null_${F}_$i.txt)"; i=$((i+1)); done < A/nulls_fam_ct.txt; done
echo "scan end $(date +%T)"
# 4. stage 2 (exact Gromark / periodic on the 23, decrypt + quadgram) on every K4 and null line
python3 check216.py $K4 x alpha.bin A/k4_direct.txt > A/k4_direct.json
python3 check216.py $K4 bank.bin themed144.bin A/k4_bank.txt > A/k4_bank.json
python3 check216.py $K4 all.bin themed144.bin A/k4_all.txt > A/k4_all.json
i=0; while read SH; do python3 check216.py $SH x alpha.bin A/null_direct_$i.txt > A/null_direct_$i.json; i=$((i+1)); done < A/nulls_direct_ct.txt
for F in bank all; do i=0; while read SH; do python3 check216.py $SH $F.bin themed144.bin A/null_${F}_$i.txt > A/null_${F}_$i.json; i=$((i+1)); done < A/nulls_fam_ct.txt; done
echo "end $(date +%T)"
