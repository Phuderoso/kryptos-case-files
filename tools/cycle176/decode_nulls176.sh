#!/bin/bash
# Decode every null fit with the same budget as K4 (decode176.py), 6 at a time.
W=${W:-/workspace/k4c176}; cd $W; mkdir -p run/dec
while read lab ct; do echo "$lab $ct"; done < run/nulls176.txt | xargs -P 6 -L 1 sh -c \
 'nice -n 5 python3 repo/tools/cycle176/decode176.py "$1" support/all.bin support/quadgrams.json run/cfg176.txt "$0" run/dec/"$0".txt $(ls run/out/"$0".g0.txt run/out/"$0".g0L8.txt run/out/"$0".w0.txt run/out/"$0".pg0.txt run/out/"$0".pg1.txt 2>/dev/null) && python3 repo/tools/cycle176/decode176.py "$1" support/all_s8.bin support/quadgrams.json run/cfg176.txt "$0" run/dec/"$0".s8.txt run/out/"$0".g1.txt run/out/"$0".w1.txt'
