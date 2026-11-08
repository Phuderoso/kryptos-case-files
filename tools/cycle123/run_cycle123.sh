#!/bin/sh
# Cycle 123 reproduction. Needs qg.bin (quadgrams, float32 log10, 26^4) and perms97.bin (165,065 bank) from the support backup.
set -e
S=${SUPPORT:-/home/box/kryptos_support_backup}; W=${WORK:-/workspace/k4c123}; mkdir -p $W
T=$(cd "$(dirname "$0")" && pwd)
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
gcc -O2 -o $W/cadenus $T/cadenus.c
python3 $T/gen_orders.py 7 $W/orders.txt                    # all orders w 2-7 + 3,889 keyword orders w 8-13
python3 -c "import itertools;f=open('$W/o8all.txt','w');[f.write('8 '+' '.join(map(str,p))+' all\n') for p in itertools.permutations(range(8))]"
python3 $T/plant.py > $W/controls.txt                       # 4 planted controls + 5 shuffled nulls
# controls (their own keyword orders)
python3 -c "import sys;sys.path.insert(0,'$T');from plant import kworder;[print(len(k),*kworder(k),k) for k in ['CADENUS','SHADOW','WELTZEITUH','BERLI']]" > $W/ctlorders.txt
for n in ctl1 ctl2 ctl3 ctl4; do ct=$(grep "^$n " $W/controls.txt|cut -d' ' -f2); $W/cadenus $ct $W/ctlorders.txt 13 $S/qg.bin $n > $W/ctl_$n.out; done
# K4 and nulls, p 1-13 exact
$W/cadenus $K4 $W/orders.txt 13 $S/qg.bin K4 > $W/k4_main.out
$W/cadenus $K4 $W/o8all.txt 13 $S/qg.bin K4w8all > $W/k4_w8all.out
for s in 1 2 3 4 5; do ct=$(grep "^null$s " $W/controls.txt|cut -d' ' -f2); $W/cadenus $ct $W/orders.txt 13 $S/qg.bin null$s > $W/null$s.out; done
for s in 1 2; do ct=$(grep "^null$s " $W/controls.txt|cut -d' ' -f2); $W/cadenus $ct $W/o8all.txt 13 $S/qg.bin null${s}w8 > $W/null${s}_w8all.out; done
# p 14-20: partial, 300 s cap (underdetermined; scored only)
timeout 300 $W/cadenus $K4 $W/orders.txt 20 $S/qg.bin K4p20 > $W/k4_p20.out || true
# audit of the 165k bank frame
python3 $T/frame_audit.py $S/perms97.bin
