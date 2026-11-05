#!/bin/bash
# Cycle 70: X-stripped key texts, exact running-key test (carved_rk = tools/carved_rk69.c) over 165,065 transpositions in 8 chunks.
cd /workspace/k4c70
{ for t in k4 null_1 null_2 null_3 null_4 null_5 null_6; do for c in 0 1 2 3 4 5 6 7; do echo "$t chunk$c.bin 12"; done; done
  for n in 1 2 3 4 5 6; do echo "ctl_$n p20k.bin 24"; done; } > jobs.txt
xargs -P 8 -L 1 bash -c './carved_rk $(cat $0.txt) $1 texts70.txt $2 > out/${0}_${1%.bin}.out' < jobs.txt
echo done > run.log
