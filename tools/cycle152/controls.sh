#!/bin/bash
# Cycle 152 controls: plant (plant.py) -> zigfree survivors (c_ctl*.txt) -> independent Python recovery (check.py).
W=${W:-/workspace/k152}; B=/home/box/kryptos_support_backup/perms97.bin; cd "$W"; gcc -O2 -march=native -o zigfree zigfree.c
python3 plant.py > controls.txt
while read lab src q w r mp nu L d feed ix t; do case $lab in null*) continue;; esac
  if [ $src = - ]; then ./zigfree $t - $lab 0 1 20 9; else ./zigfree $t $B $lab $q $((q+1)) 20 9; fi > c_$lab.txt; done < controls.txt
grep -h "^S" c_ctl*.txt; python3 check.py controls.txt all.txt c_ctl*.txt
