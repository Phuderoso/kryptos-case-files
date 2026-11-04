#!/bin/bash
cd "$(dirname "$0")"
./bookrk $(cat k4.txt) perms97.bin texts.txt 8 > k4.out &
for n in 1 2 3 4; do ./bookrk $(cat ctl_$n.txt) perms97.bin texts.txt 12 > ctl_$n.out & done
for k in 1 2 3; do ./bookrk $(cat null_$k.txt) perms97.bin texts.txt 8 > null_$k.out & done; wait
for k in 4 5 6; do ./bookrk $(cat null_$k.txt) perms97.bin texts.txt 8 > null_$k.out & done; wait
echo done > run.log
