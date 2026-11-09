#!/bin/bash
# Cycle 190 planted controls: each plant scanned with cmp190 on its perm +- 50 (direct plants on direct.bin), PE 2.
W=${W:-/workspace/k4c190/w}; cd $W/run; mkdir -p ctl
while read name q alab model per slots ct; do
  if [ "$q" = "-1" ]; then pf=../support/direct.bin; lo=0; hi=1; else pf=../support/all.bin; lo=$((q-50)); hi=$((q+51)); fi
  al=../support/azka.txt; [ "$alab" != "AZ" ] && [ "$alab" != "KA" ] && al=../support/alpha_themed180.txt
  OMP_NUM_THREADS=8 setsid timeout 60 ./cmp190 $ct $pf $al $name $lo $hi 25 26 2 > ctl/$name.txt
done < planted190.txt
