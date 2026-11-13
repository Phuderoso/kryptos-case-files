#!/usr/bin/env python3
"""Cycle 211 (PREREG211, I-280): run the 20 Voynich-desk blind aligned L 16 plants (A01-A20) through wrbank.c UNCHANGED
on the full all.bin family at L 16, record every survivor line. Blind: no truth is read here.
usage: blind211.py WRBANK ALLBIN CIPHERTEXTS OUT.json"""
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
json.dump(dict(solver_sha256=hashlib.sha256(open(sys.argv[0].replace("blind211.py", "../cycle206/wrbank.c"), "rb").read()).hexdigest(),
               L=16, wall_s=round(time.time() - t0, 1), plants=res), open(OUT, "w"), indent=1)
