"""Cycle 224 Gate P: run kb224 on each plant's true scope row and check the planted cell is reported. usage: gate224.py WORKDIR"""
import sys, subprocess, re
W = sys.argv[1]; npr = {1: 165065, 2: 165782}; fn = {1: "bank.bin", 2: "all.bin"}
ok = 0; rows = []
for line in open(W + "/plants224.tsv"):
    pid, model, scope, row, d, ix, p, desc, bad, ct, pt = line.rstrip("\n").split("\t")
    scope, row, d, ix, p = int(scope), int(row), int(d), int(ix), int(p)
    args = [W + "/kb224", ct, "x" if scope == 0 else W + "/" + fn[scope], W + "/kb224.bin", W + "/geo224.txt",
            "1" if scope == 0 else str(npr[scope]), "0" if scope == 0 else str(row), model, "1000000", "24"]
    o = subprocess.run(args, capture_output=True, text=True, env={"OMP_NUM_THREADS": "1"}).stdout
    want = dict(kv.split("=") for kv in desc.split())
    found = False
    for h in o.splitlines():
        if not h.startswith("H " + model): continue
        kv = dict(t.split("=") for t in h.split()[2:])
        if int(kv["perm"]) != (row if scope else -1) or int(kv["dir"]) != d: continue
        if any(kv.get(k) != v for k, v in want.items()): continue
        if model != "G":
            if int(kv["ix"]) != (ix if scope else 0): continue
            if p % int(kv["p"]) != 0: continue
        found = True; break
    ok += found; rows.append(f"{pid}\t{model}\t{scope}\t{row}\t{d}\t{ix}\t{p}\t{desc}\tbad={bad}\t{'PASS' if found else 'FAIL'}\thits_printed={sum(1 for h in o.splitlines() if h.startswith('H'))}")
print("\n".join(rows)); print(f"GATE P {ok}/20")
