#!/bin/bash
cd /workspace/k4c214/w; mkdir -p B; export OMP_NUM_THREADS=4
grep -v '^#' g_ct.txt | while read id ct rest; do
  [ ${#ct} -eq 97 ] || { ct=$id; id=X; }
  ./wrbank $ct bank.bin 16 16 200000 > B/$id.txt; echo "$id $(date +%T) $(grep '^T' B/$id.txt)"; done
echo end
