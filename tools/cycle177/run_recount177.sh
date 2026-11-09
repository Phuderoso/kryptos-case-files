#!/bin/bash
# Cycle 177 recount: gm177/pg177 and the numpy recount on the 49-perm slice (all.bin[::4000] + planted perms) for K4, 2 nulls
# and 4 plants (one-error G ix0/ix1, GB base 7, PG1 ix1).
W=${W:-/workspace/k4c177w}; cd $W; mkdir -p run/rc; T=/workspace/k4c177/tools/cycle177; export OMP_NUM_THREADS=2
{ echo "k4 $(cat run/k4.txt)"; head -2 run/nulls177.txt; grep -E '^(ctl1|ctl2|ctl9|ctl6) ' run/controls177.txt | cut -d' ' -f1,2; } > run/rc/texts.txt
args=""
while read lab ct; do
  for ix in 0 1; do run/gm177 $ct run/slice177.bin $lab 0 999 $ix 2 4 10 1; run/gm177 $ct run/slice177.bin $lab 0 999 $ix 2 4 7 0; run/pg177 $ct run/slice177.bin run/cfg176.txt $lab $ix; done > run/rc/$lab.C.txt
  args="$args $lab=$ct"
done < run/rc/texts.txt
while read lab ct; do echo "$lab=$ct"; done < run/rc/texts.txt | xargs -P 6 -I{} bash -c 'a="{}"; python3 '$T'/recount177.py run/slice177.bin run/cfg176.txt "$a" > run/rc/${a%%=*}.R.txt'
cat run/rc/*.R.txt > run/rc/recount_all.txt
python3 $T/cmp_recount177.py run/rc/recount_all.txt run/rc/*.C.txt > run/recount177.txt
# second, targeted slice (L 5, K4 only): the perms of every K4 one-error fit at L 4-5 (both ix) + 12 random perms, split in 6
python3 - <<'PY'
import numpy as np
A=np.fromfile('run/slice177b.bin',dtype=np.int16).reshape(-1,97)
for i in range(6): A[i::6].tofile(f'run/rc/s5_{i}.bin')
PY
K4=$(cat run/k4.txt)
for i in 0 1 2 3 4 5; do for ix in 0 1; do run/gm177 $K4 run/rc/s5_$i.bin k4s5_$i 0 999 $ix 5 5 10 1; done > run/rc/s5_$i.C.txt; done
for i in 0 1 2 3 4 5; do echo $i; done | xargs -P 6 -I{} bash -c 'RC_L5=1 python3 '$T'/recount177.py run/rc/s5_{}.bin run/cfg176.txt k4s5_{}='$K4' > run/rc/s5_{}.R.txt'
cat run/rc/s5_*.R.txt > run/rc/recount_s5.txt
python3 $T/cmp_recount177.py run/rc/recount_s5.txt run/rc/s5_*.C.txt >> run/recount177.txt
