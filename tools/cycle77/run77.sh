#!/bin/sh
# Cycle 77 run. Needs perms97.bin (cycle-22 export: python3 ../export_perms.py) and a264.bin (cycle-66 themed
# alphabets, tools/gen66.py) in this directory. Cycle 77 itself ran K4 + shuffled nulls 0-12 with transpositions
# (stopped at the ~8 min budget); nulls 13-19 resume from here. Resumable: each chunk writes out_<tag>_<chunk>.txt and is skipped if it already exists (with a DONE line).
gcc -O3 -o coord77 coord77.c
python3 -c "d=open('a264.bin','rb').read(); open('a2.bin','wb').write(d[26:52]+d[:26])"   # KA, A-Z
python3 -c "from kryptos_text import K4;print(K4)" > k4.txt
python3 controls77.py
python3 - <<'PY'
import random
from kryptos_text import K4
r = random.Random(77)
for i in range(20):
    s = list(K4); r.shuffle(s); open(f"null_{i}.txt", "w").write("".join(s))
PY
NP=165066; CH=8; STEP=$(( (NP + CH - 1) / CH ))
run_text () { tag=$1; txt=$2
  for c in $(seq 0 $((CH-1))); do f=out_${tag}_$c.txt
    if [ -f $f ] && grep -q '^DONE' $f; then continue; fi
    ( ./coord77 $txt perms97.bin a2.bin 2 6 $(( (c+1)*STEP )) $(( c*STEP )) > $f.tmp 2> $f.err && echo DONE >> $f.tmp && mv $f.tmp $f ) &
  done; wait; }
# direct, 264 themed alphabets (identity permutation only)
[ -f out_k4_direct264.txt ] || ./coord77 $(cat k4.txt) perms97.bin a264.bin 264 6 1 > out_k4_direct264.txt
for i in $(seq 0 19); do [ -f out_null${i}_direct264.txt ] || ./coord77 $(cat null_$i.txt) perms97.bin a264.bin 264 6 1 > out_null${i}_direct264.txt; done
# controls: 5,000-permutation window containing the planted permutation (KA + A-Z)
python3 - <<'PY'
import json, subprocess
for c in json.load(open("controls77_planted.json")):
    lo = max(0, c["perm"] - 2500)
    out = subprocess.run(["./coord77", c["carved"], "perms97.bin", "a2.bin", "2", "6", str(lo + 5000), str(lo)], capture_output=True, text=True).stdout
    open(f"out_ctl_{c['ctl']}.txt", "w").write(out)
PY
run_text k4 $(cat k4.txt)
for i in $(seq 0 19); do run_text null$i $(cat null_$i.txt); done
python3 summarize77.py
