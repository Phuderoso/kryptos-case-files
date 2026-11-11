#!/bin/bash
# Cycle 199 controls: each plant run on its own planted perm only (I-229), registered pair lists, threshold 0.002.
B=${B:-/workspace/k4c199}; T=$B/repo/tools/cycle197; X=$B/cmp197; S=$B/sup
while read nm ct src N kind d q model solver ab form m n keys P; do
  hit=$(timeout 30 $X perm $ct $S/$src.bin $N $kind $nm $q $((q+1)) - $S/tab2.txt - $T/pairsB_$kind.txt 0.002 | awk -v q=$q -v md=$model -v ab=$ab -v fm=$form -v m=$m -v n=$n '$1=="M"&&$4==q&&$6==md&&$7==ab&&$8==fm&&$9==m&&$10==n' | wc -l)
  if [ ${nm:0:1} = P ]; then r=$([ $hit -gt 0 ] && echo PASS || echo FAIL); else r=$([ $hit -eq 0 ] && echo PASS || echo FAIL); fi
  echo "$nm $src q $q d $d $model $ab $form $m x $n fits_at_planted_cell $hit $r"
done < $B/repo/tools/cycle199/ctl199.txt
