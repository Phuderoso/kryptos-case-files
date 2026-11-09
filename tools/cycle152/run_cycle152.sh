#!/bin/bash
# Cycle 152: free-form zig-zag autokey + progressive shift (zigfree.c), direct + full 165,065-entry bank (both directions,
# model Q and carved order), A-Z/KRYPTOS numbering, CT and PT feed, L 1-96, d 0-25. Texts: K4 + two shuffled-K4 nulls (plant.py).
# Print floor: CT m>=16 or m>=n-2 with n>=14; PT m=n with n>=9. Resumable: a chunk whose output has its "C" line is skipped.
W=${W:-/workspace/k152}; P=/home/box/kryptos_support_backup/perms97.bin; cd "$W"; K4=$(cat /tmp/kcf/data/k4.txt); mkdir -p out
gcc -O2 -march=native -o zigfree zigfree.c
for l in K4 null1 null2; do T=$([ $l = K4 ] && echo $K4 || awk -v l=$l '$1==l{print $NF}' controls.txt)
  echo "$l $T D 0 1"; for c in 0 1 2 3 4 5 6 7; do echo "$l $T B $((c*20634)) $(( c==7 ? 165065 : (c+1)*20634 ))"; done; done |
 xargs -P 8 -L 1 sh -c 'f=out/$0_$2_$3.txt; grep -q "^C " $f 2>/dev/null && exit 0;
   if [ $2 = D ]; then ./zigfree $1 - D$0 0 1 16 14 > $f.tmp; else ./zigfree $1 '$P' $0 $3 $4 16 14 > $f.tmp; fi && mv $f.tmp $f'
