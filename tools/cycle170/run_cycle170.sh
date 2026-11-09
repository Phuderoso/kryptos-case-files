#!/bin/bash
# Cycle 170: Porta (V1/V2, two half-splits, 173,431 orderings) behind 165,782 K3-law decimations + spiral/diagonal routes.
set -e
W=${W:-/workspace/k4c170/run}; T=$(cd "$(dirname "$0")" && pwd); B=${B:-/home/box/kryptos_support_backup}; mkdir -p $W; cd $W
ln -sf /workspace/k4c168/run/all.bin all.bin; cp /workspace/k4c168/run/texts.txt .; ln -sf $B/alpha.bin alpha.bin
gcc -O3 -march=native -fopenmp -o porta170 $T/porta170.c
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
$T/run_chunks.sh k4 $K4                                              # K4, full family, 16 checkpointed chunks, with running keys
python3 $T/ctl170.py all.bin alpha.bin texts.txt 12 17001            # 12 planted controls (independent encryptor)
for i in $(seq 0 11); do OMP_NUM_THREADS=2 ./porta170 $(cat ctl/ctl$i.txt) ctl/ctl${i}_slice.bin alpha.bin texts.txt > ctl/ctl$i.out; done
python3 $T/verify170.py ctl ctl/plants.txt > ctl_verify170.txt
python3 -c "
import random
K4='$K4'
for s in range(40):
  l=list(K4); random.Random(170000+s).shuffle(l); print(''.join(l))" > nulls170.txt
mkdir -p nulls; i=0; while read n; do NORK=1 ./porta170 $n all.bin alpha.bin texts.txt > nulls/null$i.out; i=$((i+1)); done < nulls170.txt
for i in 0 1 2 3 4 5 6 7; do ./porta170 $(sed -n "$((i+1))p" nulls170.txt) all.bin alpha.bin texts.txt 16 0 > nulls/rk_null$i.out; done
python3 $T/summarize170.py . > summary170.txt
python3 $T/bound170.py all.bin out/k4.c* > bound170.txt
python3 $T/verify170.py decode $K4 all.bin out/k4.c* > k4_decodes.txt
python3 $T/english170.py $B/quadgrams.json k4_decodes.txt > english170.txt
python3 $T/recount170.py $K4 all.bin alpha.bin 100 0 > recount100.txt      # compare with: NORK=1 ./porta170 $K4 ... 100 0
