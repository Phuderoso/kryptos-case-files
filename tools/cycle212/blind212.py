#!/usr/bin/env python3
"""Cycle 212 (PREREG212 part B, I-287): run the 10 Voynich-desk blind wrapped-offset L 16 plants (W01-W10) through wrbank.c UNCHANGED
on the full 165,065-row bank (perms97.bin) at L 16, record every survivor line. Blind: no truth is read here.
usage: blind212.py WRBANK ALLBIN CIPHERTEXTS OUT.json"""
import json, subprocess, sys, time, hashlib
BIN, BANK, CTS, OUT = sys.argv[1:5]
t0 = time.time(); res = []
for line in open(CTS):
    pid, ct = line.split()
    assert len(ct) == 97 and ct.isalpha() and ct.isupper()
    out = subprocess.run([BIN, ct, BANK, "16", "16", "1000000"], capture_output=True, text=True, timeout=200).stdout
    surv = [l for l in out.splitlines() if l.startswith("S ")]
    tot = [l for l in out.splitlines() if l.startswith("T ")][0]
    res.append(dict(id=pid, ct=ct, n_survivor_lines=len(surv), total_line=tot, survivors=surv))
    print(pid, "surv", len(surv), f"[{time.time()-t0:.1f}s]", flush=True)
json.dump(dict(solver_sha256=hashlib.sha256(open(sys.argv[0].replace("blind212.py", "../cycle206/wrbank.c"), "rb").read()).hexdigest(),
               L=16, wall_s=round(time.time() - t0, 1), plants=res), open(OUT, "w"), indent=1)
