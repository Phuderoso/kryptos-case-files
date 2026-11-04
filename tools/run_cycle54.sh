#!/bin/bash
cd "$(dirname "$0")"
./splitkey $(cat ../data/k4.txt) alpha.bin qg.bin > K4.out
while read n t; do ./splitkey $t alpha.bin qg.bin > $n.out & done < ctl54.txt; wait
echo DONE > run54.log
