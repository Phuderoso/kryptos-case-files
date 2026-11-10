#!/bin/bash
# Cycle 194 one-error chance-meter check (I-193, I-205) BEFORE any K4 run: 40 uniform random texts (seeds 19440-19479) on all_s2048
# (81 routes), all 625 ordered pairs, both models, mode 1 (statistic S1 with exact expectation U). Two-tableau (tab2, 4 forms) and one-tableau
# stacks (tab1s, VV/VB) metered APART (I-205).
W=${W:-/workspace/k4c194/w}; cd $W; mkdir -p run/meter2 run/meter1
for s in $(seq 19440 19479); do ct=$(python3 -c "import random;R=random.Random($s);print(''.join(chr(65+R.randrange(26)) for _ in range(97)))")
  OMP_NUM_THREADS=8 setsid timeout 60 run/cmp194 $ct support/all_s2048.bin support/tab2.txt u$s 0 999999 run/pairs_all.txt 0 1 15 | grep -E '^(B|END)' > run/meter2/u$s.txt
  OMP_NUM_THREADS=8 setsid timeout 60 run/cmp194 $ct support/all_s2048.bin support/tab1s.txt u$s 0 999999 run/pairs_all.txt 0 1 3 | grep -E '^(B|END)' > run/meter1/u$s.txt; done
echo "two-tableau (AZ>KA, KA>AZ):"; python3 tools/meter194.py run/meter2
echo "one-tableau stacks (AZ>AZ, KA>KA; additive, lumpy in 26-bundles, I-205):"; python3 tools/meter194.py run/meter1
