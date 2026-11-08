#!/bin/sh
cd /workspace/k4c128; K4=$(cat /tmp/kcf/data/k4.txt); c(){ grep "^$1 " controls.txt|cut -d' ' -f2; }
mkdir -p out
for n in K4 null1 null2; do if [ $n = K4 ]; then ct=$K4; else ct=$(c $n); fi
  for j in 0 1 2 3 4 5 6 7; do ./seqgro $ct $((j*12500)) $(((j+1)*12500)) $n > out/$n.$j & done; wait; done
echo DONE > done.flag
