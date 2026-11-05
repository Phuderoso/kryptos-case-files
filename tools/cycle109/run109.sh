#!/bin/sh
# Cycle 109: exact counts of consistent column orders, periodic substitution then columnar transposition.
# Planted controls (seed 109), then K4 plus 3 shuffled nulls (seed 1090) per configuration.
cd "$(dirname "$0")"
timeout 200 python3 subcol_count.py ctl > ctl109.txt &
for c in 14,7,1 14,14,1 13,13,1 21,3,0 21,7,0 21,21,0 21,3,1 21,7,1 21,21,1; do
  timeout 470 python3 subcol_count.py run 3 $c > k4_$c.txt &
done
wait
