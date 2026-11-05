#!/bin/sh
# Cycle 58: Portax exact crib test. Run from a scratch dir with this repo at $R.
R=${R:-/workspace/kcl}
gcc -O3 -march=native -o portax $R/tools/portax.c
python3 $R/tools/mk58.py                      # writes texts58.txt (K4, 5 nulls, CTL1-5)
grep -v "^K4\|NULL" texts58.txt > ctl.txt; grep -E "^(K4|NULL|CTL5)" texts58.txt > main.txt
./portax texts58.txt $R/data/alpha.bin 2 $R/data/c12_perm.bin 96630 48      # A-Z and KRYPTOS, behind cycle-12 transpositions, both orders
./portax texts58.txt $R/data/alpha.bin 86731 $R/data/c12_perm.bin 1 48      # every keyed alphabet, directly
python3 -c "T=open('$R/data/tw_alpha.bin','rb').read(); [open(f'tw{c}.bin','wb').write(T[c*33*26:min(264,(c+1)*33)*26]) for c in range(8)]"
for c in 0 1 2 3 4 5 6 7; do ./portax main.txt tw$c.bin $(( $(stat -c%s tw$c.bin)/26 )) $R/data/c12_perm.bin 96630 48 > tw$c.out & done; wait
