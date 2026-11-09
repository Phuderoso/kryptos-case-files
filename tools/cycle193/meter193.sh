#!/bin/bash
# Cycle 193 chance-meter check (I-193) BEFORE any K4 run: 40 uniform random texts (seeds 19340-19379) on all_s2048 (81 routes), tab4,
# all 625 ordered pairs, both sandwich models. Output per band e = round(-log26 E_config): configs, fits, solutions, E, text-level z.
W=${W:-/workspace/k4c193/w}; cd $W; mkdir -p run/meter
for s in $(seq 19340 19379); do ct=$(python3 -c "import random;R=random.Random($s);print(''.join(chr(65+R.randrange(26)) for _ in range(97)))")
  OMP_NUM_THREADS=8 timeout 60 run/cmp193 $ct support/all_s2048.bin support/tab4.txt u$s 0 999999 26 0.002 | grep -E '^(B|END)' > run/meter/u$s.txt; done
python3 tools/meter193.py run/meter
