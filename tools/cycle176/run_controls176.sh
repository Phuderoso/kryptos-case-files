#!/bin/bash
# Cycle 176 planted controls through gm176 / pg176. W = scratch dir with run/{gm176,pg176,controls176.txt,primers176.txt,cfg176.txt}, support/all.bin
W=${W:-/workspace/k4c176}; cd $W; mkdir -p run/ctl
while read nm ct model ix L pa form q key; do
  if [ $model = PG ]; then OMP_NUM_THREADS=4 run/pg176 $ct support/all.bin run/cfg176.txt $nm $ix > run/ctl/$nm.txt
  elif [ $nm = ctl4 ]; then OMP_NUM_THREADS=4 run/gm176 $ct support/all.bin $nm $((q-300)) $((q+300)) $ix 0 0 run/primers176.txt > run/ctl/$nm.txt
  elif [ $ix = 0 ]; then OMP_NUM_THREADS=4 run/gm176 $ct support/all.bin $nm 0 165782 0 2 $L > run/ctl/$nm.txt
  else OMP_NUM_THREADS=4 run/gm176 $ct support/all.bin $nm $((q-300)) $((q+300)) 1 2 $L > run/ctl/$nm.txt; fi
  echo "$nm planted: $model ix$ix L$L $pa $form q$q $key"; grep '^M' run/ctl/$nm.txt | head -8
done < run/controls176.txt
