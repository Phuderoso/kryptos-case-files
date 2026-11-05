#!/bin/sh
# Cycle 57: Nicodemus and Slidefair exact crib tests + audit rerun of cycle 13 on omitted-letter transpositions. ~3 min on 8 cores.
set -e
python3 tools/mk57.py >/dev/null           # writes data/cycle57/qg.bin (not committed) and texts57.txt
gcc -O3 -o /tmp/nicodemus tools/nicodemus.c; gcc -O3 -o /tmp/slidefair tools/slidefair.c
gcc -O3 -fopenmp -o /tmp/periodic_perm tools/c/periodic_perm.c
while read t ct; do
  /tmp/nicodemus $ct data/alpha.bin 2000 7 11 20 > /tmp/nico_$t.out &
  /tmp/slidefair $ct data/alpha.bin 86731 48 > /tmp/slide_$t.out &
done < data/cycle57/texts57.txt; wait
for f in /tmp/nico_*.out /tmp/slide_*.out; do echo "=== $(basename $f)"; cat $f; done > data/cycle57/results57.txt
python3 -c "
import numpy as np
a=np.fromfile('data/c12_perm.bin',dtype='<i2').reshape(-1,97); CI=list(range(21,34))+list(range(63,74))
a[np.where(a[:,CI].min(1)<0)[0]].tofile('/tmp/c12_omit_crib.bin')"
/tmp/periodic_perm data/tw_alpha.bin /tmp/c12_omit_crib.bin $(cat data/k4.txt) 264 16 > data/cycle57/audit_c13_omit.out
