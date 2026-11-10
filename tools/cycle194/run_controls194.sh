#!/bin/bash
# Cycle 194 planted controls: plant194.py (case 180's plants, seed 19300, + one wrong letter on a 2-core slot) -> cmp194 on ctl191.bin, all 625
# pairs, tab2 (all four forms) and tab1s (VV/VB; BB = VV, BV = VB), print every fit with U <= 1 -> checkctl194.py.
W=${W:-/workspace/k4c194/w}; cd $W; mkdir -p run/ctl
python3 tools/plant194.py support/ctl191.bin run/plants193.txt run/plants194.txt
grep -v '^#' run/plants194.txt | while read name row model exp slot ct; do
  OMP_NUM_THREADS=8 timeout 30 run/cmp194 $ct support/ctl191.bin support/tab2.txt $name 0 99 run/pairs_all.txt 1 0 15 > run/ctl/${name}_t2.txt
  OMP_NUM_THREADS=8 timeout 30 run/cmp194 $ct support/ctl191.bin support/tab1s.txt $name 0 99 run/pairs_all.txt 1 0 3 > run/ctl/${name}_t1.txt; done
python3 tools/checkctl194.py run/plants194.txt run/ctl
