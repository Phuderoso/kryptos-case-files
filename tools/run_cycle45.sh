#!/bin/bash
# Cycle 45: running keys (carved texts, Carter vol. I, KJV John; fwd+rev) behind cycle 44's rail fence / Redefence /
# AMSCO permutation files, using cycle 35's exact bitset tester tools/bookrk.c unchanged.
# Needs: perms_A.bin, perms_B.bin from tools/railamsco_gen.py (cycle 44); texts from cycles 34-36 prep scripts.
set -e
W=${W:-/workspace/k4c45}; cd $W
gcc -O3 -march=native -o bookrk /workspace/kcl/tools/bookrk.c
cat perms_A.bin perms_B.bin > all.bin
n=$(( $(stat -c%s all.bin)/194 )); per=$(( (n+7)/8 ))
split -b $((per*194)) -d -a 1 all.bin chunk_
python3 rk_railamsco_controls.py   # writes ctl_*.txt, ctl_*_slice.bin, null_*.txt, controls_planted.txt
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
{ for c in 0 1 2 3 4 5 6 7; do echo "./bookrk $K4 chunk_$c texts.txt 8 > k4_c$c.out"; done
  for k in 1 2 3; do for c in 0 5; do echo "./bookrk $(cat null_$k.txt) chunk_$c texts.txt 8 > null_${k}_c$c.out"; done; done
  for k in 1 2 3; do echo "./bookrk $(cat ctl_$k.txt) ctl_${k}_slice.bin texts.txt 12 > ctl_$k.out"; done; } > jobs.txt
xargs -P 8 -I{} bash -c "{}" < jobs.txt
