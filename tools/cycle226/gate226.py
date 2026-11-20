"""Cycle 226 Gate P: run kb226 on each plant's true scope row (as gate224.py), with the oracle and printbar -99, and record whether the
planted cell is reported (H line) and its P line (known, nqnc, NC). The decrypt-bar verdict is applied in summarize226.py.
usage: gate226.py WORKDIR -> gateP226.tsv"""
import sys, subprocess
W = sys.argv[1]; npr = {1: 165065, 2: 165782}; fn = {1: "bank.bin", 2: "all.bin"}
rows = []; nf = 0
for line in open(W + "/plants226.tsv"):
    pid, model, scope, row, d, ix, p, desc, bad, ct, pt = line.rstrip("\n").split("\t")
    scope, row, d, ix, p = int(scope), int(row), int(d), int(ix), int(p)
    args = [W + "/kb226", ct, "x" if scope == 0 else W + "/" + fn[scope], W + "/kb224.bin", W + "/geo224.txt",
            "1" if scope == 0 else str(npr[scope]), "0" if scope == 0 else str(row), model, "1000000", "24",
            W + "/qg.bin", W + "/oracle226.txt", "-99", "1000000"]
    o = subprocess.run(args, capture_output=True, text=True, env={"OMP_NUM_THREADS": "1"}).stdout
    want = dict(kv.split("=") for kv in desc.split())
    def match(h, needp):
        kv = dict(t.split("=", 1) for t in h.split()[2:] if "=" in t)
        if int(kv["perm"]) != (row if scope else -1) or int(kv["dir"]) != d: return None
        if any(kv.get(k) != v for k, v in want.items()): return None
        if int(kv["ix"]) != (ix if scope else 0): return None
        if needp and int(kv["p"]) != p: return None
        if not needp and p % int(kv["p"]) != 0: return None
        return kv
    found = any(match(h, False) for h in o.splitlines() if h.startswith("H " + model))
    pl = [match(h, True) for h in o.splitlines() if h.startswith("P " + model)]; pl = [k for k in pl if k]
    kv = pl[0] if pl else {}
    nf += found
    rows.append(f"{pid}\t{model}\t{scope}\t{p}\tbad={bad}\tfound={int(found)}\tknown={kv.get('known','<49')}\tnqnc={kv.get('nqnc','-')}\tnc={kv.get('nc','-')}\tpt={kv.get('pt','-')}\ttrue={pt}")
open(W + "/gateP226.tsv", "w").write("\n".join(rows) + "\n"); print("\n".join(r[:120] for r in rows)); print(f"FOUND {nf}/20")
