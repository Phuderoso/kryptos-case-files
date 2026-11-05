#!/bin/bash
# Cycle 82 runner: K4, 10 shuffled nulls, 6 planted controls through pfv82 (all checks>=0 hits recorded for p<=13).
cd "$(dirname "$0")"
K4=$(python3 -c "from kryptos_text import K4;print(K4)")
./pfv82 $K4 words.txt 5 > r_k4.txt &
for n in 0 1 2 3 4 5 6 7 8 9; do ./pfv82 $(cat null_$n.txt) words.txt 5 > r_null$n.txt & done
for n in 0 1 2 3 4 5; do ./pfv82 $(python3 -c "import json;print(json.load(open('controls82.json'))[$n]['ct'])") words_ctl.txt 5 > r_ctl$n.txt & done
wait; echo DONE > done.flag
