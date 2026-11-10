#!/bin/bash
# Cycle 197 controls: direct plants on the direct records (rec mode, AZ/KA + AZ>KA/KA>AZ, all pairs); decimation plants on the sample
# banks with the registered pair lists. Print threshold = the registered run's (E_config <= 0.002, I-214).
B=${B:-/workspace/k4c197}; T=$B/repo/tools/cycle197; D=$B/repo/data/cycle197; S=$B/sup; X=$B/cmp197
while read nm ct src N kind d q model solver ab form m n keys P; do
  case $src in
    direct*) $X rec $ct $D/recs197_direct.txt 98 del $nm 0 999 $S/azka2.txt $S/tab2.txt $T/pairsA_all.txt $T/pairsB_all.txt 0.002 ;;
    *) if [ $solver = A ]; then $X perm $ct $S/$src.bin $N $kind $nm 0 999999 $S/azka2.txt - $T/pairsA_$kind.txt - 0.002
       else $X perm $ct $S/$src.bin $N $kind $nm 0 999999 - $S/tab2.txt - $T/pairsB_$kind.txt 0.002; fi ;;
  esac
done < $T/ctl197.txt
