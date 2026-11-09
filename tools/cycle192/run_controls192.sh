#!/bin/bash
# Cycle 192 planted controls: plant192.py (seed 19200) -> cmp192 on ctl191.bin with tab4, all 600 pairs, mode 0, print every fit with U <= 1 -> checkctl192.py
W=${W:-/workspace/k4c192/w}; cd $W; mkdir -p run/ctl
python3 tools/plant192.py support/ctl191.bin run/plants192.txt
while read name row model exp sl ct; do OMP_NUM_THREADS=8 timeout 30 run/cmp192 $ct support/ctl191.bin support/tab4.txt $name 0 99 run/pairs_all.txt 1 0 > run/ctl/$name.txt; done < run/plants192.txt
python3 tools/checkctl192.py run/plants192.txt run/ctl
