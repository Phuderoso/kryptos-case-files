#!/bin/bash
# Cycle 173 (I-105): K4 on the full families, then K4 + 19 nulls on every 4th perm. Resumable (files with END are skipped).
W=${W:-/workspace/k4c173}; cd $W; mkdir -p run/out
T=run/anom173; K4=$(cat run/k4.txt)
jobs() {
  for m in "del 98 dec98" "ins 96 dec96" "chg 97 all" "swp 97 all"; do set -- $m
    echo "$K4 k4full $1 $2 support/$3.bin 21"
    echo "$K4 k4s4 $1 $2 support/$3_s4.bin 21"
    while read lab ct; do echo "$ct $lab $1 $2 support/$3_s4.bin 21"; done < run/nulls173.txt
  done; }
jobs | while read ct lab mo n pf pp; do f=run/out/$lab.$mo.txt; [ -s $f ] && grep -q '^END' $f || echo "$ct $lab $mo $n $pf $pp"; done |
  xargs -P 2 -L 1 sh -c 'OMP_NUM_THREADS=4 '"$T"' "$4" "$3" "$2" "$0" 26 "$5" 0 999999 > run/out/"$1"."$2".tmp && mv run/out/"$1"."$2".tmp run/out/"$1"."$2".txt'
date > run/out/done.txt
