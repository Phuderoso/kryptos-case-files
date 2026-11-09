#!/bin/bash
# Cycle 167 controls: run shift3 on every plant (all 86,731 alphabets; bank plants at their own q), error plants in drop mode.
H=$(cd "$(dirname "$0")" && pwd); A=/home/box/kryptos_support_backup/alpha.bin; B=/home/box/kryptos_support_backup/perms97.bin
W=${W:-/workspace/k4c167/run167}; mkdir -p $W/ctl; cd $W/ctl
declare -A T=([28]=7 [66]=16 [70]=20 [24]=3)
while read lab ct kind layer q d a b1 b2 f k d2 d3 err; do
  if [ "$layer" = direct ]; then
    if [ -n "$err" ]; then p=${err#err=}; echo "$H/shift3 $ct $A - $lab 0 1 86731 ${T[$p]} > $lab.drop.txt; $H/shift3 $ct $A - $lab 0 1 86731 > $lab.txt"
    else echo "$H/shift3 $ct $A - $lab 0 1 86731 > $lab.txt"; fi
  else echo "$H/shift3 $ct $A $B $lab $q $((q+1)) 86731 > $lab.txt"; fi
done < $H/plants167.txt | xargs -P 8 -I{} bash -c '{}'
