#!/bin/bash
# Cycle 79 audit of cycle 45 (running keys behind rail fence / Redefence / AMSCO) + gap closure.
# Needs: /workspace/k4c44/perms_A.bin, perms_B.bin (tools/railamsco_gen.py, cycle 44); /workspace/k4c45/texts.txt and
# chunk_0..7 (tools/run_cycle45.sh); tools/kryptos_text.py, solve_k1_k2_k3.py, sanborn_controls.py, bookrk.c, carved_rk69.c.
set -e; W=/workspace/k4c79; mkdir -p $W/out; cd $W
gcc -O3 -march=native -o bookrk bookrk.c; gcc -O3 -march=native -o carved_rk carved_rk69.c
python3 gen79.py                      # textbook transpositions -> family membership; 7 Sanborn-convention controls; slice.bin
grep -E "^c34_" /workspace/k4c45/texts.txt > carved24.txt
python3 -c "from kryptos_text import K4;open('k4.txt','w').write(K4)"
python3 -c "
import random
k=open('k4.txt').read().strip()
for s in (1,2,3):
  l=list(k); random.Random(79000+s).shuffle(l); open(f'null_{s}.txt','w').write(''.join(l))"
for n in 0 1 2 3 4 5 6; do ./bookrk $(cat ctl_$n.txt) slice.bin texts79.txt 14 > out/ctl$n.out; done
./bookrk $(cat k4.txt) slice.bin texts79.txt 9 > out/k4.out
for s in 1 2; do ./bookrk $(cat null_$s.txt) slice.bin texts79.txt 9 > out/null$s.out; done
python3 verify79.py > verify79.txt
python3 gen79b.py                     # wrapping controls with K1 (63) / K0 Morse (81) keys
for n in 0 1 2; do ./carved_rk $(cat wctl_$n.txt) slice.bin carved24.txt 20 > out/wctl$n.out; done
for t in k4 null_1 null_2 null_3; do for c in 0 1 2 3 4 5 6 7; do
  echo "./carved_rk \$(cat $t.txt) /workspace/k4c45/chunk_$c carved24.txt 13 > out/full_${t}_c$c.out"; done; done | xargs -P 8 -I{} bash -c "{}"
