#!/bin/bash
# Cycle 136: transposition-first Quagmire III autokey on vocabulary alphabets.
# Any primer of length 1..LMAX, PT- and CT-fed, carved-index and plaintext-index,
# both bank directions. Texts run sequentially so K4 is a checkpoint before the nulls.
set -e
W=${W:-/workspace/k136}; B=/home/box/kryptos_support_backup/perms97.bin; cd "$W"
K=$(cat /tmp/kcf/data/k4.txt)
N1=$(grep "^null1 " controls.txt|cut -d' ' -f2)
N2=$(grep "^null2 " controls.txt|cut -d' ' -f2)
nq=$(wc -l < all.txt)
LMAX=${LMAX:-16}

run_one() {
  local lab=$1 ct=$2
  {
    for ((lo=0; lo<nq; lo+=200)); do echo "$ct" "$lab" "$lo" "$((lo+200))"; done
  } | xargs -P 8 -L 1 sh -c './akcarve "$0" all.txt '"$B"' "$1" "$2" "$3" '"$LMAX"' > out_"$1"_"$2".txt'
  date > "done_${lab}.txt"
}

run_one K4 "$K"
run_one null1 "$N1"
run_one null2 "$N2"

cat out_*.txt | grep -E '^(S|CLUSTER)' > survivors.txt || true
for lab in K4 null1 null2; do
  cat out_${lab}_*.txt | awk -v l=$lab '/^C/{c+=$7;k+=$9;s+=$11} END{print l, "tests", c, "consistent", k, "survivors", s}'
done > results.txt
date > done.txt
