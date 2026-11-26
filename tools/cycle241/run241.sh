#!/bin/bash
# PREREG241 runner (resumable). 10 plants (plants241.tsv, slices as run240), then 24 fresh nulls x {direct full, bank r10, all.bin r10}
# with gn235 on keys233.bin. Run under: setsid timeout 660 ./run241.sh
export OMP_NUM_THREADS=8; mkdir -p R P; set -u
KS=keys233.bin; MP=1000000; s=$(date +%s)
while IFS=$'\t' read -r id scope ct qi dr ix x y f w bad fl mo m pt; do
  [ -s P/p$id.txt ] && tail -n1 P/p$id.txt | grep -q '^T ' && continue
  if [ "$scope" = direct ]; then ./gn235 "$ct" x alpha.bin alpha.bin $KS 1000 $((y%1000)) qg.bin $MP > P/p$id.txt
  else ./gn235 "$ct" $scope.bin themed144.bin themed144.bin $KS 2000 $((qi%2000)) qg.bin $MP > P/p$id.txt; fi
done < plants241.tsv
echo "plants $(( $(date +%s)-s ))s" >> R/time.txt
run(){ # tag text
  [ -s R/$1_direct.txt ] && tail -n1 R/$1_direct.txt | grep -q '^T ' || ./gn235 $2 x alpha.bin alpha.bin $KS 1 0 qg.bin $MP > R/$1_direct.txt
  [ -s R/$1_bank_r10.txt ] && tail -n1 R/$1_bank_r10.txt | grep -q '^T ' || ./gn235 $2 bank.bin themed144.bin themed144.bin $KS 10 0 qg.bin $MP > R/$1_bank_r10.txt
  [ -s R/$1_all_r10.txt ] && tail -n1 R/$1_all_r10.txt | grep -q '^T ' || ./gn235 $2 all.bin themed144.bin themed144.bin $KS 10 0 qg.bin $MP > R/$1_all_r10.txt
  echo "$1 done $(date +%T)" >> R/time.txt; }
while IFS=$'\t' read -r seed set t sha; do run null$seed $t; done < nulls241.tsv
echo "all $(( $(date +%s)-s ))s" >> R/time.txt
