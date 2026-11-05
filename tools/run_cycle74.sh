#!/bin/bash
# Cycle 74 audit: Sanborn-convention running-key controls through bookrk (cycles 35-36) and carved_rk69 (cycles 34, 69, 70).
# Needs: perms97.bin (165,065 cycle-12 transpositions; first 3,000 used), carter1.txt (cycle 35), tools/kryptos_text.py,
# tools/solve_k1_k2_k3.py, tools/sanborn_controls.py, tools/bookrk.c, tools/carved_rk69.c.
set -e; W=/workspace/k4c74; mkdir -p $W/out; cd $W
gcc -O2 -o bookrk bookrk.c; gcc -O2 -o carved_rk carved_rk69.c
python3 -c "import numpy as np;p=np.fromfile('perms97.bin',dtype=np.int16).reshape(-1,97);p[:3000].tofile('p3k.bin')"
python3 gen74.py
for n in 0 1 2 3 4; do ./bookrk $(cat ctl_$n.txt) p3k.bin texts_long.txt 14 > out/book_ctl$n.out & done
for n in 0 1 2 3 4 5 6; do ./carved_rk $(cat ctl_$n.txt) p3k.bin texts_all.txt 20 > out/crk_ctl$n.out & done
python3 -c "from kryptos_text import K4;open('k4.txt','w').write(K4)"
./bookrk $(cat k4.txt) p3k.bin texts_long.txt 12 > out/book_k4.out & ./carved_rk $(cat k4.txt) p3k.bin texts_all.txt 12 > out/crk_k4.out & wait
python3 verify74.py
