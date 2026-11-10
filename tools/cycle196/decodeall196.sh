#!/bin/bash
# Cycle 196: decode every fit printed in a full-power cell (all registered cells are full power) with decode196.py under every consistent deletion.
W=${W:-/workspace/k4c196/w}; cd $W; K4=$(cat run/k4.txt); AZ=ABCDEFGHIJKLMNOPQRSTUVWXYZ; KA=KRYPTOSABCDEFGHIJLMNQUVWXZ
for p in c1 c2; do bank=support/col$([ $p = c1 ] && echo 1 || echo 2).bin
  cat run/out/${p}a_k4.txt run/out/${p}b_k4.txt | awk '$1=="M"' | while read M lab row tab form md m n U slot; do
    t1=${tab%>*}; t2=${tab#*>}; T1=$([ $t1 = AZ ] && echo $AZ || echo $KA); T2=$([ $t2 = AZ ] && echo $AZ || echo $KA)
    idx=$(sed -n "$((row+1))p" support/col$([ $p = c1 ] && echo 1 || echo 2)_index.txt)
    echo "=== $p row $row [$idx] S$md $tab $form ${m}x$n config U $U reported slot $slot"
    python3 tools/decode196.py $K4 $bank $row $md $T1 $T2 $form $m $n 5 all; done; done
