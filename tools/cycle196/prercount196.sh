#!/bin/bash
# Cycle 196 pre-K4 exactness recount: recount196.py (independent, literal tables, all 25 deletions, no reduction) vs cmp194 (every fit, U <= 1e30)
# on a uniform random text (seed 19640), ctl195.bin rows 0 (col1 KRYPTOS/enc) and 4 (col2 KRYPTOS+PALIMPSEST/enc), all 1,250 model-pairs, tab2 x 4 forms + tab1s x VV/VB.
W=${W:-/workspace/k4c196/w}; cd $W; S=support; ct=$(cat run/u19640.txt); mkdir -p run/rc0
setsid timeout 200 python3 tools/recount196.py $ct $S/ctl195.bin 0,4 $S/tab2.txt run/pairs_all_x.txt > run/rc0/r2.txt & setsid timeout 200 python3 tools/recount196.py $ct $S/ctl195.bin 0,4 $S/tab1s.txt run/pairs_all_x.txt VV,VB > run/rc0/r1.txt; wait
cat run/rc0/r2.txt run/rc0/r1.txt | sort > run/rc0/r.txt
python3 -c "import numpy as np;a=np.fromfile('$S/ctl195.bin',dtype=np.int16).reshape(-1,97);a[[0,4]].tofile('$S/ctl195_r04.bin')"
{ OMP_NUM_THREADS=8 setsid timeout 30 run/cmp194 $ct $S/ctl195_r04.bin $S/tab2.txt u 0 99 run/pairs_all.txt 1e30 0 15; OMP_NUM_THREADS=8 setsid timeout 30 run/cmp194 $ct $S/ctl195_r04.bin $S/tab1s.txt u 0 99 run/pairs_all.txt 1e30 0 3; } | awk '$1=="M"{r=($3==0)?0:4; print "F",r,$6,$4,$5,$7,$8}' | sort > run/rc0/c.txt
cmp -s run/rc0/r.txt run/rc0/c.txt && echo "pre-K4 recount identical $(wc -l < run/rc0/c.txt) fits" || { echo "pre-K4 recount DIFFER"; diff run/rc0/r.txt run/rc0/c.txt | head; }
