#!/bin/bash
# Cycle 191 planted controls: plant191.py (seed 19100) -> cmp191 on ctl191.bin with tab4 (print every fit with E_config <= 1) -> checkctl191.py
W=${W:-/workspace/k4c191/w}; cd $W; mkdir -p run/ctl
python3 tools/plant191.py support/ctl191.bin run/plants191.txt
while read name row model exp ct; do OMP_NUM_THREADS=8 timeout 30 run/cmp191 $ct support/ctl191.bin support/tab4.txt $name 0 99 26 1 > run/ctl/$name.txt; done < run/plants191.txt
python3 tools/checkctl191.py run/plants191.txt run/ctl
