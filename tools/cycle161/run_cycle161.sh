#!/bin/bash
# Cycle 161 (IDEAS I-062): finish the cycle-159 rank-matched lineup with the UNCHANGED cycle-159 runner and cycle-155 solver.
# Resume: copy a cycle-159 work dir (results_raw.txt, nulls.txt) to $W; the runner skips finished chunks (C lines).
# Usage: W=/tmp/w161 REPO=$PWD bash tools/cycle161/run_cycle161.sh
set -e; W=${W:-/workspace/k4c161/run}; D=$(cd $(dirname "$0"); pwd); REPO=${REPO:-$D/../..}
[ -s $W/nulls.txt ] || cp $REPO/data/cycle159/nulls.txt $W/ 2>/dev/null || true   # nulls are regenerated deterministically otherwise
W=$W REPO=$REPO bash $REPO/tools/cycle159/run_cycle159.sh                              # 70 chunks in cycle 161 (364 s on 8 cores)
cd $W
python3 $D/summarize161.py results_raw.txt nulls.txt                                     # full range, per quarter, post-hoc q3
python3 $D/plant161.py > plants161.txt                                                   # 3 plants in 50-100M
while read n ct pa f pr note; do p=$((10#$pr)); ./gromark1e $ct 8 all $p $((p+1)) $n P; done < plants161.txt
for s in 0 1 2 3; do ./gromark1e $(cat ct_K4.txt) 8 all $((s*25000000)) $(((s+1)*25000000)) K4 P; done   # K4 regression 5/5/5/13
# L 9 checkpoint (not run): python3 $REPO/tools/cycle159/mknulls159.py 48 16100000 $REPO/data/k4.txt 9 > nulls_r9.txt
