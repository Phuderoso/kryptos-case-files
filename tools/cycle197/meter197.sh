#!/bin/bash
# Cycle 197 chance meter (I-193): uniform random 97-letter texts (seeds 19701-19740 direct; 19741-19750 on the sample banks).
B=${B:-/workspace/k4c197}; T=$B/repo/tools/cycle197; D=$B/repo/data/cycle197; S=$B/sup; X=$B/cmp197
for s in $(seq 19701 19740); do ct=$(python3 -c "import random;r=random.Random($s);print(''.join(r.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(97)))")
  $X rec $ct $D/recs197_direct.txt 98 del u$s 0 999 $S/azka2.txt $S/tab2.txt $T/pairsA_all.txt $T/pairsB_all.txt 0 | grep -v ^M | sed "s/^/D /"; done
for s in $(seq 19741 19750); do ct=$(python3 -c "import random;r=random.Random($s);print(''.join(r.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(97)))")
  for k in "98 del" "96 ins"; do set -- $k
    $X perm $ct $S/dec$1_s32.bin $1 $2 u$s 0 999999 $S/azka2.txt - $T/pairsA_$2.txt - 0 | grep -v ^M | sed "s/^/T /"
    $X perm $ct $S/decM$1_s8.bin $1 $2 u$s 0 999999 - $S/tab2.txt - $T/pairsB_$2.txt 0 | grep -v ^M | sed "s/^/T /"; done; done
