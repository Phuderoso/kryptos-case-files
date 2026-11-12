#!/bin/bash
# 8 workers x 25M shuffles of K4 (seeds 1..8) + 8 x 5M iid-uniform texts (seeds 11..18); owned process group, 400 s cap
cd /workspace/k4c205/w259
for i in 1 2 3 4 5 6 7 8; do timeout 400 ./wnull 25000000 $i 0 > shuf_$i.out & done; wait
for i in 11 12 13 14 15 16 17 18; do timeout 300 ./wnull 5000000 $i 1 > iid_$i.out & done; wait
echo done > DONE
