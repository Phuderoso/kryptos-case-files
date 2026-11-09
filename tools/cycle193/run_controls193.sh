#!/bin/bash
# Cycle 193 planted controls: plant193.py (seed 19300) -> cmp193 on ctl191.bin with tab4 (print every fit with E_config <= 1) -> checkctl193.py.
# Non-equivalence check: the sandwich plants P1, P5 and P8 under case 178's solver cmp191 (keys on one side) must give no fit with
# E_config <= 1e-4 at their row, and N4 (a case-178 compound key) must be found by cmp191 (sanity) and not by cmp193 (checked by checkctl193).
W=${W:-/workspace/k4c193/w}; cd $W; mkdir -p run/ctl
python3 tools/plant193.py support/ctl191.bin run/plants193.txt
while read name row model exp ct; do OMP_NUM_THREADS=8 timeout 30 run/cmp193 $ct support/ctl191.bin support/tab4.txt $name 0 99 26 1 > run/ctl/$name.txt; done < run/plants193.txt
python3 tools/checkctl193.py run/plants193.txt run/ctl
for name in P1 P5 P8 N4; do read nm row model exp ct < <(awk -v n=$name '$1==n' run/plants193.txt)
  OMP_NUM_THREADS=8 timeout 30 run/cmp191 $ct support/ctl191.bin support/tab4.txt $name 0 99 26 1 > run/ctl/x191_$name.txt
  echo "cmp191 on $name (row $row): fits E<=1e-4 at row: $(awk -v r=$row '$1=="M" && $3==r && $9<=1e-4' run/ctl/x191_$name.txt | wc -l); at AZ>KA VV 7 11 P: $(awk -v r=$row '$1=="M" && $3==r && $4=="AZ>KA" && $5=="VV" && $6=="P" && $7==7 && $8==11' run/ctl/x191_$name.txt | wc -l)"; done
