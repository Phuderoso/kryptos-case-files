#!/bin/bash
# Cycle 195 planted controls: plant195 -> cmp193 on ctl195.bin (7 rows), tab4, all 625 pairs, print E_config <= 0.002 (registered print threshold; rehearsal fix: 1e-4 hid P4, E_config 0.0015, a width-14 weak plant) -> checkctl195.
# Bank-level: P5 (PALIMPSEST -> KRYPTOS columnar -> ABSCISSA) on the whole col1.bin, P6 (double) on the whole col2.bin.
W=${W:-/workspace/k4c195/w}; cd $W; mkdir -p run/ctl; python3 tools/plant195.py support/ctl195.bin run/plants195.txt ${SLOT:-3}
while read name row md exp ct; do OMP_NUM_THREADS=8 timeout 30 run/cmp193 $ct support/ctl195.bin support/tab4.txt $name 0 99 26 0.002 > run/ctl/$name.txt; done < run/plants195.txt
python3 tools/checkctl195.py run/plants195.txt run/ctl
p5=$(awk '$1=="P5"{print $5}' run/plants195.txt); p6=$(awk '$1=="P6"{print $5}' run/plants195.txt)
OMP_NUM_THREADS=8 timeout 60 run/cmp193 $p5 support/col1.bin support/tab4.txt P5bank 0 999999 26 1e-6 | awk '$1=="M"' > run/ctl/P5bank.txt
OMP_NUM_THREADS=8 timeout 120 run/cmp193 $p6 support/col2.bin support/tab4.txt P6bank 0 999999 26 1e-6 | awk '$1=="M"' > run/ctl/P6bank.txt
echo "P5 on all of col1.bin (expect row 0 = KRYPTOS/enc, AZ>KA VV S1 10 8): $(awk '{print $3,$4,$5,$6,$7,$8}' run/ctl/P5bank.txt | sort | uniq -c | sort -rn | head -5 | tr '\n' ';')"
echo "P6 on all of col2.bin (expect row 2 = KRYPTOS+PALIMPSEST/enc, AZ>AZ VV S1 3 25): $(awk '{print $3,$4,$5,$6,$7,$8}' run/ctl/P6bank.txt | sort | uniq -c | sort -rn | head -5 | tr '\n' ';')"
