#!/bin/sh
# Cycle 39: periodic affine substitution on either side of 165,065 transpositions (incl. identity).
# Needs perms97.bin (python3 export_perms.py) and qg.bin (quadgrams as float32, built from data/quadgrams.json).
cd "$(dirname "$0")"
gcc -O3 -march=native -o affine affine.c
python3 - <<'PY'
import json,struct
q=json.load(open('../data/quadgrams.json')); a=[q['floor']]*(26**4)
for k,v in q['q'].items():
    i=0
    for c in k: i=i*26+ord(c)-65
    a[i]=v
open('qg.bin','wb').write(struct.pack('%df'%len(a),*a))
PY
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
./affine $K4 perms97.bin qg.bin > r_k4.txt &
for s in 1 2 3 4 5 6 7 8 9 10; do ./affine $(python3 affine_controls.py null $s) perms97.bin qg.bin > r_null$s.txt & done
for s in 31 32 33 34 35 36; do ./affine $(python3 affine_controls.py control $s 2>meta_ctl$s.txt) perms97.bin qg.bin > r_ctl$s.txt & done
for s in 37 38 39; do ./affine $(python3 affine_controls.py control $s 1 2>meta_ctl$s.txt) perms97.bin qg.bin > r_ctl$s.txt & done
wait
python3 affine_summarize.py
