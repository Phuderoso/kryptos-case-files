#!/bin/bash
# Cycle 52 full run: K4 and 2 shuffled nulls, all 1837x1838 keyword-order pairs, 8 parts each.
cd "${WORKDIR:-$(dirname "$0")}"
for name in K4 NULL0 NULL1; do
  if [ $name = K4 ]; then t=$(cat k4.txt); else t=$(grep "^$name " ctl52.txt|cut -d' ' -f2); fi
  for p in 0 1 2 3 4 5 6 7; do SMAX=26 LMAX=22 ./dcol $t qg.bin orders.txt $p 8 > ${name}_p$p.out & done; wait
done
echo DONE
