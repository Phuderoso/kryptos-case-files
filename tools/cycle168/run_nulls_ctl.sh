#!/bin/bash
# Cycle 168 part A nulls (NNULL shuffled K4s, default 24 = first 24 of nulls40.txt; 40 prepared on chunk_15 = last 10,352 decimations + all 6,070 routes) and the 12 planted
# controls on their 2,000-perm slices (controls first). Checkpointed like run_part_a.sh (finished outputs end in SUMMARY).
W=${W:-/workspace/k4c168/run}; cd $W; mkdir -p out
python3 - <<'P'
import random
K4='OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR'; r=random.Random(16840)
with open('nulls40.txt','w') as f:
    for i in range(40): l=list(K4); r.shuffle(l); f.write(''.join(l)+'\n')
P
{ for c in ctl/ctl*.txt; do b=$(basename $c .txt); o=out/$b.out; grep -qs '^SUMMARY' $o && continue
    echo "./bookrk $(cat $c) ctl/${b}_slice.bin texts.txt 12 > $o.tmp && mv $o.tmp $o"; done
  i=0; head -n ${NNULL:-24} nulls40.txt | while read t; do o=out/null${i}_chunk_15.out; i=$((i+1)); grep -qs '^SUMMARY' $o && continue
    echo "./bookrk $t chunk_15 texts.txt 9 > $o.tmp && mv $o.tmp $o"; done; } | xargs -P 8 -I{} bash -c "{}"
