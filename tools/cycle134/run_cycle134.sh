#!/bin/bash
# Cycle 134: phrase-primer PT-autokey (L 11-22) and CT-autokey (L 22-28)
# behind the bank. Q = all vocabulary keywords; S = KA/AK on themed keywords.
W=${W:-/workspace/k134}; B=/home/box/kryptos_support_backup/perms97.bin; cd "$W"
K=$(cat /tmp/kcf/data/k4.txt)
N1=$(grep "^null1 " controls.txt|cut -d' ' -f2)
N2=$(grep "^null2 " controls.txt|cut -d' ' -f2)
nq=$(wc -l < all.txt)
nt=$(wc -l < themed.txt)
{
  for lab in K4 null1 null2; do
    ct=$K; [ $lab = null1 ] && ct=$N1; [ $lab = null2 ] && ct=$N2
    for ((lo=0; lo<nq; lo+=80)); do echo "$ct" "$lab" Q "$lo" "$((lo+80))"; done
    for ((lo=0; lo<nt; lo+=8)); do echo "$ct" "$lab" S "$lo" "$((lo+8))"; done
  done
} | xargs -P 8 -L 1 sh -c './qphrase "$0" all.txt themed.txt '"$B"' "$1" "$2" "$3" "$4" > out_"$1"_"$2"_"$3".txt'
cat out_*.txt | grep -E '^(S|CLUSTER)' > survivors.txt || true
for lab in K4 null1 null2; do
  cat out_${lab}_*.txt | awk -v l=$lab '/^C/{c+=$7;k+=$9;s+=$11} END{print l, "tests", c, "consistent", k, "survivors", s}'
done > results.txt
date > done.txt
