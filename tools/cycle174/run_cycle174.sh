#!/bin/bash
# Cycle 174 (I-108): K4 on the full 165,782 perms (16 chunks per tool), then K4 + 19 nulls on all_s4.bin. Resumable:
# output files that already end with END are skipped. Run from run/ with support/ next to it. Parallel: $J jobs (default 6).
J=${J:-6}; K4=$(cat k4.txt); mkdir -p out
jobs_list() {
  NP=165782; C=$(( (NP + 15) / 16 ))
  for t in hill rag portax; do for c in $(seq 0 15); do lo=$((c*C)); hi=$(((c+1)*C)); echo "$t k4full_$c $K4 ../support/all.bin $lo $hi"; done; done
  for t in hill portax rag; do echo "$t k4s4 $K4 ../support/all_s4.bin 0 41446"; while read lab ct; do echo "$t $lab $ct ../support/all_s4.bin 0 41446"; done < nulls174.txt; done
}
run1() { t=$1; lab=$2; ct=$3; pf=$4; lo=$5; hi=$6; f=out/${t}_${lab}.txt
  if [ -f $f ] && tail -1 $f | grep -q '^END'; then return; fi
  case $t in hill) ./hill174 $ct $pf $lab $lo $hi > $f.tmp;; rag) ./rag174 $ct ../support/alpha172.txt $pf $lab $lo $hi > $f.tmp;; portax) ./portax174 $ct $pf $lab $lo $hi 48 > $f.tmp;; esac
  mv $f.tmp $f; }
export -f run1
jobs_list | xargs -P $J -L 1 bash -c 'run1 "$@"' _
echo ALLDONE
