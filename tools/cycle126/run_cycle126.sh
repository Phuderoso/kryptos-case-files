#!/bin/sh
cd /workspace/k4c126; K4=$(cat /tmp/kcf/data/k4.txt); c(){ grep "^$1 " controls.txt|cut -d' ' -f2; }
mkdir -p q w11
for n in K4 null1 null2 null3; do if [ $n = K4 ]; then ct=$K4; else ct=$(c $n); fi
  ./allcol2 $ct 9 -1 18 $n 23 > q/$n.w9; for f in 0 1 2 3 4 5 6 7 8 9; do ./allcol2 $ct 10 $f 18 $n 23 > q/$n.w10.$f & done; wait; done
for n in ctl4 K4 null1 null2; do if [ $n = K4 ]; then ct=$K4; else ct=$(c $n); fi
  for f in 0 1 2 3 4 5 6 7 8 9 10; do ./allcol2 $ct 11 $f 18 $n 0123 > w11/$n.$f & done; wait; done
echo DONE > done.flag
