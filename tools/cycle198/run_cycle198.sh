#!/bin/bash
# Cycle 198 registered run (PREREG198). Own process group; every step under timeout; decimation stage in q-chunks of 1000 perms with
# checkpoints (a chunk whose output already ends in END is skipped, so the script is resumable).
B=${B:-/workspace/k4c198}; T=$B/src; S=$B/sup; X=$B/cmp198; O=$B/work/run; export OMP_NUM_THREADS=${OMP_NUM_THREADS:-6}
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
mkdir -p $O; date +"start %T %Z"
done_() { [ -s "$1" ] && tail -1 "$1" | grep -q ^END; }
done_ $O/k4_dir.txt || timeout 60 $X rec $K4 $S/recs197_direct.txt 98 del K4dir 0 999 $S/azka2.txt $S/tab2.txt $T/pairsA_all.txt $T/pairsB_all.txt 0.05 > $O/k4_dir.txt
for k in "98 del 4116" "96 ins 3072"; do set -- $k
  for lo in $(seq 0 1000 $(($3 - 1))); do f=$O/k4_decM$1_$lo.txt
    done_ $f || timeout 400 $X perm $K4 $S/decM$1.bin $1 $2 K4decM $lo $((lo + 1000)) $S/azka2.txt $S/tab2.txt $T/pairsA_$2.txt $T/pairsB_$2.txt 0.05 > $f
    date +"chunk decM$1 $lo %T %Z"; done; done
date +"k4 done %T %Z"
for s in $(seq 19851 19869); do ct=$(python3 -c "import random;s=list('$K4');random.Random($s).shuffle(s);print(''.join(s))")
  done_ $O/null_dir_$s.txt || timeout 60 $X rec $ct $S/recs197_direct.txt 98 del n$s 0 999 $S/azka2.txt $S/tab2.txt $T/pairsA_all.txt $T/pairsB_all.txt 0.05 > $O/null_dir_$s.txt
  for k in "98 del" "96 ins"; do set -- $k
    done_ $O/null_M$1_$s.txt || timeout 60 $X perm $ct $S/decM$1_s128.bin $1 $2 n$s 0 999999 $S/azka2.txt $S/tab2.txt $T/pairsA_$2.txt $T/pairsB_$2.txt 0.05 > $O/null_M$1_$s.txt; done; done
for k in "98 del" "96 ins"; do set -- $k
  done_ $O/grid_M$1_K4.txt || timeout 60 $X perm $K4 $S/decM$1_s128.bin $1 $2 g4 0 999999 $S/azka2.txt $S/tab2.txt $T/pairsA_$2.txt $T/pairsB_$2.txt 0.05 > $O/grid_M$1_K4.txt; done
date +"nulls done %T %Z"
