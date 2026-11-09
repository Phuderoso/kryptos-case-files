#!/bin/bash
# Cycle 169 (I-087 + I-090): named running keys behind the 165,782 K3-law decimations + spiral/diagonal routes,
# one wrong crib letter or one wrong carved letter at a crib position (>= 23 of 24), masked depth diagnostic.
# Reuses cycle 168's run folder inputs (all.bin, chunk_00..15, texts.txt, ctl/) by symlink/copy; checkpointed: every
# output ends in a SUMMARY line and finished outputs are skipped on rerun. Stages: controls -> K4 16 chunks -> 40 nulls.
set -e
W=${W:-/workspace/k4c169/run}; T=$(cd "$(dirname "$0")" && pwd); R=${R:-/workspace/k4c168/run}; cd $W
for f in texts.txt all.bin $(cd $R && ls chunk_??); do [ -e $f ] || ln -s $R/$f .; done
[ -d ctl168 ] || cp -r $R/ctl ctl168
gcc -O3 -march=native -o bookrk1e $T/bookrk1e.c; gcc -O3 -march=native -o bookrk_strict $T/../bookrk.c
[ -f ctl169/planted.txt ] || python3 $T/ctl169.py all.bin texts.txt ctl168 16901
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
# null slice: first 500 decimations + last 500 routes (1,000 perms), 40 shuffled K4s (seed 16940)
[ -f nullslice.bin ] || { head -c $((194*500)) all.bin > nullslice.bin; tail -c $((194*500)) all.bin >> nullslice.bin; }
[ -f nulls169.txt ] || python3 -c "
import random;K='$K4';r=random.Random(16940)
for i in range(40): l=list(K); r.shuffle(l); print(''.join(l))" > nulls169.txt
mkdir -p out
{ for c in ctl169/*.txt; do b=$(basename $c .txt); [ $b = planted ] && continue
    o=out/ctl_$b.out; grep -qs '^SUMMARY' $o || echo "./bookrk1e $(cat $c) ctl169/${b}_slice.bin texts.txt 20 > $o.tmp && mv $o.tmp $o"
    o=out/ctlS_$b.out; grep -qs '^SUMMARY' $o || echo "./bookrk_strict $(cat $c) ctl169/${b}_slice.bin texts.txt 30 > $o.tmp && mv $o.tmp $o"; done
  for c in chunk_??; do o=out/k4_$c.out; grep -qs '^SUMMARY' $o || echo "./bookrk1e $K4 $c texts.txt 11 > $o.tmp && mv $o.tmp $o"; done
  o=out/k4_nullslice.out; grep -qs '^SUMMARY' $o || echo "./bookrk1e $K4 nullslice.bin texts.txt 9 > $o.tmp && mv $o.tmp $o"
  i=0; while read t; do o=out/null${i}.out; i=$((i+1)); grep -qs '^SUMMARY' $o && continue
    echo "./bookrk1e $t nullslice.bin texts.txt 9 > $o.tmp && mv $o.tmp $o"; done < nulls169.txt
} | xargs -P ${NP:-8} -I{} bash -c "{}"
