#!/bin/sh
# Cycle 76 reproduction. Needs perms97.bin (cycle-22 export: python3 ../export_perms.py) in this directory.
# Controls are rebuilt by controls76.py (needs the cycle-74 English corpus); their carved texts are also
# stored in analysis/cycle76_controls_planted.json.
gcc -O3 -o nulltr76 nulltr76.c
python3 -c "from kryptos_text import K4;print(K4)" > k4.txt
python3 controls76.py
python3 - <<'PY'
import random
from kryptos_text import K4
r = random.Random(76)
for i in range(20):
    s = list(K4); r.shuffle(s); open(f"null_{i}.txt", "w").write("".join(s))
PY
for n in 0 1 2 3 4 5; do ./nulltr76 $(cat ctl_$n.txt) perms97.bin 1 > out_ctl_$n.raw & done; wait
./nulltr76 $(cat k4.txt) perms97.bin 5 > out_k4.txt
for i in $(seq 0 19); do ./nulltr76 $(cat null_$i.txt) perms97.bin 5 > out_null_$i.txt & done; wait
python3 summarize76.py
