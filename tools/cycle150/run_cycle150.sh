#!/bin/sh
set -e
gcc -O2 -o zigauto zigauto.c; python3 plant.py > controls.txt
K=$(cat ../../data/k4.txt); B=${BANK:-perms97.bin}
./zigauto $K - K4direct 0 1 7 4 | tail -1
( echo "K4 $K"; awk '/^null/{print $1, $4}' controls.txt ) | while read l t; do
  for c in 0 1 2 3 4 5 6 7; do echo "$l $t $((c*20634)) $(((c+1)*20634))"; done
done | xargs -P 8 -L 1 sh -c 'exec ./zigauto $1 '$B' $0 $2 $3 12 9 > bank_$0_$2.txt'
