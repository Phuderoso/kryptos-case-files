#!/bin/bash
# Cycle 133: Quagmire-III PT-autokey and keyword+PT-autokey stacks (both orders)
# behind the bank, hashed, K4 + 2 nulls.
W=${W:-/workspace/k133}; B=/home/box/kryptos_support_backup/perms97.bin; cd "$W"
K=$(cat /tmp/kcf/data/k4.txt)
N1=$(grep "^null1 " controls.txt|cut -d' ' -f2)
N2=$(grep "^null2 " controls.txt|cut -d' ' -f2)
n=$(wc -l < all.txt)
for lab in K4 null1 null2; do
  ct=$K; [ $lab = null1 ] && ct=$N1; [ $lab = null2 ] && ct=$N2
  for ((lo=0; lo<n; lo+=200)); do echo "$ct $lab $lo $((lo+200))"; done
done | xargs -P 8 -L 1 sh -c './qak "$0" all.txt '"$B"' "$1" "$2" "$3" > out_"$1"_"$2".txt'
cat out_*.txt | grep '^S' > survivors.txt || true
for lab in K4 null1 null2; do
  cat out_${lab}_*.txt | awk -v l=$lab '/^C/{c+=$4;s+=$8;k+=$10} END{print l, "configs", c, "survivors", s, "skipped_pairs", k}'
done > results.txt
date > done.txt
