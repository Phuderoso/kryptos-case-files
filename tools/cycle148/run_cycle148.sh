#!/bin/sh
# Cycle 148 full run (8 cores, ~2 min)
set -e
python3 streams.py > /dev/null   # writes streams.txt
gcc -O2 -o constkey constkey.c
python3 plant.py                 # writes controls.txt
K4=$(cat ../../data/k4.txt); B=${BANK:-perms97.bin}
./constkey $K4 streams.txt - K4direct 0 1 0 | tail -1
( echo "K4 $K4"; awk '/^null/{print $1, $4}' controls.txt ) | while read l t; do
  for c in 0 1 2 3 4 5 6 7; do echo "$l $t $((c*20634)) $(((c+1)*20634))"; done
done | xargs -P 8 -L 1 sh -c 'exec ./constkey $1 streams.txt '$B' $0 $2 $3 20 > bank_$0_$2.txt'
