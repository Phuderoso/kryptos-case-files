#!/bin/bash
# Cycle 177 decodes (pre-registered set + the C2 flag rule): K4 and the first 5 nulls, 6 parallel processes.
# ix 0 model-G fits up to L 6 (L 6 added because C2 = G1 ix0 L6 was flagged: K4 above all 19 nulls); ix 1 all (K4 full set,
# nulls 1/8); named primers all; GB ix0 L <= 6 and ix 1 all. PG1 had no fits.
W=${W:-/workspace/k4c177w}; cd $W; mkdir -p run/dec; D=/workspace/k4c177/tools/cycle177/decode177.py
{ K4=$(cat run/k4.txt)
  for g in g0e w0e b0 g1e w1e b1; do echo "$K4 k4 $g run/out/k4.$g.txt"; done
  head -5 run/nulls177.txt | while read lab ct; do for g in g0e w0e b0 g1e w1e b1; do echo "$ct $lab $g run/out/$lab.$g.txt"; done; done
} | xargs -P 6 -L 1 bash -c 'python3 '$D' $0 support/all.bin support/quadgrams.json run/cfg176.txt $1 run/dec/$1.$2.dec 6 $3' 
# the ix-1 null runs used all_s8.bin: decode them against that perm file
head -5 run/nulls177.txt | while read lab ct; do for g in g1e w1e b1; do echo "$ct $lab $g run/out/$lab.$g.txt"; done; done | \
  xargs -P 6 -L 1 bash -c 'python3 '$D' $0 support/all_s8.bin support/quadgrams.json run/cfg176.txt $1 run/dec/$1.$2.dec 6 $3'
date > run/dec/done.txt
