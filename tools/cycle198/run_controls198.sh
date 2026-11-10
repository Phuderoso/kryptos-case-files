#!/bin/bash
# Cycle 198 controls: direct plants on the 101 direct records (AZ/KA + both tableau pairs, registered pair lists); decimation plants on the
# M = N sample banks (both solvers, registered lists; only the planted perm q is run, the checker reads only that perm). Print threshold = the registered run's (U_config <= 0.05).
B=${B:-/workspace/k4c198}; T=$B/src; S=$B/sup; X=$B/cmp198
while read nm ct src N kind d q model solver ab form m n keys wrong P; do
  case $src in
    direct*) $X rec $ct $S/recs197_direct.txt 98 del $nm 0 999 $S/azka2.txt $S/tab2.txt $T/pairsA_all.txt $T/pairsB_all.txt 0.05 ;;
    *) $X perm $ct $S/$src.bin $N $kind $nm $q $((q+1)) $S/azka2.txt $S/tab2.txt $T/pairsA_$kind.txt $T/pairsB_$kind.txt 0.05 ;;
  esac
done < $T/ctl198.txt
