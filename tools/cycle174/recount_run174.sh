#!/bin/bash
# Cycle 174 recount: Python brute force vs the C tools on the same ranges (plant slices + K4 / 2 nulls on sampled perm ranges).
mkdir -p rec; K4=$(cat k4.txt); N0=$(sed -n 1p nulls174.txt|cut -d' ' -f2); N1=$(sed -n 2p nulls174.txt|cut -d' ' -f2)
python3 - <<'PY' > rec/plants.lst
import json; d=json.load(open('ctl/plants.json'))
for p in d['plants']: print(p['id'], p['kind'], p['ct'], p['slice'], p['at'])
PY
while read id kind ct sl at; do
  case $kind in
   hill) python3 ../tools/recount174.py $ct $sl 0 200 hill p$id > rec/hill_p$id.py.txt; ./hill174 $ct $sl p$id 0 200 > rec/hill_p$id.c.txt;;
   portax) python3 ../tools/recount174.py $ct $sl $((at>5?at-5:0)) $((at+5)) portax p$id > rec/px_p$id.py.txt; ./portax174 $ct $sl p$id $((at>5?at-5:0)) $((at+5)) 48 > rec/px_p$id.c.txt;;
  esac
done < rec/plants.lst
for t in "k4 $K4" "null0 $N0" "null1 $N1"; do set -- $t
  python3 ../tools/recount174.py $2 ../support/all.bin 50000 50100 hill $1 > rec/hill_$1.py.txt; ./hill174 $2 ../support/all.bin $1 50000 50100 > rec/hill_$1.c.txt
  python3 ../tools/recount174.py $2 ../support/all.bin 120000 120030 portax $1 > rec/px_$1.py.txt; ./portax174 $2 ../support/all.bin $1 120000 120030 48 > rec/px_$1.c.txt
done
echo RECDONE
