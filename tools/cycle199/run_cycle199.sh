#!/bin/bash
# Cycle 199 registered run (PREREG199, I-220 chunk 1). Solver B (cmp197, case 184 build, compiled with -fopenmp, 7 threads) behind
# NON-M = N perms: dec98 q 4116-28115 (del), dec96 q 3072-27071 (ins); registered pair lists pairsB_del/ins (cycle 197).
B=${B:-/workspace/k4c199}; T=$B/repo/tools/cycle197; S=$B/sup; X=$B/cmp197; O=$B/work/run; export OMP_NUM_THREADS=7
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
mkdir -p $O; date +"start %T %Z"
timeout 240 $X perm $K4 $S/dec98.bin 98 del K4c1 4116 28116 - $S/tab2.txt - $T/pairsB_del.txt 0.002 > $O/k4_B_del_c1.txt
timeout 200 $X perm $K4 $S/dec96.bin 96 ins K4c1 3072 27072 - $S/tab2.txt - $T/pairsB_ins.txt 0.002 > $O/k4_B_ins_c1.txt
date +"k4 done %T %Z"
for s in K4 $(seq 19951 19969); do
  if [ $s = K4 ]; then ct=$K4; else ct=$(python3 -c "import random;s=list('$K4');random.Random($s).shuffle(s);print(''.join(s))"); fi
  timeout 30 $X perm $ct $S/dec98_c1s64.bin 98 del n$s 0 375 - $S/tab2.txt - $T/pairsB_del.txt 0.002 > $O/g_del_$s.txt
  timeout 30 $X perm $ct $S/dec96_c1s64.bin 96 ins n$s 0 375 - $S/tab2.txt - $T/pairsB_ins.txt 0.002 > $O/g_ins_$s.txt; done
date +"nulls done %T %Z"
