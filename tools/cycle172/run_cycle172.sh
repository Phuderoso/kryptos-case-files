#!/bin/bash
# Cycle 172 (IDEAS I-095): periodic Quagmire IV (two different keyed alphabets, 18,776 = vocabulary keyed on A-Z and on
# the KRYPTOS order, + A-Z, KA) behind 165,782 K3-law decimations / spiral-diagonal routes, both layer orders, p 1-16.
# K4 full (16 checkpointed chunks); 8 shuffled nulls on every 4th perm (41,446; 4 chunks each). Resumable: finished chunks skipped.
W=${W:-/workspace/k4c172}; cd $W; mkdir -p run/out
T=run/q4d172; A=support/alpha172.txt; K4=$(cat run/k4.txt)
{ NP=165782; S=16; ST=$(( (NP+S-1)/S )); for ((i=0;i<S;i++)); do echo "$K4 k4 support/all.bin $((i*ST)) $(((i+1)*ST)) c$i"; done
  NP=41446; S=4; ST=$(( (NP+S-1)/S )); while read lab ct; do for ((i=0;i<S;i++)); do echo "$ct $lab support/all_s4.bin $((i*ST)) $(((i+1)*ST)) c$i"; done; done < run/nulls172.txt
} | while read ct lab pf lo hi c; do [ -s run/out/${lab}.$c.txt ] && grep -q '^END' run/out/${lab}.$c.txt || echo "$ct $lab $pf $lo $hi $c"; done |
 xargs -P 8 -L 1 sh -c ''"$T"' "$0" '"$A"' "$2" "$1" "$3" "$4" 1 16 2>/dev/null > run/out/"$1"."$5".tmp && mv run/out/"$1"."$5".tmp run/out/"$1"."$5".txt'
date > run/out/done.txt
