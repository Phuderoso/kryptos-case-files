#!/bin/bash
# Cycle 64 full run: K4, 2 shuffled nulls and 4 planted controls over all 367,184 word entries, 8 parts each.
cd "${WORKDIR:-$(dirname "$0")}"
for name in K4 NULL0 NULL1 CTL1 CTL2 CTL3 CTL4; do
  if [ $name = K4 ]; then t=$(cat k4.txt); else t=$(grep "^$name " ctl64.txt|cut -d' ' -f2); fi
  for p in 0 1 2 3 4 5 6 7; do LMAX=22 ./c64 $t qg.bin words64.txt $p 8 > ${name}_p$p.out & done; wait
done
echo DONE
