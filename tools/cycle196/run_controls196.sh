#!/bin/bash
# Cycle 196 planted controls: plant196.py (case 182's plants, plant195.py seed 19500, + one wrong carved letter (+7) on a 2-core slot; P0 no
# error; PD pendant error; N3 two wrong letters; N1/N2/N4 negatives; N5 K3-route sandwich) -> cmp194 on ctl195.bin (7 rows), ALL 625 pairs,
# tab2 (4 forms) + tab1s (VV/VB), print every fit with U <= 1 (looser than the registered 0.05, I-214) -> checkctl196.py.
# Bank-level: P5 (PALIMPSEST -> KRYPTOS columnar -> ABSCISSA, one wrong letter) on ALL of col1.bin, P6 (double columnar, one wrong letter) on ALL of col2.bin,
# P5 with the registered col1 pair list, print U <= 0.05 (the registered threshold, I-214), listed by config U.
W=${W:-/workspace/k4c196/w}; cd $W; mkdir -p run/ctl196
python3 tools/plant195.py support/ctl195.bin run/plants195_re.txt && cmp run/plants195_re.txt run/plants195.txt && echo "plants195 reproduced"
python3 tools/plant196.py support/ctl195.bin run/plants195.txt run/plants196.txt
grep -v '^#' run/plants196.txt | while read name row model exp slot ct; do
  OMP_NUM_THREADS=8 setsid timeout 30 run/cmp194 $ct support/ctl195.bin support/tab2.txt $name 0 99 run/pairs_all.txt 1 0 15 > run/ctl196/${name}_t2.txt
  OMP_NUM_THREADS=8 setsid timeout 30 run/cmp194 $ct support/ctl195.bin support/tab1s.txt $name 0 99 run/pairs_all.txt 1 0 3 > run/ctl196/${name}_t1.txt; done
python3 tools/checkctl196.py run/plants196.txt run/ctl196 support/ctl195.bin
p5=$(awk '$1=="P5"{print $6}' run/plants196.txt); p6=$(awk '$1=="P6"{print $6}' run/plants196.txt)
OMP_NUM_THREADS=8 setsid timeout 60 run/cmp194 $p5 support/col1.bin support/tab2.txt P5bank 0 999999 run/pairs_fp_col1.txt 0.05 0 15 | awk '$1=="M"' > run/ctl196/P5bank.txt
OMP_NUM_THREADS=8 setsid timeout 90 run/cmp194 $p6 support/col2.bin support/tab1s.txt P6bank 0 999999 run/pairs_p6.txt 1e-3 0 3 | awk '$1=="M"' > run/ctl196/P6bank.txt
echo "P5 one-error on all of col1.bin (expect row 0 = KRYPTOS/enc, AZ>KA VV S1 10 8, slot 9 or its 2-core twin): $(sort -g -k9 run/ctl196/P5bank.txt | awk "{print \$3,\$4,\$5,\$6,\$7,\$8,\$9,\$10}" | head -6 | tr '\n' ';')"
echo "P6 one-error on all of col2.bin (cell 3 x 25 is LOW-POWER under one error, so only that pair is run, print U <= 1e-3; expect row 2 = KRYPTOS+PALIMPSEST/enc, AZ>AZ VV S1 3 25 among the lowest U): $(awk '{print $3,$4,$5,$6,$7,$8,$10}' run/ctl196/P6bank.txt | sort | uniq -c | sort -rn | head -5 | tr '\n' ';')"
