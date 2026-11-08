#!/bin/bash
# Cycle 132: model Q over vocabulary x vocabulary (10,056^2 pairs x 36 tableau/direction settings), K4 + 2 nulls.
W=${W:-/workspace/k4c132}; B=/home/box/kryptos_support_backup/perms97.bin; cd $W
K=$(cat /tmp/kcf/data/k4.txt); N1=$(grep "^null1 " controls.txt|cut -d' ' -f2); N2=$(grep "^null2 " controls.txt|cut -d' ' -f2)
n=$(wc -l < all.txt)
for lab in K4 null1 null2; do ct=$K; [ $lab = null1 ] && ct=$N1; [ $lab = null2 ] && ct=$N2
  for ((lo=0; lo<n; lo+=200)); do echo "$ct $lab $lo $((lo+200))"; done; done |
  xargs -P 8 -L 1 sh -c './dblq $0 all.txt all.txt '$B' $1 $2 $3 > out_$1_$2.txt'
cat out_*.txt | grep '^S' > survivors.txt
for lab in K4 null1 null2; do cat out_${lab}_*.txt | awk -v l=$lab '/^C/{c+=$5;s+=$9} END{print l, "configs", c, "survivors", s}'; done > results.txt
date > done.txt
