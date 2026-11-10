#!/bin/bash
# Cycle 196 one-error chance-meter check (I-193, I-205) BEFORE any K4 run: 40 uniform random texts (seeds 19640-19679) on col1_m45 (82 rows =
# col1.bin[::45]) and col2_m209 (81 rows = col2.bin[::209]), all 625 ordered pairs, both models, mode 1 (statistic S1, exact expectation U).
# Two-tableau (tab2, 4 forms) and one-tableau stacks (tab1s, VV/VB) metered APART (I-205). meter194.py unchanged.
W=${W:-/workspace/k4c196/w}; cd $W
for b in col1_m45 col2_m209; do mkdir -p run/meter/$b/t2 run/meter/$b/t1
for s in $(seq 19640 19679); do ct=$(python3 -c "import random;R=random.Random($s);print(''.join(chr(65+R.randrange(26)) for _ in range(97)))")
  OMP_NUM_THREADS=8 setsid timeout 60 run/cmp194 $ct support/$b.bin support/tab2.txt u$s 0 999999 run/pairs_all.txt 0 1 15 | grep -E '^(B|END)' > run/meter/$b/t2/u$s.txt
  OMP_NUM_THREADS=8 setsid timeout 60 run/cmp194 $ct support/$b.bin support/tab1s.txt u$s 0 999999 run/pairs_all.txt 0 1 3 | grep -E '^(B|END)' > run/meter/$b/t1/u$s.txt; done
echo "== $b two-tableau (AZ>KA, KA>AZ):"; python3 tools/meter194.py run/meter/$b/t2
echo "== $b one-tableau stacks (AZ>AZ, KA>KA; additive, lumpy in 26-bundles, I-205):"; python3 tools/meter194.py run/meter/$b/t1; done
