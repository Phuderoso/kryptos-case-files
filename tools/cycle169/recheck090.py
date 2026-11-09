"""Cycle 169 I-090 re-check: re-score quoted bookrk depths with the tail bits masked.
For each listed config (run dir, chunk file, perm index, carved text, model, mode, key text) it cuts the one permutation
and the one key text out, runs the original bookrk (unmasked) and bookrk1e (masked strict depth + one-error depth1) on
them with THR 1, and prints both depths for the listed model/mode. usage: recheck090.py BOOKRK BOOKRK1E LIST"""
import sys, subprocess, re, os, tempfile
bk, bk1, lst = sys.argv[1:4]
for line in open(lst):
    if not line.strip() or line.startswith('#'): continue
    label, run, chunk, p, car, model, mode, text = line.split()
    p = int(p); d = tempfile.mkdtemp()
    with open(f"{run}/{chunk}", "rb") as f: f.seek(194*p); open(f"{d}/p.bin", "wb").write(f.read(194))
    tx = [l for l in open(f"{run}/texts.txt") if l.split()[0] == text][0]; open(f"{d}/t.txt", "w").write(tx)
    a = subprocess.run([bk, car, f"{d}/p.bin", f"{d}/t.txt", "1"], capture_output=True, text=True).stdout
    b = subprocess.run([bk1, car, f"{d}/p.bin", f"{d}/t.txt", "1"], capture_output=True, text=True).stdout
    da = [int(m[1]) for m in re.finditer(rf"CAND depth=(\d+) perm=0 model={model} mode={mode} ", a)]
    db = [(int(m[1]), int(m[2])) for m in re.finditer(rf"CAND1 depth1=(\d+) depth=(\d+) perm=0 model={model} mode={mode} ", b)]
    print(f"{label}: {text} model {model} mode {mode}  unmasked depth {da[0] if da else 'n/a'}  masked depth {db[0][1] if db else '<1'}  one-error depth1 {db[0][0] if db else 'n/a'}")
