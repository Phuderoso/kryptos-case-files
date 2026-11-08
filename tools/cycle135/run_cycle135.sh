#!/bin/bash
# Cycle 135: transposition-first periodic Quagmire (I/II/III) on vocabulary alphabets.
# Any key of period 1..PMAX, carved-index and plaintext-index, both bank directions.
W=${W:-/workspace/k135}; B=/home/box/kryptos_support_backup/perms97.bin; cd "$W"
K=$(cat /tmp/kcf/data/k4.txt)
N1=$(grep "^null1 " controls.txt|cut -d' ' -f2)
N2=$(grep "^null2 " controls.txt|cut -d' ' -f2)
nq=$(wc -l < all.txt)
PMAX=${PMAX:-16}
{
  for lab in K4 null1 null2; do
    ct=$K; [ $lab = null1 ] && ct=$N1; [ $lab = null2 ] && ct=$N2
    for ((lo=0; lo<nq; lo+=200)); do echo "$ct" "$lab" "$lo" "$((lo+200))"; done
  done
} | xargs -P 8 -L 1 sh -c './carveq "$0" all.txt '"$B"' "$1" "$2" "$3" '"$PMAX"' > out_"$1"_"$2".txt'
cat out_*.txt | grep -E '^(S|CLUSTER)' > survivors.txt || true
for lab in K4 null1 null2; do
  cat out_${lab}_*.txt | awk -v l=$lab '/^C/{c+=$7;k+=$9;s+=$11} END{print l, "tests", c, "consistent", k, "survivors", s}'
done > results.txt
date > done.txt
