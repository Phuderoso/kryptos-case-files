#!/bin/bash
# Cycle 197 registered K4 run (PREREG197). Own process group; every step under timeout.
B=${B:-/workspace/k4c197}; T=$B/repo/tools/cycle197; D=$B/repo/data/cycle197; S=$B/sup; X=$B/cmp197; O=$B/work/run
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
mkdir -p $O; date +"start %T %Z"
timeout 120 $X rec $K4 $D/recs197_direct.txt 98 del K4dirA 0 999 $S/alpha_direct189.txt - $T/pairsA_all.txt - 0.002 > $O/k4_dirA.txt
timeout 60 $X rec $K4 $D/recs197_direct.txt 98 del K4dirB 0 999 - $S/tab2.txt - $T/pairsB_all.txt 0.002 > $O/k4_dirB.txt
timeout 240 $X perm $K4 $S/dec98.bin 98 del K4decA 0 999999 $S/azka2.txt - $T/pairsA_del.txt - 0.002 > $O/k4_decA_del.txt
timeout 240 $X perm $K4 $S/dec96.bin 96 ins K4decA 0 999999 $S/azka2.txt - $T/pairsA_ins.txt - 0.002 > $O/k4_decA_ins.txt
timeout 120 $X perm $K4 $S/decM98.bin 98 del K4decB 0 999999 - $S/tab2.txt - $T/pairsB_del.txt 0.002 > $O/k4_decB_del.txt
timeout 120 $X perm $K4 $S/decM96.bin 96 ins K4decB 0 999999 - $S/tab2.txt - $T/pairsB_ins.txt 0.002 > $O/k4_decB_ins.txt
date +"k4 done %T %Z"
for s in $(seq 19751 19769); do ct=$(python3 -c "import random;s=list('$K4');random.Random($s).shuffle(s);print(''.join(s))")
  timeout 30 $X rec $ct $D/recs197_direct.txt 98 del n$s 0 999 $S/azka2.txt $S/tab2.txt $T/pairsA_all.txt $T/pairsB_all.txt 0.002 > $O/null_dir_$s.txt
  for k in "98 del" "96 ins"; do set -- $k
    timeout 60 $X perm $ct $S/dec$1_s32.bin $1 $2 n$s 0 999999 $S/azka2.txt - $T/pairsA_$2.txt - 0.002 > $O/null_A_$2_$s.txt
    timeout 60 $X perm $ct $S/decM$1_s8.bin $1 $2 n$s 0 999999 - $S/tab2.txt - $T/pairsB_$2.txt 0.002 > $O/null_B_$2_$s.txt; done; done
# K4 on the same sample banks (grid comparability)
$X rec $K4 $D/recs197_direct.txt 98 del g4 0 999 $S/azka2.txt $S/tab2.txt $T/pairsA_all.txt $T/pairsB_all.txt 0.002 > $O/grid_dir_K4.txt
for k in "98 del" "96 ins"; do set -- $k
  timeout 60 $X perm $K4 $S/dec$1_s32.bin $1 $2 g4 0 999999 $S/azka2.txt - $T/pairsA_$2.txt - 0.002 > $O/grid_A_$2_K4.txt
  timeout 60 $X perm $K4 $S/decM$1_s8.bin $1 $2 g4 0 999999 - $S/tab2.txt - $T/pairsB_$2.txt 0.002 > $O/grid_B_$2_K4.txt; done
date +"nulls done %T %Z"
