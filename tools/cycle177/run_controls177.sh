#!/bin/bash
# Cycle 177 planted controls through gm177 / pg177 (after the main run; 4 threads). W = scratch with run/{gm177,pg177,
# controls177.txt,primers176.txt,cfg176.txt}, support/all.bin
W=${W:-/workspace/k4c177w}; cd $W; mkdir -p run/ctl; export OMP_NUM_THREADS=4
while read nm ct model ix L pa form b q key slots; do
  err=1; [ "$slots" = "-" ] && [ $b != 10 ] && err=0
  if [ $model = PG ]; then run/pg177 $ct support/all.bin run/cfg176.txt $nm $ix > run/ctl/$nm.txt
  elif [ $nm = ctl4 ]; then run/gm177 $ct support/all.bin $nm $((q-300)) $((q+300)) 1 0 0 10 1 run/primers176.txt > run/ctl/$nm.txt
  elif [ $ix = 0 ]; then run/gm177 $ct support/all.bin $nm 0 165782 0 2 $L $b $err > run/ctl/$nm.txt
  else run/gm177 $ct support/all.bin $nm $((q-300)) $((q+300)) 1 2 $L $b $err > run/ctl/$nm.txt; fi
  echo "$nm planted: $model ix$ix L$L $pa $form b$b q$q $key err-slots $slots"; grep '^M' run/ctl/$nm.txt | head -6
done < run/controls177.txt
