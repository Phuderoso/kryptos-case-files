#!/bin/bash
# Cycle 195 chance-meter check (I-193, split by tableau type per I-205) BEFORE any K4 run: 40 uniform random texts (seeds 19540-19579) on
# col1_s8 (460 keyword-columnar rows) and col2_s32 (529 double rows), tab2 (two-tableau) and tab1s (one-tableau) separately, all 625
# pairs, models S1 and S2; plus 400 further texts (seeds 19580-19979) for the lumpy one-tableau meter on col1_s8.
W=${W:-/workspace/k4c195/w}; cd $W
for bank in col1_s8 col2_s32; do for tb in tab2 tab1s; do d=run/meter/${bank}_$tb; mkdir -p $d
  for s in $(seq 19540 19579); do ct=$(python3 -c "import random;R=random.Random($s);print(''.join(chr(65+R.randrange(26)) for _ in range(97)))")
    OMP_NUM_THREADS=8 timeout 60 run/cmp193 $ct support/$bank.bin support/$tb.txt u$s 0 999999 26 0.002 | grep -E '^(B|END)' > $d/u$s.txt; done
  echo "== $bank $tb (40 texts)"; python3 tools/meter195.py $d; done; done
d=run/meter/col1_s8_tab1s_400; mkdir -p $d
for s in $(seq 19580 19979); do ct=$(python3 -c "import random;R=random.Random($s);print(''.join(chr(65+R.randrange(26)) for _ in range(97)))")
  OMP_NUM_THREADS=8 timeout 60 run/cmp193 $ct support/col1_s8.bin support/tab1s.txt u$s 0 999999 26 0.002 | grep -E '^(B|END)' > $d/u$s.txt; done
echo "== col1_s8 tab1s (400 further texts)"; python3 tools/meter195.py $d
