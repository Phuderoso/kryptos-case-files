#!/bin/bash
# Cycle 53 full run: K4, 2 shuffled nulls, 4 planted controls; 8 parts each.
cd "$(dirname "$0")"
for name in K4 NULL0 NULL1 CTL1 CTL2 CTL3 CTL4; do
  if [ $name = K4 ]; then t=$(cat k4.txt); else t=$(grep "^$name " ctl53.txt|cut -d' ' -f2); fi
  for p in 0 1 2 3 4 5 6 7; do SMAX=26 LMAX=22 ./disr $t qg.bin orders.txt dthemed.txt dperms.txt $p 8 > ${name}_p$p.out & done; wait
done
echo DONE > run53.log
