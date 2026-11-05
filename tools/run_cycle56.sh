#!/bin/bash
# Cycle 56 run: interrupted key, single words over all alphabets, two-word phrases (first 3000 words) over 298 themed alphabets
cd "$(dirname "$0")"; K=$(cat k4.txt)
( echo "K4 $K"; cat ctl56.txt ) > all56.txt
while read n t; do
  ./intkey $t alpha.bin words56.txt > ${n}_single.out &
  ./intkey2 $t alpha.bin words56.txt idx300.txt 3000 > ${n}_pairs.out &
  wait
done < all56.txt
echo DONE > run56.log
