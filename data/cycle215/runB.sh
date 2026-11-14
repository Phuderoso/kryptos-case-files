#!/bin/bash
cd /workspace/k4c215/w; R=../repo/data; export OMP_NUM_THREADS=1
K4=$(cat $R/k4.txt)
jobs_=()
echo "start $(date +%T)"
( ./wrbank $K4 bank.bin 17 19 100000 > B/k4_bank.txt ) &
( ./wrbank $K4 all.bin 17 19 100000 > B/k4_all.txt ) &
i=0; while read SH; do i=$((i+1)); echo "./wrbank $SH bank.bin 17 19 100000 > B/n193_$i.txt"; done < $R/cycle206/nulls_ct.txt > B/cmds.txt
i=0; while read SH; do i=$((i+1)); echo "./wrbank $SH all.bin 17 19 100000 > B/n195_$i.txt"; done < $R/cycle208/nulls_ct.txt >> B/cmds.txt
xargs -P 6 -I{} sh -c '{}' < B/cmds.txt
wait; echo "end $(date +%T)"
