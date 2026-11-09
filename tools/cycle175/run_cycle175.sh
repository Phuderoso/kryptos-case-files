#!/bin/bash
# Cycle 175 (I-111 + I-113): K4 on the full families, then K4 + 19 nulls on every 8th perm. Resumable (files with END are skipped).
W=${W:-/workspace/k4c175}; cd $W; mkdir -p run/out
K4=$(cat run/k4.txt)
jobs() {
  echo "hill $K4 k4full support/all.bin 2 4"
  for m in "delx 98 dec98" "insx 96 dec96"; do set -- $m
    echo "slip $K4 k4full $1 $2 support/$3.bin"; echo "slip $K4 k4s8 $1 $2 support/$3_s8.bin"
    while read lab ct; do echo "slip $ct $lab $1 $2 support/$3_s8.bin"; done < run/nulls175.txt
  done
  echo "hill $K4 k4s8 support/all_s8.bin 4 4"
  while read lab ct; do echo "hill $ct $lab support/all_s8.bin 4 4"; done < run/nulls175.txt; }
jobs | while read kind ct lab a b c; do
  if [ $kind = slip ]; then f=run/out/$lab.$a.txt; else f=run/out/$lab.hill.txt; fi
  [ -s $f ] && grep -q '^END' $f || echo "$kind $ct $lab $a $b $c"; done |
  xargs -P 3 -L 1 sh -c '
    if [ "$0" = slip ]; then OMP_NUM_THREADS=3 run/slip175 "$5" "$4" "$3" "$1" 26 20 4 0 9999999 > run/out/"$2"."$3".tmp && mv run/out/"$2"."$3".tmp run/out/"$2"."$3".txt
    else run/hill175 "$1" "$3" "$2" 0 9999999 "$4" "$5" 4 > run/out/"$2".hill.tmp && mv run/out/"$2".hill.tmp run/out/"$2".hill.txt; fi'
date > run/out/done.txt
