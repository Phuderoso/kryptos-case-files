#!/bin/bash
cd "$(dirname "$0")"
D=/workspace/kcl/data/c12_perm.bin; K=$(cat /workspace/k4c53/k4.txt)
./ragbaby $K alpha.bin 25 > K4_direct.out
while read n t; do ./ragbaby $t alpha.bin 25 > $n.out; done < ctl55.txt
for r in "0 25000" "25000 50000" "50000 75000" "75000 93334"; do ./ragperm $K alpha.bin $D themed_idx.txt $r > K4_perm_${r% *}.out & done
while read n t; do ./ragperm $t alpha.bin $D themed_idx.txt 0 93334 > $n.out & done < ctl55b.txt
wait; echo DONE > run55.log
