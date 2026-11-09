#!/bin/bash
# Cycle 151: Hill n=2..4 under one carving error (hill1e.c), direct + full 165,065-entry bank (both directions,
# model Q and carved order), A-Z/KRYPTOS numbering, every alignment. Texts: K4 + two shuffled-K4 nulls (plant.py).
# Resumable: a chunk whose output already has its "C" line is skipped.
W=${W:-/workspace/k151}; P=/home/box/kryptos_support_backup/perms97.bin; cd "$W"; K4=$(cat /tmp/kcf/data/k4.txt); mkdir -p out
for l in K4 null1 null2; do T=$([ $l = K4 ] && echo $K4 || awk -v l=$l '$1==l{print $6}' controls.txt)
  for n in 2 3 4; do echo "$l $T $n D 0 1"; for c in 0 1 2 3 4 5 6 7; do echo "$l $T $n B $((c*20634)) $(( c==7 ? 165065 : (c+1)*20634 ))"; done; done; done |
 xargs -P 8 -L 1 sh -c 'f=out/$0_n$2_$3_$4.txt; grep -q "^C " $f 2>/dev/null && exit 0;
   if [ $3 = D ]; then ./hill1e $1 - D$0 0 1 1 $2 > $f.tmp; else ./hill1e $1 '$P' $0 $4 $5 1 $2 > $f.tmp; fi && mv $f.tmp $f'
