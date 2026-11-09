#!/bin/bash
# Cycle 192 chance-meter check (I-193, one-error form): 40 uniform random texts (seeds 19240-19279) on all_s2048 (81 routes), tab2, all 600
# ordered pairs, mode 1 (full meter statistic S1, whose exact expectation is U). Output: per band e = round(-log26 U): configs, fits, U, S1.
W=${W:-/workspace/k4c192/w}; cd $W; mkdir -p run/meter
for s in $(seq 19240 19279); do ct=$(python3 -c "import random;R=random.Random($s);print(''.join(chr(65+R.randrange(26)) for _ in range(97)))")
  OMP_NUM_THREADS=8 timeout 60 run/cmp192 $ct support/all_s2048.bin support/tab2.txt u$s 0 999999 run/pairs_all.txt 0 1 | grep -E '^(B|END)' > run/meter/u$s.txt; done
python3 tools/meter192.py run/meter
